#!/usr/bin/env python3
"""Génère la voix off de chaque scène dans public/ep/<slug>/voix/

Priorité pour chaque scène :
  1. Ta propre voix : episodes/<slug>/voix/<id>.(wav|mp3|m4a|ogg) → nettoyée et normalisée.
  2. Voix IA française Pocket TTS (Kyutai, code MIT) : modèle "french_24l", voix "estelle" (CC0) par défaut.
  3. VOIX_MOTEUR=silence : silence de la bonne durée (tests sans modèle).

Chaque voix IA passe par une chaîne de traitement "radio" réglée par mesure (scripts/analyse_voix.py) :
coupe-bas, creux dans le "carton" (220/380 Hz), présence (2,7/4,3 kHz), sifflantes maîtrisées,
débruitage, porte de bruit, compression douce, limiteur, normalisation en deux passes à -16 LUFS / -1,5 dBTP
(voir scripts/traitement_audio.py).
Écrit aussi <id>.json avec le minutage de chaque phrase (pour caler les sous-titres).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import wave

slug = sys.argv[1]
dossier_ep = os.path.join("episodes", slug)
montage = json.load(open(os.path.join(dossier_ep, "montage.json"), encoding="utf-8"))
reglages = montage.get("voix", {})
moteur = os.environ.get("VOIX_MOTEUR", reglages.get("moteur", "pocket"))
modele_nom = reglages.get("modele", "french_24l")
etapes = int(reglages.get("etapes", 5))  # étapes de calcul Pocket TTS : plus = moins de défauts, plus lent
locuteur = reglages.get("locuteur", "estelle")
temperature = float(reglages.get("temperature", 0.3))  # plus haut = plus expressif, moins stable
pause_phrase = float(reglages.get("pause_phrase", 0.22))
sortie = os.path.join("public", "ep", slug, "voix")
cache = os.path.join(".cache", "voix")
os.makedirs(sortie, exist_ok=True)
os.makedirs(cache, exist_ok=True)
SR = 48000

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from traitement_audio import EGALISATION_IA, EGALISATION_MICRO, EGALISATION_NEURONALE, ffmpeg, traiter  # noqa: E402


def duree(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def phrases(texte):
    if moteur == "edge":
        # Voix multilingue : une phrase isolée de moins de 6 mots peut basculer en anglais (retour d'Omar).
        # On synthétise tout le plan d'un coup et on rattache les phrases courtes à la précédente par une virgule.
        morceaux = re.split(r"(?<=[.!?…])\s+", texte.strip())
        sortie = []
        for m in morceaux:
            if sortie and len(re.findall(r"\w+", m)) < 6 and sortie[-1][-1:] in ".!":
                sortie[-1] = sortie[-1][:-1] + ", " + m[0].lower() + m[1:]
            else:
                sortie.append(m)
        return [" ".join(sortie)]

    morceaux = re.split(r"(?<=[.!?…])\s+", texte.strip())
    resultat = []
    for m in morceaux:  # coupe les phrases très longues sur les virgules (le modèle reste plus naturel)
        while len(m) > 220 and "," in m[:220]:
            i = m[:220].rfind(",") + 1
            resultat.append(m[:i].strip())
            m = m[i:].strip()
        if m:
            resultat.append(m)
    return resultat


_modele, _etat = None, None


def modele():
    global _modele, _etat
    if _modele is None:
        from pocket_tts import TTSModel

        print(f"Chargement de Pocket TTS ({modele_nom}, voix {locuteur})…", flush=True)
        _modele = TTSModel.load_model(language=modele_nom, temp=temperature, sampler_decode_steps=etapes)
        _etat = _modele.get_state_for_audio_prompt(locuteur)
    return _modele, _etat


def synthese(texte, dest, qui=None):
    voix_edge = (reglages.get("voix_secondaires", {}) or {}).get(qui, locuteur) if qui else locuteur
    if moteur == "edge":
        # Voix neuronale Microsoft Edge (choix d'Omar du 31/10/2026 : Vivienne). Gratuite, conditions d'usage à surveiller.
        from voix_edge import dire
        mp3 = dest + ".mp3"
        import time
        time.sleep(1.2)  # Microsoft limite le débit : on espace les appels
        for essai in range(12):
            try:
                dire(texte, voix_edge, mp3, reglages.get("debit", "+8%"), lang=False)  # <lang> refusé par le serveur : xml:lang='fr-FR' suffit
                if os.path.exists(mp3) and os.path.getsize(mp3) > 1000:
                    break
                raise RuntimeError("fichier audio vide")
            except Exception as e:  # limite de débit ou coupure : attente croissante (jusqu'à 90 s)
                attente = min(90, 5 * 2 ** min(essai, 5))
                print(f"  edge-tts : {e}, nouvel essai dans {attente} s", flush=True)
                time.sleep(attente)
        else:
            raise RuntimeError(f"Voix Edge indisponible après 12 essais : {texte[:60]}")
        ffmpeg("-i", mp3, "-ar", str(SR), "-ac", "1", dest)
        os.remove(mp3)
        return
    if moteur == "silence":
        ffmpeg("-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{max(0.6, len(texte.split()) / 2.6):.2f}", dest)
        return
    import scipy.io.wavfile

    m, etat = modele()
    audio = m.generate_audio(etat, texte)
    scipy.io.wavfile.write(dest, m.sample_rate, audio.numpy())


def _norm(t):
    return re.sub(r"[\W_]+", "", t.lower())


def aligner(morceaux, mots):
    """Rattache chaque mot minuté au morceau de texte qui le contient (par le compte des lettres).
    Renvoie [(debut_premier_mot, fin_dernier_mot)] par morceau, ou None si l'alignement n'est pas fiable."""
    cibles, acc = [], 0
    for m in morceaux:
        acc += len(_norm(m))
        cibles.append(acc)
    total_mots = sum(len(_norm(w["texte"])) for w in mots)
    if not mots or abs(total_mots - acc) > 0.08 * max(acc, 1):
        return None
    bornes, avant, k = [[None, None] for _ in morceaux], 0, 0
    for w in mots:
        while k < len(cibles) - 1 and avant >= cibles[k]:
            k += 1
        if bornes[k][0] is None:
            bornes[k][0] = w["debut"]
        bornes[k][1] = w["fin"]
        avant += len(_norm(w["texte"]))
    if any(b[0] is None for b in bornes):
        return None
    return bornes


def blocs_continus():
    """Regroupe les plans voisins lus par la même voix en blocs d'environ 120 mots maximum, lus d'un seul souffle.
    Coupe un bloc sur : plan sans texte (cartes titre), témoignage, voix d'Omar, changement de voix, devinette."""
    blocs, cur, mots_cur, qui_cur = [], [], 0, None
    def fermer():
        nonlocal cur, mots_cur
        if cur:
            blocs.append(cur)
        cur, mots_cur = [], 0
    for s in montage["scenes"]:
        texte = (s.get("texte") or "").strip()
        perso = any(os.path.exists(os.path.join(dossier_ep, "voix", f"{s['id']}.{e}")) for e in ("wav", "mp3", "m4a", "ogg"))
        if not texte or perso or s.get("temoignage"):
            fermer(); continue
        n = len(texte.split())
        if cur and (s.get("voix") != qui_cur or mots_cur + n > 120):
            fermer()
        cur.append(s); mots_cur += n; qui_cur = s.get("voix")
        if (s.get("schema") or {}).get("type") == "devine":
            fermer()
    fermer()
    return blocs


pre_rendus = {}
if moteur == "edge" and reglages.get("continu", True):
    from voix_edge import dire_avec_mots
    import time
    for bloc in blocs_continus():
        qui = bloc[0].get("voix")
        voix_bloc = (reglages.get("voix_secondaires", {}) or {}).get(qui, locuteur) if qui else locuteur
        texte_bloc = " ".join(s["texte"].strip() for s in bloc)
        cle = hashlib.sha1(json.dumps(["bloc-v1", voix_bloc, reglages.get("debit_continu", "+6%"), texte_bloc]).encode()).hexdigest()[:16]
        mp3, meta = os.path.join(cache, f"{cle}.mp3"), os.path.join(cache, f"{cle}.mots.json")
        if not (os.path.exists(mp3) and os.path.exists(meta)):
            for essai in range(8):
                try:
                    time.sleep(1.2)
                    mots = dire_avec_mots(texte_bloc, voix_bloc, mp3, reglages.get("debit_continu", "+6%"))
                    if os.path.getsize(mp3) > 1000 and mots:
                        json.dump(mots, open(meta, "w"), ensure_ascii=False)
                        break
                    raise RuntimeError("audio ou minutage vide")
                except Exception as e:
                    attente = min(90, 5 * 2 ** min(essai, 5))
                    print(f"  edge-tts (bloc) : {e}, nouvel essai dans {attente} s", flush=True)
                    time.sleep(attente)
            else:
                print("  bloc abandonné, lecture plan par plan", flush=True)
                continue
        mots = json.load(open(meta))
        bornes = aligner([s["texte"] for s in bloc], mots)
        if bornes is None:
            print(f"  alignement incertain pour {bloc[0]['id']}…{bloc[-1]['id']} : lecture plan par plan", flush=True)
            continue
        wav_bloc = os.path.join(cache, f"{cle}.wav")
        if not os.path.exists(wav_bloc):
            ffmpeg("-i", mp3, "-ar", str(SR), "-ac", "1", wav_bloc)
        fin_audio = duree(wav_bloc)
        for k, s in enumerate(bloc):
            # coupe au milieu du silence entre deux plans : chaque plan garde la moitié de la respiration naturelle
            debut = 0.0 if k == 0 else (bornes[k - 1][1] + bornes[k][0]) / 2
            fin = fin_audio if k == len(bloc) - 1 else (bornes[k][1] + bornes[k + 1][0]) / 2
            morceau = os.path.join(cache, f"{cle}-{k}.wav")
            ffmpeg("-i", wav_bloc, "-af", f"atrim=start={debut:.3f}:end={fin:.3f},asetpts=PTS-STARTPTS", morceau)
            # sous-titres : minutage réel de chaque phrase du plan
            phr = [p for p in re.split(r"(?<=[.!?…])\s+", s["texte"].strip()) if p]
            mots_plan = [w for w in mots if w["debut"] >= debut - 1e-3 and w["fin"] <= fin + 1e-3]
            bp = aligner(phr, mots_plan)
            segments = ([{"texte": p, "debut": max(0.0, b[0] - debut), "fin": b[1] - debut} for p, b in zip(phr, bp)]
                        if bp else [{"texte": s["texte"].strip(), "debut": bornes[k][0] - debut, "fin": bornes[k][1] - debut}])
            pre_rendus[s["id"]] = (morceau, segments)
        print(f"✔ bloc {bloc[0]['id']}…{bloc[-1]['id']} : {len(bloc)} plan(s) lus d'un seul souffle ({fin_audio:.1f} s)", flush=True)

for s in montage["scenes"]:
    sid, texte = s["id"], (s.get("texte") or "").strip()
    if sid in pre_rendus:
        morceau, segments = pre_rendus[sid]
        dest = os.path.join(sortie, f"{sid}.wav")
        traiter(morceau, dest, EGALISATION_NEURONALE)
        json.dump({"segments": segments, "continu": True}, open(dest[:-4] + ".json", "w"), ensure_ascii=False)
        continue
    perso = next((os.path.join(dossier_ep, "voix", f"{sid}.{ext}") for ext in ("wav", "mp3", "m4a", "ogg")
                  if os.path.exists(os.path.join(dossier_ep, "voix", f"{sid}.{ext}"))), None)
    dest = os.path.join(sortie, f"{sid}.wav")
    if perso:
        traiter(perso, dest, EGALISATION_MICRO)
        json.dump({"segments": [{"texte": texte, "debut": 0, "fin": duree(dest)}]}, open(dest[:-4] + ".json", "w"), ensure_ascii=False)
        print(f"✔ {sid} : ta voix ({os.path.basename(perso)})")
        continue
    if not texte:
        continue
    segments, fichiers, t = [], [], 0.0
    for p in phrases(texte):
        qui = s.get("voix")
        cle = hashlib.sha1(json.dumps(["fr-force-v1" if moteur == "edge" else "", moteur, modele_nom, locuteur, temperature, etapes, reglages.get("debit"), qui, p]).encode()).hexdigest()[:16]
        brut = os.path.join(cache, f"{cle}.wav")
        if not os.path.exists(brut):
            synthese(p, brut + ".tmp.wav", qui)
            ffmpeg("-i", brut + ".tmp.wav", "-ar", str(SR), "-ac", "1", brut)
            os.remove(brut + ".tmp.wav")
        d = duree(brut)
        segments.append({"texte": p, "debut": t, "fin": t + d})
        fichiers.append(brut)
        t += d + pause_phrase
    # Assemble les phrases avec de courtes pauses naturelles, puis traite l'ensemble.
    liste = os.path.join(cache, f"{slug}-{sid}.txt")
    silence = os.path.join(cache, f"silence-{pause_phrase}.wav")
    if not os.path.exists(silence):
        ffmpeg("-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(pause_phrase), silence)
    with open(liste, "w") as f:
        for i, fi in enumerate(fichiers):
            if i:
                f.write(f"file '{os.path.abspath(silence)}'\n")
            f.write(f"file '{os.path.abspath(fi)}'\n")
    brut_scene = os.path.join(cache, f"{slug}-{sid}-brut.wav")
    ffmpeg("-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", brut_scene)
    if moteur == "silence":
        shutil.copy(brut_scene, dest)
    elif moteur == "edge":
        traiter(brut_scene, dest, EGALISATION_NEURONALE)
    else:
        traiter(brut_scene, dest, EGALISATION_IA)
    json.dump({"segments": segments}, open(dest[:-4] + ".json", "w"), ensure_ascii=False)
    print(f"✔ {sid} : voix {moteur} ({t:.1f} s, {len(segments)} phrase(s))", flush=True)
