#!/usr/bin/env python3
"""Publie sur YouTube les fichiers de publications/*.json (appli Google « BMO Studio Link », API YouTube Data v3).

Un fichier = une vidéo ou un Short. Champs :
  chaine        nom du secret sans préfixe : "LEVRAIPRIX" → secret YT_REFRESH_TOKEN_LEVRAIPRIX
  video_url     lien public du MP4 (Release ou raw GitHub)
  titre, description, tags (liste), categorie (id YouTube, 27 = Éducation)
  miniature_url (facultatif)   commentaire (facultatif, posté sous la vidéo)
  publier_le    (facultatif) date ISO, ex. "2026-11-04T08:00:00+01:00" → la vidéo est mise en ligne à cette heure
  pour_enfants  false par défaut
Après envoi, le fichier part dans publications/fait/ avec l'id YouTube.
Tant que Google n'a pas audité l'appli, YouTube garde les vidéos en privé : il faut les passer en public dans Studio.
"""
import datetime as dt
import glob
import json
import os
import shutil
import sys
import tempfile
import time

import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SECRETS = json.loads(os.environ.get("SECRETS_JSON", "{}"))
CLIENT_ID, CLIENT_SECRET = SECRETS.get("YT_CLIENT_ID"), SECRETS.get("YT_CLIENT_SECRET")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly"]


def service(chaine):
    jeton = SECRETS.get(f"YT_REFRESH_TOKEN_{chaine}")
    if not (CLIENT_ID and CLIENT_SECRET and jeton):
        raise SystemExit(f"Secrets manquants : YT_CLIENT_ID, YT_CLIENT_SECRET ou YT_REFRESH_TOKEN_{chaine}")
    cred = Credentials(None, refresh_token=jeton, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                       token_uri="https://oauth2.googleapis.com/token", scopes=SCOPES)
    return build("youtube", "v3", credentials=cred, cache_discovery=False)


def telecharger(url, dossier, nom):
    chemin = os.path.join(dossier, nom)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(chemin, "wb") as f:
            for bloc in r.iter_content(1 << 20):
                f.write(bloc)
    return chemin


def publier(p, yt, dossier):
    video = telecharger(p["video_url"], dossier, "video.mp4")
    statut = {"privacyStatus": "public", "selfDeclaredMadeForKids": bool(p.get("pour_enfants", False))}
    if p.get("publier_le"):
        quand = dt.datetime.fromisoformat(p["publier_le"])
        if quand > dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=10):
            statut = {**statut, "privacyStatus": "private",
                      "publishAt": quand.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")}
    corps = {"snippet": {"title": p["titre"][:100], "description": p.get("description", "")[:5000],
                         "tags": p.get("tags", []), "categoryId": str(p.get("categorie", 27)),
                         "defaultLanguage": "fr", "defaultAudioLanguage": "fr"},
             "status": statut}
    media = MediaFileUpload(video, mimetype="video/mp4", chunksize=16 << 20, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=corps, media_body=media, notifySubscribers=True)
    rep = None
    while rep is None:
        etat, rep = req.next_chunk()
        if etat:
            print(f"  envoi {int(etat.progress() * 100)} %", flush=True)
    vid = rep["id"]
    print(f"  ✔ vidéo envoyée : https://youtu.be/{vid} (statut {rep['status'].get('privacyStatus')})", flush=True)
    res = {"id": vid, "lien": f"https://youtu.be/{vid}", "statut_youtube": rep["status"].get("privacyStatus")}
    if p.get("miniature_url"):
        try:
            img = telecharger(p["miniature_url"], dossier, "miniature.jpg")
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(img, mimetype="image/jpeg")).execute()
            res["miniature"] = "ok"
        except HttpError as e:
            res["miniature"] = f"refusée : {e.reason if hasattr(e, 'reason') else e}"
        print(f"  miniature : {res['miniature']}", flush=True)
    if p.get("commentaire"):
        try:
            yt.commentThreads().insert(part="snippet", body={"snippet": {"videoId": vid, "topLevelComment": {
                "snippet": {"textOriginal": p["commentaire"]}}}}).execute()
            res["commentaire"] = "ok"
        except HttpError as e:
            res["commentaire"] = f"refusé : {e}"
        print(f"  commentaire : {res['commentaire']}", flush=True)
    return res


def main():
    fichiers = sorted(glob.glob("publications/*.json"))
    if not fichiers:
        print("Rien à publier.")
        return
    erreurs = 0
    for f in fichiers:
        p = json.load(open(f, encoding="utf-8"))
        print(f"→ {f} : {p.get('titre')}", flush=True)
        try:
            with tempfile.TemporaryDirectory() as d:
                res = publier(p, service(p.get("chaine", "LEVRAIPRIX")), d)
            p["resultat"] = {**res, "envoye_le": dt.datetime.now(dt.timezone.utc).isoformat()}
            json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            shutil.move(f, os.path.join("publications/fait", os.path.basename(f)))
        except Exception as e:  # on continue avec les suivants
            erreurs += 1
            print(f"  ✘ échec : {e}", flush=True)
        time.sleep(2)
    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()
