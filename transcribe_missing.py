#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

import argparse
from main import get_config, validate_config
from core.video_processor import VideoProcessor

def main():
    # Configuração específica para os 2 vídeos que faltam
    input_folder = "D:/GoogleDrive/MÉTODO VTD/JEJUM INTERMITENTE/VIDEOS - Aulas"
    output_folder = "D:/GoogleDrive/MÉTODO VTD/JEJUM INTERMITENTE/VIDEOS - Aulas/Transcrito"
    
    # Arquivos específicos para processar
    target_files = [
        "A aula mais importante.mp4",
        "Tudo sobre o jejum.mp4"
    ]
    
    print("🎯 Transcrevendo apenas os 2 vídeos que faltam:")
    for file in target_files:
        print(f"   - {file}")
    print()
    
    # Criar argumentos simulados
    args = argparse.Namespace()
    args.input_folder = input_folder
    args.output_folder = output_folder
    args.model = 'tiny'
    args.language = 'pt'
    args.device = 'auto'
    args.monitor = False
    
    # Configuração
    config = get_config(args)
    
    # Validar configuração
    validate_config(config)
    
    # Criar processador
    processor = VideoProcessor(config)
    
    # Processar apenas os arquivos específicos
    for filename in target_files:
        video_path = Path(input_folder) / filename
        if video_path.exists():
            print(f"🎬 Processando: {filename}")
            success = processor.process_video(video_path)
            if success:
                print(f"✅ Concluído: {filename}")
            else:
                print(f"❌ Erro ao processar: {filename}")
        else:
            print(f"⚠️ Arquivo não encontrado: {filename}")

if __name__ == "__main__":
    main()