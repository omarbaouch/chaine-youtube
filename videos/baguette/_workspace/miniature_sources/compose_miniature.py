"""Miniature « baguette » : vraie photo (image du rendu à ~339,8 s), quignon coupé en orange = le blé (6 c)."""
import math, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops, ImageEnhance

SRC, OUT, FONT = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 1280, 720
ORANGE = (255, 107, 44)
BLANC = (242, 244, 247)
DX, DY = int(sys.argv[4]) if len(sys.argv) > 4 else -150, 6

photo = Image.open(SRC).convert("RGB").resize((W, H), Image.LANCZOS)
photo = ImageEnhance.Contrast(photo).enhance(1.08)

# Axe de la baguette principale (coordonnées photo 1280x720), quignon en A
A = (240, 140); B = (1272, 602)
L = math.dist(A, B); u = ((B[0]-A[0])/L, (B[1]-A[1])/L); n = (-u[1], u[0])
S_CUT = 0.062 * L        # 6 % de la longueur = la part du blé
GAP = 30
pt = lambda s, t: (A[0]+u[0]*s+n[0]*t, A[1]+u[1]*s+n[1]*t)

lum = photo.convert("L")
bread = lum.point(lambda v: 255 if v > 45 else 0).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
zone = Image.new("L", (W, H), 0)
ImageDraw.Draw(zone).polygon([pt(-30, -82), pt(S_CUT, -82), pt(S_CUT, 74), pt(-30, 74)], fill=255)
piece = ImageChops.multiply(bread, zone)

bg_col = tuple(int(v) for v in photo.crop((60, 20, 180, 90)).resize((1, 1), Image.BOX).getpixel((0, 0)))
base = photo.copy()
base.paste(Image.new("RGB", (W, H), bg_col), (0, 0), piece.filter(ImageFilter.MaxFilter(5)))

# Toile : photo décalée, bord droit fondu dans le noir
canvas = Image.new("RGB", (W, H), bg_col)
fade = Image.new("L", (W, H), 255); fd = ImageDraw.Draw(fade)
for i in range(60):
    fd.line([(W-60+i, 0), (W-60+i, H)], fill=int(255*(1-i/60)))
canvas.paste(base, (DX, DY), fade)

# Quignon : teinte orange (texture conservée), écarté vers le haut-gauche, halo
off = (int(-u[0]*GAP) + DX, int(-u[1]*GAP) + DY)
tinted = Image.blend(photo, Image.new("RGB", (W, H), ORANGE), 0.42)
tinted = ImageEnhance.Brightness(tinted).enhance(1.12)
m = Image.new("L", (W, H), 0); m.paste(piece, off)
glow = m.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(16))
canvas.paste(ORANGE, (0, 0), glow.point(lambda v: int(v*0.75)))
t2 = Image.new("RGB", (W, H)); t2.paste(tinted, off)
canvas.paste(t2, (0, 0), m)

# Ligne de coupe en pointillés dans l'écart
d = ImageDraw.Draw(canvas)
c = pt(S_CUT - GAP/2, 0); c = (c[0]+DX, c[1]+DY)
for t in range(-96, 90, 16):
    d.line([(c[0]+n[0]*t, c[1]+n[1]*t), (c[0]+n[0]*(t+9), c[1]+n[1]*(t+9))], fill=BLANC, width=4)

# Assombrir la zone de texte (haut droite) + vignette
vig = Image.new("L", (W, H), 0)
ImageDraw.Draw(vig).ellipse((600, -280, 1620, 500), fill=150)
vig = vig.filter(ImageFilter.GaussianBlur(90))
canvas = Image.composite(Image.new("RGB", (W, H), (8, 5, 4)), canvas, vig)
edge = Image.new("L", (W, H), 0)
ImageDraw.Draw(edge).rectangle((0, 0, W, H), outline=255, width=40)
edge = edge.filter(ImageFilter.GaussianBlur(40))
canvas = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), canvas, edge.point(lambda v: int(v*0.6)))

def text(xy, s, size, fill, anchor="la", stroke=8):
    global canvas
    f = ImageFont.truetype(FONT, size)
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).text((xy[0]+5, xy[1]+8), s, font=f, anchor=anchor, fill=210, stroke_width=stroke)
    canvas.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(9)))
    dr = ImageDraw.Draw(canvas)
    dr.text(xy, s, font=f, anchor=anchor, fill=fill, stroke_width=stroke, stroke_fill=(10, 8, 8))
    return dr.textbbox(xy, s, font=f, anchor=anchor, stroke_width=stroke)

RX = 1246
b1 = text((RX, 30), "LE BLÉ ?", 104, BLANC, "ra")
b2 = text((RX, b1[3]), "6", 250, ORANGE, "ra", stroke=10)
b3 = text((RX, b2[3] - 22), "CENTIMES", 92, ORANGE, "ra")

# Étiquette « 1 € » sur le corps de la baguette (pastille sombre, texte blanc)
f = ImageFont.truetype(FONT, 84)
lab = "1 €"
bb = ImageDraw.Draw(canvas).textbbox((0, 0), lab, font=f)
w, h = bb[2]-bb[0], bb[3]-bb[1]
bx, by = 470 + DX + 150, 290 + DY
pad = 20
panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(panel).rounded_rectangle((bx-pad, by-pad, bx+w+pad, by+h+pad+6), radius=18,
                                        fill=(12, 10, 10, 220), outline=BLANC + (255,), width=4)
canvas = Image.alpha_composite(canvas.convert("RGBA"), panel).convert("RGB")
ImageDraw.Draw(canvas).text((bx-bb[0], by-bb[1]+3), lab, font=f, fill=BLANC)

canvas.save(OUT, quality=92)
canvas.resize((320, 180), Image.LANCZOS).save(OUT.replace(".jpg", "_320.jpg"), quality=92)
