"""Visuels « preuve à l'écran » de la vidéo électricité (17/11/2026).
Chaque image part d'une vraie capture (workflow « Captures de documents », releases captures-electricite-N, copiées dans
videos/electricite/medias/captures/) : recadrage, surligneur, flou des noms de fournisseur, caches « ? » sur les réponses
pas encore révélées. Sortie : episodes/electricite/medias/*.png (1920×1080).
Usage : python3 videos/electricite/_workspace/visuels.py"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
CAP = os.path.join(ICI, "..", "medias", "captures")
OUT = os.path.join(RACINE, "episodes", "electricite", "medias")
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
FOND, BLANC, ORANGE, JAUNE = (14, 15, 18), (242, 244, 247), (255, 107, 44), (255, 226, 60)
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FM = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"
if not os.path.exists(FB):
    FB = FM = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F = lambda s, g=True: ImageFont.truetype(FB if g else FM, s)


def prep(nom, box, hl=(), flou=(), caches=()):
    """Coordonnées de la capture d'origine : surligneur, flou, caches « ? », puis recadrage."""
    im = Image.open(os.path.join(CAP, nom)).convert("RGB")
    for b in flou:
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2])
    if hl:
        cal = Image.new("RGB", im.size, (255, 255, 255))
        d = ImageDraw.Draw(cal)
        for b in hl:
            d.rounded_rectangle(b, 6, fill=JAUNE)
        im = ImageChops.multiply(im, cal)
    d = ImageDraw.Draw(im)
    for b in caches:
        d.rounded_rectangle(b, 14, fill=(22, 24, 30))
        d.text(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), "?", font=F(int((b[3] - b[1]) * 0.8)), fill=ORANGE, anchor="mm")
    return im.crop(box)


def poser(c, sortie, bas=None, maxw=1760, maxh=940):
    """Pose le recadrage sur un fond flou sombre, centré, avec ombre ; texte facultatif en bas."""
    fond = c.resize((W, H)).filter(ImageFilter.GaussianBlur(50))
    im = Image.blend(Image.new("RGB", (W, H), FOND), fond, 0.25)
    if bas:
        maxh -= 150
    k = min(maxw / c.width, maxh / c.height, 2.4)
    c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
    x, y = (W - c.width) // 2, (H - (150 if bas else 0) - c.height) // 2 + (10 if bas else 0)
    ombre = Image.new("L", (W, H), 0)
    ImageDraw.Draw(ombre).rounded_rectangle((x - 6, y + 10, x + c.width + 6, y + c.height + 22), 18, fill=170)
    im.paste((0, 0, 0), (0, 0), ombre.filter(ImageFilter.GaussianBlur(22)))
    masque = Image.new("L", c.size, 0)
    ImageDraw.Draw(masque).rounded_rectangle((0, 0, c.width, c.height), 14, fill=255)
    im.paste(c, (x, y), masque)
    if bas:
        d = ImageDraw.Draw(im)
        lignes = bas.split("\n")
        for i, l in enumerate(lignes):
            d.text((W / 2, H - 150 + i * 50), l, font=F(36 if i < len(lignes) - 1 else 28, i < len(lignes) - 1), fill=BLANC if i < len(lignes) - 1 else (180, 189, 201),
                   anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
    im.save(os.path.join(OUT, sortie))
    print("ok", sortie)


# Comparateur officiel (accueil) et indicateur A-D
poser(prep("cap01_comparateur.png", (430, 200, 1520, 1080)), "cap01_comparateur_resultat_accueil.png")
poser(prep("cap01_comparateur.png", (430, 440, 1520, 1050)), "cap01_comparateur_resultat_saisie.png")
poser(prep("cap02_energieinfo_nouveautes.png", (120, 90, 1830, 440)), "cap01_comparateur_resultat.png")
poser(prep("cap02_energieinfo_nouveautes.png", (110, 440, 1260, 900)), "cap02_energieinfo_nouveautes.png")
# CRE : niveau de certitude
poser(prep("cap03_cre_niveau_certitude.png", (131, 58, 1110, 1270)), "cap03_cre_niveau_certitude.png")
poser(prep("cap03_cre_niveau_certitude.png", (131, 628, 1110, 1270)), "cap03_cre_niveau_certitude_b.png")
# Tarif bleu (délibération 2026-147, annexe B)
B = "cap04b_annexeB_base.png" if os.path.exists(os.path.join(CAP, "cap04b_annexeB_base.png")) else None
poser(prep("cap04_cre_annexeB.png", (100, 40, 1141, 720)), "cap04_cre_annexeB_base.png")
if B:
    poser(prep(B, (130, 60, 1110, 420), hl=[(255, 302, 450, 321)]), "cap04_cre_annexeB.png")
else:
    poser(prep("cap04_cre_annexeB.png", (100, 250, 1141, 900)), "cap04_cre_annexeB.png")
poser(prep("cap05_afp_facture_moyenne.png", (370, 120, 1550, 760)), "cap05_afp_facture_moyenne.png")
poser(prep("cap06_energieinfo_seule_composante.png", (124, 300, 1280, 720)), "cap06_energieinfo_seule_composante.png")
# CRE : rapport Cohérence des offres
poser(prep("cap07a_cre_coherence.png", (0, 0, 1241, 900)), "cap07a_cre_coherence_titre.png")
poser(prep("cap07a_cre_coherence.png", (0, 760, 1241, 1754)), "cap07a_cre_coherence_titre_sommaire.png")
poser(prep("cap07b_cre_coherence_591.png", (131, 58, 1110, 526), hl=[(146, 440, 1095, 495)]), "cap07b_cre_coherence_591.png")
# UFC-Que Choisir : titre + citation (lue sur la page, recopiée mot pour mot)
poser(prep("cap08b_ufc_titre.png", (124, 270, 1310, 600)), "cap08_ufc_wargon.png",
      bas="« … prendre contact avec les quelques fournisseurs qui maintiennent\nces offres à prix fixe très onéreuses »\nEmmanuelle Wargon, présidente de la CRE · citée par UFC-Que Choisir, 18/06/2026")
# Loi 2025-594, article 13 (JO du 01/07/2025)
poser(prep("cap09_loi_2025_594.png", (90, 1400, 1150, 1720), hl=[(100, 1462, 1140, 1528)]), "cap09_loi_2025_594.png")
poser(prep("cap10_faux_mediateur.png", (124, 470, 1840, 830)), "cap10_energieinfo_faux_mediateur.png")
# Journal du Net, 15/05/2026 (nom du fournisseur flouté)
poser(prep("cap11a_jdn_titre.png", (210, 440, 1180, 1000), flou=[(584, 862, 690, 905)]), "cap11a_jdn_titre.png")
poser(prep("cap11a_jdn_titre.png", (210, 440, 1180, 760)), "cap11a_jdn_titre_releves.png")
poser(prep("cap11b_jdn_on_ne_sait_pas.png", (215, 450, 1190, 545)), "cap11b_jdn_on_ne_sait_pas.png")
poser(prep("cap11b_jdn_on_ne_sait_pas.png", (215, 505, 1190, 625)), "cap11c_jdn_exceptionnel.png")
poser(prep("cap11d_jdn_ca_change_tout.png", (224, 448, 1184, 656), flou=[(884, 464, 962, 500)]), "cap11d_jdn_ca_change_tout.png")
poser(prep("cap11d_jdn_ca_change_tout.png", (224, 136, 1184, 320), flou=[(382, 210, 482, 247)]), "cap11e_jdn_mai2025.png")
poser(prep("cap11d_jdn_ca_change_tout.png", (224, 862, 1184, 1080)), "cap11f_jdn_denouement.png")
# JeChange, 06/11/2026 mis à jour le 11/11/2026 : « 42 % » caché jusqu'à la réponse (p090)
poser(prep("cap12_jechange.png", (40, 150, 1880, 530), flou=[(425, 262, 1028, 330)], caches=[(742, 340, 946, 406)]), "cap12_jechange.png")
im = prep("cap12_jechange.png", (40, 150, 1880, 530), flou=[(425, 262, 1028, 330)])
ImageDraw.Draw(im).rounded_rectangle((742 - 40, 404 - 150, 946 - 40, 404 - 150 + 10), 4, fill=ORANGE)
poser(im, "cap12_jechange_revele.png")
# energie-info : messages du fournisseur, offres dynamiques, étoiles du médiateur
poser(prep("cap13_energieinfo_messages.png", (124, 120, 1260, 420)), "cap13_energieinfo_messages.png")
poser(prep("cap13_energieinfo_messages.png", (124, 380, 1260, 660)), "cap13_energieinfo_messages_surligne.png")
poser(prep("cap14_energieinfo_dynamiques.png", (110, 300, 1290, 760)), "cap14_energieinfo_dynamiques.png")
poser(prep("cap16_energieinfo_etoiles.png", (110, 330, 1290, 860)), "cap16_energieinfo_etoiles.png")
# Baromètre énergie-info 2026 (médiateur, 03/11/2026)
poser(prep("cap15_barometre_2026.png", (60, 0, 1181, 1100)), "cap15_barometre_2026.png")
poser(prep("cap15b_barometre_hc.png", (70, 30, 1170, 420), hl=[(85, 272, 1160, 330)]), "cap15b_barometre_hc.png")
