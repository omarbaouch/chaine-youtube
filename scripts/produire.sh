#!/usr/bin/env bash
# Pipeline complet d'un épisode : rushes → voix → timeline → rendu MP4 → planche de contrôle.
# Usage : bash scripts/produire.sh <slug> [--brouillon]
#   --brouillon : rendu rapide en 720p pour relire le montage
set -euo pipefail
slug="${1:?Usage : bash scripts/produire.sh <slug> [--brouillon]}"
mode="${2:-}"
cd "$(dirname "$0")/.."

echo "▶ 0/4 Musique";  node scripts/musique.mjs
echo "▶ 1/4 Rushes";   node scripts/medias.mjs "$slug"
echo "▶ 2/4 Voix";     python3 scripts/voix.py "$slug"
echo "▶ 3/4 Timeline"; node scripts/construire.mjs "$slug"

mkdir -p out
args=(remotion render src/index.ts Episode "out/$slug.mp4" "--props=public/ep/$slug/props.json" --codec=h264 --audio-bitrate=192k)
if [[ "$mode" == "--brouillon" ]]; then
  args+=(--scale=0.5 --crf=26); args[4]="out/$slug-brouillon.mp4"
else
  args+=(--crf=18)
fi
args+=("--concurrency=${REMOTION_CONCURRENCY:-50%}")
[[ -n "${REMOTION_BROWSER:-}" ]] && args+=("--browser-executable=$REMOTION_BROWSER")
echo "▶ 4/4 Rendu";  npx "${args[@]}"

# Mastering audio : -14 LUFS, le niveau de référence de YouTube (vidéo copiée sans réencodage).
ffmpeg -y -loglevel error -i "${args[4]}" -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=9" -c:a aac -b:a 192k -ar 48000 "${args[4]%.mp4}.master.mp4"
mv "${args[4]%.mp4}.master.mp4" "${args[4]}"

node scripts/planche.mjs "$slug" "${args[4]}"
echo "✅ Terminé : ${args[4]}"
