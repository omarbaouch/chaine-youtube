import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
import os

for f in fm.findSystemFonts():
    if "Inter" in f:
        fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Inter"

BG = "#0e0f12"; FG = "#f2f2f2"; MUTED = "#8a8f98"; RED = "#ff3b30"; GOLD = "#ffcc00"; GREEN = "#34c759"
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 19.2, 10.8


def fig():
    f = plt.figure(figsize=(W, H), dpi=100, facecolor=BG)
    return f


def save(f, name):
    f.savefig(os.path.join(OUT, name), facecolor=BG, dpi=100)
    plt.close(f)


def style(ax):
    ax.set_facecolor(BG)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=20)


def source(f, txt):
    f.text(0.04, 0.035, "Source : " + txt, color=MUTED, fontsize=16)


# 1/2/6 — Affiché vs réel (relevés UFC-Que Choisir, Black Friday 2025)
def promo_card(fname, enseigne, produit, barre, prix, aff, ref_label, ref, reel):
    f = fig()
    f.text(0.04, 0.9, f"{produit}", color=FG, fontsize=46, weight="bold")
    f.text(0.04, 0.84, f"{enseigne} — Black Friday 2025", color=MUTED, fontsize=26)
    # colonne gauche : ce qui est affiché
    f.text(0.06, 0.66, "CE QUI EST AFFICHÉ", color=MUTED, fontsize=22, weight="bold")
    t = f.text(0.06, 0.53, barre, color=MUTED, fontsize=54)
    f.canvas.draw()
    bb = t.get_window_extent().transformed(f.transFigure.inverted())
    ym = (bb.y0 + bb.y1) / 2
    f.add_artist(plt.Line2D([bb.x0 - 0.005, bb.x1 + 0.005], [ym, ym], color=RED, lw=6, transform=f.transFigure))
    f.text(0.06, 0.38, prix, color=FG, fontsize=90, weight="bold")
    f.text(0.06, 0.18, aff, color=RED, fontsize=110, weight="bold")
    # séparateur
    f.add_artist(plt.Line2D([0.5, 0.5], [0.12, 0.72], color="#2a2d34", lw=3, transform=f.transFigure))
    # colonne droite : la réalité
    f.text(0.56, 0.66, "LA RÉALITÉ", color=GOLD, fontsize=22, weight="bold")
    f.text(0.56, 0.53, ref_label, color=MUTED, fontsize=28)
    f.text(0.56, 0.38, ref, color=FG, fontsize=90, weight="bold")
    f.text(0.56, 0.18, reel, color=GREEN if reel != "−0 %" else MUTED, fontsize=110, weight="bold")
    f.text(0.56, 0.12, "de réduction réelle", color=MUTED, fontsize=24)
    source(f, "UFC-Que Choisir, « Black Friday 2025 – Encore des prix douteux », 26/11/2025")
    save(f, fname)


promo_card("01_casque_amazon.png", "Amazon", "Casque Beats Studio Pro",
           "399,95 €", "189 €", "−53 %", "Prix relevé avant le Black Friday", "259 €", "−27 %")
promo_card("02_aspirateur_boulanger.png", "Boulanger", "Aspirateur Dyson V8 Advanced",
           "399 €", "249 €", "−38 %", "Prix relevé avant le Black Friday", "279 €", "−11 %")
promo_card("06_frigo_rakuten.png", "Rakuten", "Réfrigérateur Haier FD 90 Série 7",
           "1 799 €", "1 549 €", "−13 %", "Prix sur d'autres sites", "1 500 €", "−0 %")

# 1b — Timeline du casque : la hausse de septembre
f = fig()
f.text(0.04, 0.9, "Comment le casque est passé à 399,95 €", color=FG, fontsize=46, weight="bold")
f.text(0.04, 0.84, "Beats Studio Pro chez Amazon — relevé UFC-Que Choisir", color=MUTED, fontsize=24)
ax = f.add_axes([0.08, 0.15, 0.86, 0.6]); style(ax)
x = [0, 1, 2, 3]
labels = ["Juillet", "Septembre →\nmois avant la promo", "Black Friday", "Autres sites\n(longtemps)"]
vals = [259, 399.95, 189, 279]
cols = [GREEN, RED, GOLD, MUTED]
bars = ax.bar(x, vals, color=cols, width=0.55)
for b, v in zip(bars, vals):
    t = f"{v:.2f}".replace(".", ",").replace(",00", "") + " €"
    ax.text(b.get_x() + b.get_width() / 2, v + 10, t, ha="center", color=FG, fontsize=32, weight="bold")
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=22, color=FG)
ax.set_ylim(0, 470); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.annotate("Devient le prix barré légal", xy=(1.28, 380), xytext=(1.6, 430), color=RED, fontsize=20,
            arrowprops=dict(arrowstyle="->", color=RED, lw=2))
source(f, "UFC-Que Choisir, 26/11/2025")
save(f, "01b_casque_chronologie.png")

# 3 — Le mécanisme des 30 jours (schéma)
f = fig()
f.text(0.04, 0.9, "La faille de la règle des 30 jours", color=FG, fontsize=46, weight="bold")
f.text(0.04, 0.84, "Schéma explicatif — valeurs illustratives", color=MUTED, fontsize=24)
ax = f.add_axes([0.08, 0.18, 0.86, 0.58]); style(ax)
days = list(range(0, 91))
price = [100 if d < 45 else (140 if d < 85 else 105) for d in days]
ax.step(days, price, where="post", color=FG, lw=5)
ax.axvspan(55, 85, color=GOLD, alpha=0.15)
ax.text(70, 152, "30 jours avant la promo\n= fenêtre de référence", ha="center", color=GOLD, fontsize=20)
ax.annotate("Prix gonflé\n+40 %", xy=(50, 140), xytext=(20, 150), color=RED, fontsize=22,
            arrowprops=dict(arrowstyle="->", color=RED, lw=2))
ax.annotate("« −25 % »\nBlack Friday", xy=(87, 105), xytext=(72, 80), color=GREEN, fontsize=22,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
ax.axhline(100, color=MUTED, ls="--", lw=2)
ax.text(2, 93, "Prix d'origine", color=MUTED, fontsize=18)
ax.set_xlim(0, 92); ax.set_ylim(60, 175)
ax.set_xticks([0, 45, 85]); ax.set_xticklabels(["Été", "Octobre", "Black Friday"], fontsize=22, color=FG)
ax.set_yticks([])
source(f, "Code de la consommation, art. L112-1-1 (en vigueur depuis le 28/05/2022)")
save(f, "03_faille_30_jours.png")

# 4 — Chiffres clés
f = fig()
f.text(0.04, 0.88, "Ce que disent les contrôles", color=FG, fontsize=50, weight="bold")
cards = [
    ("30 %", "des 314 vendeurs en ligne contrôlés\naffichaient des réductions incorrectes", "Commission européenne, mars 2026"),
    ("1 / 3", "des 1 000 établissements contrôlés\nen France présentait des anomalies", "Gouvernement, Black Friday 2023"),
    ("< 2 %", "de réduction réelle moyenne\nmesurée sur les promos", "UFC-Que Choisir, étude 2016"),
]
for i, (big, txt, src) in enumerate(cards):
    x0 = 0.04 + i * 0.32
    ax = f.add_axes([x0, 0.15, 0.29, 0.62]); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.04",
                                 fc="#1a1c21", ec="#2a2d34", lw=2, transform=ax.transAxes))
    ax.text(0.5, 0.66, big, ha="center", color=RED, fontsize=96, weight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.36, txt, ha="center", va="center", color=FG, fontsize=21, transform=ax.transAxes)
    ax.text(0.5, 0.1, src, ha="center", color=MUTED, fontsize=15, transform=ax.transAxes)
save(f, "04_chiffres_cles.png")

# 5 — La loi
f = fig()
f.text(0.04, 0.88, "Ce que dit la loi", color=FG, fontsize=50, weight="bold")
lines = [
    ("28 mai 2022", "Entrée en vigueur de l'article L112-1-1 (directive « Omnibus »)"),
    ("Règle", "Prix barré = prix le plus bas pratiqué sur les 30 derniers jours"),
    ("Promos en cascade", "La référence reste le prix d'avant la 1re remise"),
    ("Hors règle", "« Prix conseillé » et « prix de comparaison » : la brèche"),
]
for i, (k, v) in enumerate(lines):
    y = 0.68 - i * 0.15
    f.text(0.06, y, k, color=GOLD, fontsize=30, weight="bold")
    f.text(0.33, y, v, color=FG, fontsize=28)
source(f, "Code de la consommation ; DGCCRF ; UFC-Que Choisir")
save(f, "05_la_loi.png")
print("ok")
