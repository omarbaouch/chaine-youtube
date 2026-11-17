"""Captures de documents publics (preuves à l'écran) — tourne sur GitHub Actions (le réseau de la session cloud est fermé).
Entrée : un JSON [{"nom": "cap01.png", "url": "...", "texte": "phrase à surligner" (facultatif), "page": 3 (PDF, facultatif)}].
HTML : Playwright 1280×720 ×1,5 = 1920×1080, bannière cookies refusée/fermée, phrase centrée et surlignée en jaune.
PDF : téléchargé, page trouvée par pdftotext (ou `page`), rendue en PNG 150 dpi (recadrage fait ensuite à la main).
Usage : python3 scripts/captures.py liste.json dossier_sortie"""
import json, os, subprocess, sys, urllib.request

liste, sortie = json.load(open(sys.argv[1])), sys.argv[2]
os.makedirs(sortie, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

JS_SURLIGNE = """(t) => {
  const norm = s => s.replace(/\\s+/g,' ').replace(/[’']/g,"'").toLowerCase();
  const cible = norm(t).slice(0, 60);
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  let best = null;
  while (w.nextNode()) { const e = w.currentNode;
    if (!e.offsetParent && e !== document.body) continue;
    const txt = norm(e.innerText || '');
    if (txt.includes(cible) && (!best || txt.length < norm(best.innerText).length)) best = e; }
  if (!best) return false;
  best.style.background = '#FFE23C'; best.style.boxShadow = '0 0 0 6px #FFE23C'; best.style.color = '#111';
  best.scrollIntoView({block: 'center'}); return true; }"""

COOKIES = ["Tout refuser", "Refuser", "Continuer sans accepter", "Tout accepter", "Accepter", "J'accepte", "OK", "Fermer"]


def html(e, pw):
    nav = pw.chromium.launch()
    p = nav.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1.5, user_agent=UA, locale="fr-FR")
    p.goto(e["url"], wait_until="domcontentloaded", timeout=60000)
    p.wait_for_timeout(3500)
    for b in COOKIES:
        try:
            l = p.get_by_role("button", name=b, exact=False)
            if l.count():
                l.first.click(timeout=1500); p.wait_for_timeout(800); break
        except Exception:
            pass
    ok = True
    if e.get("texte"):
        ok = p.evaluate(JS_SURLIGNE, e["texte"]); p.wait_for_timeout(600)
    p.screenshot(path=os.path.join(sortie, e["nom"]))
    nav.close()
    return ok


def pdf(e):
    f = os.path.join(sortie, "_tmp.pdf")
    req = urllib.request.Request(e["url"], headers={"User-Agent": UA})
    open(f, "wb").write(urllib.request.urlopen(req, timeout=90).read())
    page = e.get("page")
    if not page and e.get("texte"):
        n = int([l for l in subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")][0].split()[-1])
        cible = " ".join(e["texte"].lower().split())[:40]
        for i in range(1, n + 1):
            t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), f, "-"], capture_output=True, text=True).stdout
            if cible in " ".join(t.lower().replace("’", "'").split()):
                page = i; break
    page = page or 1
    base = os.path.join(sortie, e["nom"][:-4])
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "150", "-png", "-singlefile", f, base], check=True)
    os.remove(f)
    return f"page {page}"


from playwright.sync_api import sync_playwright
rapport = []
with sync_playwright() as pw:
    for e in liste:
        try:
            r = pdf(e) if e["url"].lower().split("?")[0].endswith(".pdf") else html(e, pw)
            rapport.append(f"{e['nom']}: ok ({r})")
        except Exception as x:
            rapport.append(f"{e['nom']}: ÉCHEC {type(x).__name__} {str(x)[:200]}")
open(os.path.join(sortie, "rapport.txt"), "w").write("\n".join(rapport) + "\n")
print("\n".join(rapport))
