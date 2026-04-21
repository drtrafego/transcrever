#!/usr/bin/env python3
"""
🎥 Video Transcription Agent - Main Entry Point

Sistema simples de transcrição de vídeos que monitora uma pasta e gera arquivos TXT.

Uso:
    python main.py [--input-folder PASTA] [--output-folder PASTA]

Exemplos:
    python main.py                                    # Usa configurações do .env
    python main.py --input-folder "C:/Videos"        # Pasta específica
    python main.py --output-folder "C:/Transcripts"  # Saída específica

Autor: Video Transcription Agent
Data: 2024
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent))


def setup_logging() -> None:
    """Configura o sistema de logging."""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    save_logs = os.getenv('SAVE_LOGS', 'true').lower() == 'true'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if save_logs:
        log_dir = Path("data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_dir / 'transcription.log'))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers,
        encoding='utf-8'
    )


def parse_arguments() -> argparse.Namespace:
    """Parse argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="🎥 Video Transcription Agent - Transcrição Simples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                                    # Usa configurações do .env
  python main.py --input-folder "C:/Videos"        # Pasta específica de entrada
  python main.py --output-folder "C:/Transcripts"  # Pasta específica de saída
        """
    )
    
    parser.add_argument(
        "--input-folder", "-i",
        type=str,
        help="Pasta com os vídeos para transcrever (sobrescreve .env)"
    )
    
    parser.add_argument(
        "--output-folder", "-o", 
        type=str,
        help="Pasta onde salvar as transcrições (sobrescreve .env)"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        help="Modelo Whisper a usar (tiny, base, small, medium, large-v3)"
    )
    
    parser.add_argument(
        "--language", "-l",
        type=str,
        help="Idioma dos vídeos (pt, en, auto)"
    )
    
    return parser.parse_args()


def get_config(args: argparse.Namespace) -> dict:
    """Carrega configuração do .env e argumentos."""
    config = {
        'input_folder': args.input_folder or os.getenv('INPUT_FOLDER_PATH'),
        'output_folder': args.output_folder or os.getenv('OUTPUT_FOLDER_PATH', 'data/outputs'),
        'whisper_model': args.model or os.getenv('WHISPER_MODEL', 'base'),
        'whisper_language': args.language or os.getenv('WHISPER_LANGUAGE', 'pt'),
        'whisper_device': os.getenv('WHISPER_DEVICE', 'auto'),
        'supported_formats': os.getenv('SUPPORTED_VIDEO_FORMATS', 'mp4,avi,mov,mkv,wmv,flv,webm,m4v').split(','),
        'max_concurrent': int(os.getenv('MAX_CONCURRENT_VIDEOS', '2')),
        'max_file_size_mb': int(os.getenv('MAX_FILE_SIZE_MB', '500')),
        'include_timestamp': os.getenv('INCLUDE_TIMESTAMP', 'true').lower() == 'true',
        'create_date_folders': os.getenv('CREATE_DATE_FOLDERS', 'true').lower() == 'true',
        'auto_monitor': os.getenv('AUTO_MONITOR', 'true').lower() == 'true',
        'monitor_interval': int(os.getenv('MONITOR_INTERVAL', '30')),
        'process_existing': os.getenv('PROCESS_EXISTING_FILES', 'true').lower() == 'true',
    }
    
    return config


def validate_config(config: dict) -> bool:
    """Valida a configuração."""
    logger = logging.getLogger(__name__)
    
    if not config['input_folder']:
        logger.error("Pasta de entrada nao configurada!")
        logger.error("   Configure INPUT_FOLDER_PATH no .env ou use --input-folder")
        return False
    
    input_path = Path(config['input_folder'])
    if not input_path.exists():
        logger.error(f"Pasta de entrada nao existe: {input_path}")
        return False
    
    if not input_path.is_dir():
        logger.error(f"Caminho nao e uma pasta: {input_path}")
        return False
    
    # Criar pasta de saída se não existir
    output_path = Path(config['output_folder'])
    output_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Pasta de entrada: {input_path}")
    logger.info(f"Pasta de saida: {output_path}")
    logger.info(f"Modelo Whisper: {config['whisper_model']}")
    logger.info(f"Idioma: {config['whisper_language']}")
    
    return True


def main() -> None:
    """Função principal do sistema."""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        logger.info("Video Transcription Agent - Iniciando...")
        
        # Parse argumentos
        args = parse_arguments()
        
        # Carregar configuração
        config = get_config(args)
        
        # Validar configuração
        if not validate_config(config):
            sys.exit(1)
        
        # Importar e executar processador
        from core.video_processor import VideoProcessor
        
        processor = VideoProcessor(config)
        processor.run()
        
    except KeyboardInterrupt:
        logger.info("Interrupcao solicitada pelo usuario")
    except Exception as e:
        logging.error(f"Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()