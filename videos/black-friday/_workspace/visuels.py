"""Visuels « preuve à l'écran » de la vidéo Black Friday (11/11/2026).
Chaque image part d'une vraie capture (UFC-Que Choisir, Commission européenne, SignalConso) : recadrage, surligneur,
caches « ? » sur les réponses pas encore révélées. Sortie : episodes/black-friday/medias/*.png (1920×1080).
Usage : python3 videos/black-friday/_workspace/visuels.py"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
CAP = os.path.join(ICI, "..", "medias", "captures")
OUT = os.path.join(RACINE, "episodes", "black-friday", "medias")
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
FOND, BLANC, ORANGE, BLEU, GRIS, VERT, ROUGE, JAUNE = (14, 15, 18), (242, 244, 247), (255, 107, 44), (127, 212, 255), (180, 189, 201), (52, 199, 89), (255, 59, 48), (255, 226, 60)
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FM = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"
if not os.path.exists(FM):
    FM = FB


def F(s, gras=True):
    return ImageFont.truetype(FB if gras else FM, s)


_cache = {}


def cap(nom):
    if nom not in _cache:
        _cache[nom] = Image.open(os.path.join(CAP, nom)).convert("RGB")
    return _cache[nom]


def fond(src=None):
    im = Image.new("RGB", (W, H), FOND)
    if src is not None:
        b = src.resize((W, H)).filter(ImageFilter.GaussianBlur(60))
        im = Image.blend(im, b, 0.22)
    return im


def preparer(nom, hl=(), flou=(), caches=()):
    """Travaille en coordonnées de la capture : surligneur, flou, caches « ? »."""
    im = cap(nom).copy()
    for b in flou:
        z = im.crop(b).filter(ImageFilter.GaussianBlur(9))
        im.paste(z, b[:2])
    if hl:
        cal = Image.new("RGB", im.size, (255, 255, 255))
        d = ImageDraw.Draw(cal)
        for b in hl:
            d.rounded_rectangle(b, 6, fill=JAUNE)
        im = ImageChops.multiply(im, cal)
    d = ImageDraw.Draw(im)
    for b in caches:
        d.rounded_rectangle(b, 16, fill=(22, 24, 30))
        h = b[3] - b[1]
        d.text(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), "?", font=F(int(h * 0.72)), fill=ORANGE, anchor="mm")
    return im


def papier(im, boite, lmax=1700, hmax=860, rayon=26):
    c = im.crop(boite)
    k = min(lmax / c.width, hmax / c.height)
    c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
    m = Image.new("L", c.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), rayon, fill=255)
    return c, m


def poser(base, c, m, cx=W // 2, cy=H // 2 + 10):
    x, y = int(cx - c.width / 2), int(cy - c.height / 2)
    ombre = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ombre).rounded_rectangle((x - 6, y + 14, x + c.width + 6, y + c.height + 30), 30, fill=(0, 0, 0, 170))
    base.paste(ombre.filter(ImageFilter.GaussianBlur(24)), (0, 0), ombre.filter(ImageFilter.GaussianBlur(24)))
    base.paste(c, (x, y), m)
    return x, y


def bandeau(base, texte, coul=BLEU):
    d = ImageDraw.Draw(base)
    d.text((70, 52), texte.upper(), font=F(36), fill=coul, anchor="lm")


def tampon(base, texte, coul, cx, cy, taille=120, angle=-9):
    f = F(taille)
    l = int(ImageDraw.Draw(base).textlength(texte, font=f)) + 90
    t = Image.new("RGBA", (l, taille + 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle((6, 6, l - 6, taille + 74), 22, fill=(14, 15, 18, 235), outline=coul, width=10)
    d.text((l / 2, (taille + 80) / 2), texte, font=f, fill=coul, anchor="mm")
    t = t.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)


def pastilles(base, actifs, x=1500, y=300):
    d = ImageDraw.Draw(base)
    for i, n in enumerate(["01", "02", "03"]):
        on = n in actifs
        yy = y + i * 190
        d.rounded_rectangle((x, yy, x + 300, yy + 150), 28, fill=ORANGE if on else (34, 37, 45), outline=BLEU if not on else None, width=4)
        d.text((x + 150, yy + 75), n, font=F(96), fill=FOND if on else GRIS, anchor="mm")


def sauver(im, nom):
    im.save(os.path.join(OUT, nom))


def preuve(nom_sortie, capture, boite, titre=None, hl=(), flou=(), caches=(), stamp=None, chips=None, lmax=1840, hmax=860, cx=None):
    src = preparer(capture, hl, flou, caches)
    base = fond(cap(capture).crop(boite))
    if chips is not None:
        lmax, cx = 1300, 730
    c, m = papier(src, boite, lmax, hmax)
    poser(base, c, m, cx or W // 2)
    if titre:
        bandeau(base, titre)
    if chips is not None:
        pastilles(base, chips)
    if stamp:
        tampon(base, *stamp)
    sauver(base, nom_sortie)


U3, U4, U5 = "ufc_bf2025_3.png", "ufc_bf2025_4.png", "ufc_bf2025_5.png"
# ── Casque (Amazon) ───────────────────────────────────────────────────────────
CARTE_C = (407, 392, 1167, 748)
BADGE_C, CONST_C = (1000, 396, 1163, 502), (762, 608, 1100, 726)
PRIX_C = (740, 518, 1167, 612)
preuve("casque_q.png", U3, CARTE_C, caches=[BADGE_C, CONST_C])
preuve("casque_53.png", U3, PRIX_C, hl=[(1030, 568, 1096, 604)], hmax=420)
preuve("casque_barre.png", U3, PRIX_C, hl=[(924, 562, 1030, 606)], hmax=420)
preuve("casque_legal.png", U3, CARTE_C, caches=[BADGE_C, CONST_C], stamp=("LÉGAL", VERT, 1380, 820))
preuve("casque_prix.png", U3, (560, 510, 1167, 612), hl=[(924, 562, 1030, 606)], caches=[], hmax=420)
PARA_C = (395, 868, 1180, 934)
FLOU_MOIS = [(395, 868, 585, 904), (668, 898, 1180, 934)]
preuve("casque_mois.png", U3, PARA_C, titre="UFC-Que Choisir, 26/11/2025", hl=[(586, 872, 1168, 902), (405, 900, 667, 930)], flou=FLOU_MOIS, hmax=300)
preuve("casque_pasconseille.png", U3, PARA_C, titre="Réflexe 02 : un vrai prix du mois", hl=[(586, 872, 1168, 902), (405, 900, 667, 930)], flou=FLOU_MOIS, hmax=300)
preuve("casque_279.png", U3, (395, 924, 1180, 962), titre="Réflexe 03 : ailleurs", hl=[(588, 928, 1162, 958)], flou=[(395, 924, 586, 962)], hmax=220)
preuve("casque_retour.png", U3, CARTE_C, caches=[BADGE_C, CONST_C], chips=[])
preuve("casque_revele.png", U3, CARTE_C)
preuve("casque_trompeuse.png", U3, (395, 784, 1180, 902), titre="UFC-Que Choisir, 26/11/2025", hl=[(618, 844, 1094, 874), (405, 872, 505, 902)],
       flou=[(506, 872, 1180, 902)], hmax=330, stamp=("LÉGAL… ET TROMPEUR", ORANGE, 960, 860, 96, -5))
preuve("ufc_peche.png", U3, (395, 82, 1180, 284), titre="UFC-Que Choisir, 26/11/2025", hl=[(733, 113, 1112, 143), (405, 141, 480, 171)], hmax=520)
preuve("ufc_titre.png", "ufc_bf2025_0.png", (380, 0, 1200, 560))

# Devinette n°1 : carte à gauche, 3 choix à droite (apparition cumulée)
for i, n in enumerate(["casque_d1.png", "casque_d2.png", "casque_d3.png"]):
    src = preparer(U3, caches=[BADGE_C, CONST_C])
    base = fond(cap(U3).crop(CARTE_C))
    c, m = papier(src, CARTE_C, 1020, 800)
    poser(base, c, m, 570)
    d = ImageDraw.Draw(base)
    d.text((1180, 200), "VENDU 399,95 €", font=F(54), fill=BLEU, anchor="lm")
    d.text((1180, 262), "PENDANT…", font=F(54), fill=BLEU, anchor="lm")
    for j, t in enumerate(["JAMAIS", "1 JOUR", "1 MOIS"][: i + 1]):
        y = 350 + j * 200
        on = j == i
        d.rounded_rectangle((1180, y, 1820, y + 160), 30, fill=ORANGE if on else (34, 37, 45))
        d.text((1500, y + 80), t, font=F(100), fill=FOND if on else GRIS, anchor="mm")
    sauver(base, n)

# ── Aspirateur (Boulanger) ────────────────────────────────────────────────────
CARTE_A = (407, 62, 1167, 418)
BADGE_A, CONST_A = (1000, 66, 1163, 170), (664, 282, 985, 396)
preuve("aspi_q.png", U4, CARTE_A, caches=[BADGE_A, CONST_A])
preuve("aspi_38.png", U4, (640, 190, 1167, 282), hl=[(832, 234, 902, 274), (903, 240, 968, 272)], hmax=420)
preuve("aspi_revele.png", U4, CARTE_A)
preuve("aspi_10sites.png", U4, (395, 540, 1180, 600), titre="UFC-Que Choisir, 26/11/2025", hl=[(725, 542, 1130, 572), (405, 570, 472, 600)], hmax=260)
# ── Frigo (Rakuten) ───────────────────────────────────────────────────────────
CARTE_F = (407, 142, 1167, 498)
BADGE_F, CONST_F = (1000, 146, 1163, 250), (762, 362, 1080, 476)
preuve("frigo_q.png", U5, CARTE_F, caches=[BADGE_F, CONST_F])
preuve("frigo_13.png", U5, (740, 270, 1167, 362), hl=[(952, 314, 1036, 352), (1038, 320, 1096, 350)], hmax=420)
FLOU_F = [(395, 622, 1180, 680)]
preuve("frigo_conseille.png", U5, (395, 534, 1180, 624), titre="UFC-Que Choisir, 26/11/2025", hl=[(566, 538, 822, 568)], hmax=320)
preuve("frigo_30j.png", U5, (395, 534, 1180, 624), titre="UFC-Que Choisir, 26/11/2025", hl=[(540, 594, 1150, 624)], hmax=320)
preuve("frigo_1500.png", U5, CARTE_F, caches=[BADGE_F])
preuve("frigo_revele.png", U5, CARTE_F)
preuve("reflexe2.png", U5, (395, 534, 1180, 596), hl=[(662, 538, 822, 568)], hmax=300)
preuve("cdiscount_titre.png", U5, (407, 712, 1167, 1060), hl=[(446, 752, 940, 790)])
preuve("cdiscount_rabais.png", U5, (427, 876, 1147, 964), titre="UFC-Que Choisir, 26/11/2025", hl=[(846, 904, 1087, 934), (446, 932, 587, 962)], hmax=330)
# Mosaïque des trois annonces (le casque reste masqué : sa réponse arrive à la fin)
for n, capt, boite, caches in [("mos_casque.png", U3, CARTE_C, [BADGE_C, CONST_C]), ("mos_aspi.png", U4, CARTE_A, []), ("mos_frigo.png", U5, CARTE_F, [])]:
    src = preparer(capt, caches=caches)
    c = src.crop(boite)
    k = H / c.height
    c = c.resize((int(c.width * k), H), Image.LANCZOS)
    base = Image.new("RGB", (W, H), (255, 255, 255))
    base.paste(c, ((W - c.width) // 2, 0))
    sauver(base, n)

# ── Commission européenne ─────────────────────────────────────────────────────
UE = "commission_ue_2.png"
preuve("ue_titre.png", "commission_ue_0.png", (200, 80, 1700, 520))
preuve("ue_30.png", UE, (296, 698, 1250, 768), titre="Commission européenne, 26/03/2026", hl=[(412, 704, 570, 736), (654, 704, 986, 736)], hmax=260)
preuve("ue_18.png", UE, (296, 902, 1250, 972), titre="Commission européenne, 26/03/2026", hl=[(358, 908, 692, 940)], hmax=260)
preuve("ue_10.png", UE, (296, 970, 1250, 1040), titre="Commission européenne, 26/03/2026", hl=[(358, 976, 558, 1008)], hmax=260)
preuve("signalconso.png", "signalconso_0.png", (300, 20, 1640, 900))


# ── Graphiques qui se construisent ────────────────────────────────────────────
def axes(d, titre, source):
    d.text((110, 90), titre, font=F(60), fill=BLANC, anchor="lm")
    d.line((180, 880, 1780, 880), fill=GRIS, width=4)
    d.text((110, 1010), "Source : " + source, font=F(28, False), fill=GRIS, anchor="lm")


def y_de(v, vmax):
    return 880 - int(640 * v / vmax)


# Faille des 30 jours : l'aspirateur (279 € en juillet, 399 € barré, 249 € le jour J)
PTS = [("JUILLET", 279), ("OCTOBRE", 399), ("NOVEMBRE", 399), ("BLACK FRIDAY", 249)]
XS = [340, 800, 1220, 1620]
for etape in range(1, 6):
    im = fond()
    d = ImageDraw.Draw(im)
    axes(d, "Aspirateur Dyson V8 Advanced, chez Boulanger", "UFC-Que Choisir, 26/11/2025")
    n = min(etape, 4)
    if etape >= 3:  # fenêtre légale des 30 jours
        d.rounded_rectangle((1010, 200, 1790, 878), 18, fill=(30, 40, 52))
        d.text((1400, 846), "LES 30 JOURS QUE REGARDE LA LOI", font=F(32), fill=BLEU, anchor="mm")
    xy = [(XS[i], y_de(PTS[i][1], 440)) for i in range(n)]
    if len(xy) > 1:
        d.line(xy, fill=BLANC, width=10, joint="curve")
    for i, (x, y) in enumerate(xy):
        heros = i == n - 1 and etape < 5
        d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=ORANGE if heros else BLANC)
        lab = f"{PTS[i][1]} €" + (" barré" if i == 2 else "")
        d.text((x, y - 62), lab, font=F(64), fill=ORANGE if heros else BLANC, anchor="mm")
        d.text((x, 925), PTS[i][0], font=F(34), fill=GRIS, anchor="mm")
    if etape >= 4:
        d.text((1620, y_de(249, 440) + 70), "affiché −38 %", font=F(44), fill=ROUGE, anchor="mm")
    if etape == 5:
        y = y_de(279, 440)
        for x in range(340, 1780, 44):
            d.line((x, y, x + 24, y), fill=ORANGE, width=8)
        d.text((1000, y + 46), "PRIX DE JUILLET : 279 €", font=F(46), fill=ORANGE, anchor="mm")
    sauver(im, f"faille{etape}.png")

# Chronologie du casque : 399,95 € le mois d'avant, 259 € en juillet, 189 € le jour J
BARRES = [("JUILLET", 259, ORANGE), ("LE MOIS AVANT LA PROMO", 399.95, BLANC), ("BLACK FRIDAY", 189, VERT)]
ORDRE = [[1], [1, 0], [1, 0, 2]]
for k, visibles in enumerate(ORDRE, 1):
    im = fond()
    d = ImageDraw.Draw(im)
    axes(d, "Casque Beats Studio Pro, chez Amazon", "UFC-Que Choisir, 26/11/2025")
    for i, (lab, v, coul) in enumerate(BARRES):
        x = 330 + i * 520
        if i in visibles:
            y = y_de(v, 440)
            d.rounded_rectangle((x, y, x + 300, 878), 14, fill=coul)
            d.text((x + 150, y - 60), (f"{v:.2f}".replace(".", ",") if v % 1 else str(int(v))) + " €", font=F(84), fill=coul, anchor="mm")
        d.text((x + 150, 925), lab if i in visibles else "?", font=F(34), fill=GRIS, anchor="mm")
    if k == 1:
        d.text((960, 190), "Hausse du prix en septembre", font=F(52), fill=ROUGE, anchor="mm")
    sauver(im, f"chrono{k}.png")
print(len(os.listdir(OUT)), "visuels")
