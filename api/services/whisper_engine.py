from faster_whisper import WhisperModel

print("🔄 Iniciando servidor Local de IA Faster-Whisper...")

try:
    # Usando o modelo base que requer pouca RAM e é muito mais rápido que o whisper normal
    model_size = "base"
    
    # Ele detectará se você tem GPU da NVIDIA no PC, senão cai na CPU que também é ultra rápida
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Configuração nativa de tipagem (float16 em GPU para rapidez, int8 em CPU pra não engasgar a máquina)
    compute_type = "float16" if device == "cuda" else "int8"
    
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    print(f"✅ Modelo '{model_size}' carregado localmente com sucesso! Dispositivo: {device}")
except Exception as e:
    print(f"⚠️ Erro crítico ao carregar motor de transcrição: {str(e)}")
    model = None

def transcribe_audio_file(audio_path: str, language: str = "pt") -> str:
    """
    Recebe o caminho de um MP3 e faz a leitura de forma paralela via IA local.
    """
    if not model:
        raise RuntimeError("O modelo do Faster Whisper não está ativo ou de erro de memória.")
        
    # 'segments' é um gerador de informações, vamos extrair de uma vez
    segments, info = model.transcribe(audio_path, language=language, beam_size=5)
    
    texto_final = ""
    for segment in segments:
        texto_final += segment.text + " "
        
    return texto_final.strip()
