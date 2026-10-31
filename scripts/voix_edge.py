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
