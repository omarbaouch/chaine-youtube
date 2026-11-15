"""Outils texte communs aux voix d'Omar : normalisation pour comparer ce qui est dit et ce qui est écrit."""
import re, unicodedata

from num2words import num2words


def _sans_accents(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def _nombre(m):
    s = m.group(0)
    if re.fullmatch(r"\d+[.,]\d+", s):
        a, b = re.split(r"[.,]", s)
        return f" {num2words(int(a), lang='fr')} {num2words(int(b), lang='fr')} "
    return f" {num2words(int(s), lang='fr')} "


def canon(texte):
    """Texte → jetons comparables (chiffres en lettres, sigles épelés, sans accents ni ponctuation)."""
    t = texte.replace("’", "'").replace(" ", " ")
    t = re.sub(r"\b1er\b", "premier", t)
    t = re.sub(r"(?<=\d) (?=\d{3}\b)", "", t)                 # 2 000 → 2000
    t = re.sub(r"\b([A-Z]{2,4})\b", lambda m: " ".join(m.group(1)), t)  # TVA → T V A
    t = t.replace("€", " euros ").replace("%", " pour cent ")
    t = re.sub(r"\d+(?:[.,]\d+)?", _nombre, t)
    t = _sans_accents(t.lower()).replace("-", " ").replace("'", " ")
    return ["euro" if x == "euros" else x for x in re.findall(r"[a-z]+", t)]


def phrases(texte):
    return [p.strip() for p in re.split(r"(?<=[.?!…])\s+", texte.strip()) if p.strip()]
