import subprocess
import os
import tempfile

def extract_mp3_from_video(video_path: str) -> str:
    """
    Extrai o áudio do vídeo especificado no formato MP3 usando FFmpeg localmente.
    Retorna o caminho temporário gerado ou levanta uma exceção em caso de erro.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")
        
    # Gera um caminho local na pasta temporária para o modelo
    temp_dir = tempfile.gettempdir()
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_mp3_path = os.path.join(temp_dir, f"{base_name}_extracted.mp3")
    
    # Se o temporário já existir (limpeza) apagamos
    if os.path.exists(output_mp3_path):
        os.remove(output_mp3_path)
    
    # Extrai mono (-ac 1) com bitrate moderado (128k) que minimiza tamanho
    # e entrega qualidade audível perfeita para o Whisper
    try:
        command = [
            "ffmpeg", "-y", "-i", video_path, 
            "-vn", "-acodec", "libmp3lame", "-ab", "128k", "-ac", "1",
            output_mp3_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_mp3_path
    except subprocess.CalledProcessError as e:
        if os.path.exists(output_mp3_path):
            os.remove(output_mp3_path)
        raise RuntimeError(f"Falha ao extrair áudio com ffmpeg: {e}")
