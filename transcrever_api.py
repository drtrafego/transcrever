import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

def main():
    print("=== Transcrição via Whisper API (OpenAI) ===")
    
    # Carregar variáveis do .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERRO: Chave da API não encontrada!")
        print("Adicione OPENAI_API_KEY no seu arquivo .env")
        return

    client = OpenAI(api_key=api_key)
    
    # Caminhos
    video_path = Path("videos/videoplayback.mp4")
    if not video_path.exists():
        print(f"❌ Vídeo não encontrado: {video_path}")
        return
        
    audio_path = Path("videos/temp_audio.mp3")
    output_path = Path("transcrição/videoplayback_api.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"1. Extraindo áudio de {video_path.name}...")
    # Usando ffmpeg para extrair áudio (mp3, 128kbps para garantir tamanho < 25MB)
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video_path), 
            "-vn", "-acodec", "libmp3lame", "-ab", "128k", 
            str(audio_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Áudio extraído com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao extrair áudio com ffmpeg: {e}")
        return

    print("2. Enviando para a API do OpenAI (isso será muito mais rápido!)...")
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
            
        # Salvar o resultado
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)
            
        print(f"✅ Transcrição concluída! Salvo em: {output_path}")
    except Exception as e:
        print(f"❌ Erro na API do OpenAI: {e}")
    finally:
        # Limpar arquivo de áudio temporário
        if audio_path.exists():
            audio_path.unlink()

if __name__ == "__main__":
    main()
