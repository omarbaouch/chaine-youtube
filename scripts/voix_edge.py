"""Voix Microsoft Edge (edge-tts) forcée en français.
edge-tts écrit xml:lang='en-US' dans le SSML : les voix « Multilingual » (Vivienne) lisent alors certains mots
à l'anglaise (« centimes » !). Retour d'Omar du 31/10/2026. On force fr-FR, avec un repli si le serveur refuse <lang>."""
import asyncio
import edge_tts
import edge_tts.communicate as _c

_MODE = {"lang": True}


def _mkssml(tc, escaped_text):
    if isinstance(escaped_text, bytes):
        escaped_text = escaped_text.decode("utf-8")
    corps = f"<lang xml:lang='fr-FR'>{escaped_text}</lang>" if _MODE["lang"] else escaped_text
    return ("<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='fr-FR'>"
            f"<voice name='{tc.voice}'><prosody pitch='{tc.pitch}' rate='{tc.rate}' volume='{tc.volume}'>"
            f"{corps}</prosody></voice></speak>")


_c.mkssml = _mkssml


def dire(texte, voix, dest_mp3, debit="+8%", lang=True):
    _MODE["lang"] = lang
    asyncio.run(edge_tts.Communicate(texte, voix, rate=debit).save(dest_mp3))


def dire_avec_mots(texte, voix, dest_mp3, debit="+6%", lang=False, hauteur="+0Hz"):
    """Lit tout un bloc d'un seul souffle et renvoie le minutage de chaque mot (secondes).
    Une seule lecture = une intonation qui suit le sens d'une phrase à l'autre (retour d'Omar du 02/11/2026)."""
    _MODE["lang"] = lang
    mots = []

    async def _run():
        com = edge_tts.Communicate(texte, voix, rate=debit, pitch=hauteur, boundary="WordBoundary")
        with open(dest_mp3, "wb") as f:
            async for m in com.stream():
                if m["type"] == "audio":
                    f.write(m["data"])
                elif m["type"] == "WordBoundary":
                    debut = m["offset"] / 1e7
                    mots.append({"texte": m["text"], "debut": debut, "fin": debut + m["duration"] / 1e7})

    asyncio.run(_run())
    return mots
