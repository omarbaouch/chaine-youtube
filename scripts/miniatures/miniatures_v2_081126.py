"""Miniatures v2 (08/11/2026) : une idée, un contraste, 3-4 mots, lisibles en 160 px de large."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

F = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
W, H = 1280, 720
BLANC, JAUNE, ROUGE, VERT, NOIR = (255, 255, 255), (255, 214, 0), (230, 30, 40), (40, 210, 90), (12, 12, 14)


def font(s):
    return ImageFont.truetype(F, s)


def cadre(img, box, size):
    """Recadre box (x, y, w, h) de l'image source et redimensionne à size."""
    x, y, w, h = box
    return img.crop((x, y, x + w, y + h)).resize(size, Image.LANCZOS)


def pop(img, c=1.25, s=1.3, b=1.05):
    img = ImageEnhance.Contrast(img).enhance(c)
    img = ImageEnhance.Color(img).enhance(s)
    return ImageEnhance.Brightness(img).enhance(b)


def texte(d, xy, t, taille, coul=BLANC, contour=10, ancre="la"):
    d.text(xy, t, font=font(taille), fill=coul, stroke_width=contour, stroke_fill=NOIR, anchor=ancre)


def pastille(d, xy, t, taille, fond, coul=BLANC, pad=(22, 10), ancre="la", rayon=18):
    f = font(taille)
    x0, y0, x1, y1 = d.textbbox(xy, t, font=f, anchor=ancre)
    d.rounded_rectangle((x0 - pad[0], y0 - pad[1], x1 + pad[0], y1 + pad[1]), rayon, fill=fond, outline=NOIR, width=5)
    d.text(xy, t, font=f, fill=coul, anchor=ancre)


def fleche(d, x, y, long, larg, coul, vers="bas"):
    s = 1 if vers == "bas" else -1
    tige = [(x - larg * .28, y), (x + larg * .28, y), (x + larg * .28, y + s * long * .55), (x - larg * .28, y + s * long * .55)]
    tete = [(x - larg / 2, y + s * long * .55), (x + larg / 2, y + s * long * .55), (x, y + s * long)]
    for poly in (tige, tete):
        d.polygon(poly, fill=coul, outline=NOIR, width=6)


def degrade_gauche(img, part=0.62, force=225):
    m = Image.new("L", (W, H))
    dm = ImageDraw.Draw(m)
    for x in range(int(W * part)):
        dm.line([(x, 0), (x, H)], fill=int(force * (1 - x / (W * part)) ** 1.3))
    noir = Image.new("RGB", (W, H), NOIR)
    return Image.composite(noir, img, m)


# 1) Cacao : la planteuse et ses cabosses | la tablette — « −60 % » contre « ? »
fem = Image.open("f-chocolat-103.jpg").convert("RGB")
tab = Image.open("f-chocolat-202.jpg").convert("RGB")
g = pop(cadre(fem, (250, 0, 740, 832), (640, 720)))
dr = pop(cadre(tab, (720, 60, 860, 968), (640, 720)), c=1.15, s=1.2, b=1.0)
img = Image.new("RGB", (W, H))
img.paste(g, (0, 0)); img.paste(dr, (640, 0))
d = ImageDraw.Draw(img)
d.rectangle((632, 0, 648, H), fill=NOIR)
pastille(d, (320, 40), "LE CACAO", 58, NOIR, ancre="ma")
fleche(d, 95, 455, 190, 140, ROUGE)
texte(d, (395, 560), "-60 %", 140, ROUGE, 12, "mm")
pastille(d, (960, 40), "TA TABLETTE", 58, NOIR, ancre="ma")
texte(d, (960, 470), "?", 360, JAUNE, 16, "mm")
img.save("mini-cacao.jpg", quality=92)

# 2) Gazole : le pistolet dans le réservoir — « BARIL ↓ » contre « TON PLEIN ↑ »
src = Image.open("f-essence-12.05.jpg").convert("RGB")
img = pop(cadre(src, (380, 0, 1480, 832), (W, H)), c=1.2, s=1.25)
img = degrade_gauche(img, 0.62, 245)
d = ImageDraw.Draw(img)
texte(d, (40, 60), "LE BARIL", 100, BLANC, 10)
fleche(d, 560, 40, 190, 150, VERT, "bas")
texte(d, (40, 300), "TON PLEIN", 100, BLANC, 10)
fleche(d, 680, 470, 190, 150, ROUGE, "haut")
pastille(d, (50, 540), "2,37 € / L", 96, ROUGE, ancre="la", pad=(26, 14))
img.save("mini-gazole.jpg", quality=92)

# 3) Baguette : les baguettes dorées — « TON 1 € » / « QUI LE PREND ? »
src = Image.open("f-baguette-219.5.jpg").convert("RGB")
img = pop(cadre(src, (0, 0, 1920, 1080), (W, H)), c=1.15, s=1.2)
img = degrade_gauche(img, 0.7, 210)
d = ImageDraw.Draw(img)
d.ellipse((60, 60, 330, 330), fill=JAUNE, outline=NOIR, width=10)
texte(d, (195, 198), "1 €", 120, NOIR, 0, "mm")
texte(d, (40, 400), "QUI LE", 130, BLANC, 12)
texte(d, (40, 545), "PREND ?", 130, JAUNE, 12)
img.save("mini-baguette.jpg", quality=92)

# Planche : grandes + taille téléphone (fil d'accueil ≈ 360 px)
pl = Image.new("RGB", (1280 + 380, 3 * 360 + 40), (30, 30, 30))
for i, n in enumerate(["cacao", "gazole", "baguette"]):
    m = Image.open(f"mini-{n}.jpg")
    pl.paste(m.resize((640, 360)), (0, i * 370))
    pl.paste(m.resize((320, 180)), (680, i * 370))
    pl.paste(m.resize((168, 94)), (1040, i * 370))
pl.save("planche-miniatures.jpg")
