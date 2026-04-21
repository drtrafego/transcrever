#!/usr/bin/env python3
import os
from pathlib import Path

# Pastas
videos_folder = Path("D:/GoogleDrive/MÉTODO VTD/JEJUM INTERMITENTE/VIDEOS - Aulas")
transcripts_folder = Path("D:/GoogleDrive/MÉTODO VTD/JEJUM INTERMITENTE/VIDEOS - Aulas/Transcrito")

# Encontrar todos os vídeos
video_files = []
for video_path in videos_folder.glob("*.mp4"):
    video_files.append(video_path.stem)  # Nome sem extensão

# Encontrar todas as transcrições
transcript_files = []
for transcript_path in transcripts_folder.rglob("*.txt"):
    # Remover timestamp do final do nome
    name = transcript_path.stem
    if '_' in name:
        # Remove o timestamp (últimos 6 dígitos após o último underscore)
        parts = name.split('_')
        if len(parts) > 1 and parts[-1].isdigit() and len(parts[-1]) == 6:
            name = '_'.join(parts[:-1])
    transcript_files.append(name)

# Encontrar vídeos não transcritos
missing = []
for video in video_files:
    if video not in transcript_files:
        missing.append(video)

print(f"Total de vídeos: {len(video_files)}")
print(f"Total de transcrições: {len(transcript_files)}")
print(f"Vídeos não transcritos: {len(missing)}")
print("\nVídeos que ainda precisam ser transcritos:")
for video in missing:
    video_path = videos_folder / f"{video}.mp4"
    if video_path.exists():
        size_mb = video_path.stat().st_size / (1024 * 1024)
        print(f"- {video}.mp4 ({size_mb:.1f}MB)")