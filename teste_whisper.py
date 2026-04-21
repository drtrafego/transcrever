#!/usr/bin/env python3
"""
Teste simples do Whisper para verificar se consegue processar um arquivo
"""

import whisper
from pathlib import Path
import os

def test_whisper():
    print("=== TESTE WHISPER ===")
    
    # Caminho do vídeo
    video_path = Path(r"D:\GoogleDrive\MÉTODO VTD\JEJUM INTERMITENTE\VIDEOS - Aulas\Como dividir o prato.mp4")
    
    print(f"Arquivo: {video_path}")
    print(f"Existe: {video_path.exists()}")
    print(f"Tamanho: {video_path.stat().st_size if video_path.exists() else 'N/A'} bytes")
    
    if not video_path.exists():
        print("❌ Arquivo não encontrado!")
        return
    
    try:
        print("\n1. Carregando modelo tiny...")
        model = whisper.load_model("tiny")
        print("✅ Modelo carregado!")
        
        print("\n2. Transcrevendo...")
        result = model.transcribe(str(video_path), language="pt", verbose=True)
        
        print("\n3. Resultado:")
        print(f"Texto: {result['text'][:200]}...")
        print(f"Idioma detectado: {result.get('language', 'N/A')}")
        
        print("\n✅ Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_whisper()