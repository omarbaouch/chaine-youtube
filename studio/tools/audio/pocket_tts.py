"""Pocket TTS (Kyutai) — voix off française de la chaîne, avec la chaîne de traitement "radio" mesurée.

Ajout propre à la chaîne d'Omar (pas dans OpenMontage d'origine). Voix validée à l'oreille par Omar :
modèle "french_24l", voix "estelle" (CC0), 5 étapes de calcul. Le son passe ensuite par
scripts/traitement_audio.py du dépôt (débruitage, égalisation, porte de bruit, compression, -16 LUFS).
Utiliser avec tts_selector(preferred_tool="pocket_tts").
"""

from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

_DEPOT = Path(__file__).resolve().parents[3]  # racine du dépôt chaine-youtube
_MODELES: dict[tuple, Any] = {}


def _traitement():
    sys.path.insert(0, str(_DEPOT / "scripts"))
    import traitement_audio  # noqa: PLC0415

    return traitement_audio


class PocketTTS(BaseTool):
    name = "pocket_tts"
    version = "0.1.0"
    tier = ToolTier.VOICE
    capability = "tts"
    provider = "kyutai_pocket"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.LOCAL

    dependencies = ["python:pocket_tts", "cmd:ffmpeg"]
    install_instructions = "pip install pocket-tts scipy --extra-index-url https://download.pytorch.org/whl/cpu"
    agent_skills = ["text-to-speech"]

    capabilities = ["text_to_speech", "offline_generation", "french_narration"]
    supports = {"voice_cloning": False, "multilingual": True, "offline": True, "native_audio": True}
    best_for = ["narration française naturelle gratuite (accent de France)", "chaîne YouTube d'Omar : voix par défaut"]
    not_good_for = ["clonage de voix (demande un compte Hugging Face)"]

    input_schema = {
        "type": "object",
        "required": ["text"],
        "properties": {
            "text": {"type": "string"},
            "language": {"type": "string", "default": "french_24l"},
            "voice": {"type": "string", "default": "estelle"},
            "steps": {"type": "integer", "default": 5},
            "temperature": {"type": "number", "default": 0.3},
            "radio_chain": {"type": "boolean", "default": True, "description": "Appliquer le traitement audio mesuré"},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=2, ram_mb=2048, vram_mb=0, disk_mb=800, network_required=False)
    retry_policy = RetryPolicy(max_retries=1, retryable_errors=[])
    idempotency_key_fields = ["text", "language", "voice", "steps", "temperature", "radio_chain"]
    side_effects = ["writes audio file to output_path"]
    user_visible_verification = ["Écouter : accent de France, pas de sifflements ni de 'tiiit'"]

    def get_status(self) -> ToolStatus:
        if importlib.util.find_spec("pocket_tts") is None:
            return ToolStatus.UNAVAILABLE
        return ToolStatus.AVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        if self.get_status() != ToolStatus.AVAILABLE:
            return ToolResult(success=False, error="Pocket TTS absent. " + self.install_instructions)
        debut = time.time()
        try:
            import scipy.io.wavfile
            from pocket_tts import TTSModel

            langue = inputs.get("language", "french_24l")
            voix = inputs.get("voice", "estelle")
            etapes = int(inputs.get("steps", 5))
            temp = float(inputs.get("temperature", 0.3))
            cle = (langue, etapes, temp)
            if cle not in _MODELES:
                _MODELES[cle] = TTSModel.load_model(language=langue, temp=temp, sampler_decode_steps=etapes)
            modele = _MODELES[cle]
            etat = modele.get_state_for_audio_prompt(voix)
            sortie = Path(inputs.get("output_path", "pocket_tts.wav"))
            sortie.parent.mkdir(parents=True, exist_ok=True)
            brut = sortie.with_suffix(".brut.wav")
            scipy.io.wavfile.write(brut, modele.sample_rate, modele.generate_audio(etat, inputs["text"]).numpy())
            if inputs.get("radio_chain", True):
                _traitement().traiter(str(brut), str(sortie))
                brut.unlink(missing_ok=True)
            else:
                brut.rename(sortie)
        except Exception as exc:  # noqa: BLE001
            return ToolResult(success=False, error=f"Pocket TTS a échoué : {exc}")
        return ToolResult(
            success=True,
            data={"provider": self.provider, "model": langue, "voice": voix, "steps": etapes, "output": str(sortie), "format": "wav"},
            artifacts=[str(sortie)],
            model=langue,
            duration_seconds=round(time.time() - debut, 2),
        )
