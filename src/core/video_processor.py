#!/usr/bin/env python3
"""
🎥 Video Processor - Módulo Principal de Processamento

Responsável por:
- Monitorar pasta de vídeos
- Processar arquivos de vídeo
- Gerar transcrições com Whisper
- Salvar arquivos TXT organizados

Autor: Video Transcription Agent
Data: 2024
"""

import os
import time
import logging
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from faster_whisper import WhisperModel
import torch


class VideoProcessor:
    """Processador principal de vídeos para transcrição."""
    
    def __init__(self, config: dict):
        """
        Inicializa o processador de vídeos.
        
        Args:
            config: Dicionário com configurações
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.whisper_model = None
        self.processed_files = set()
        
        # Configurar caminhos
        self.input_folder = Path(config['input_folder'])
        self.output_folder = Path(config['output_folder'])
        self.cache_folder = Path(config.get('temp_cache_path', 'data/cache'))
        
        # Criar pastas necessárias
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.cache_folder.mkdir(parents=True, exist_ok=True)
        
        # Configurar formatos suportados
        self.supported_formats = [f".{fmt.lower()}" for fmt in config['supported_formats']]
        
        self.logger.info(f"VideoProcessor inicializado")
        self.logger.info(f"Entrada: {self.input_folder}")
        self.logger.info(f"Saida: {self.output_folder}")
        self.logger.info(f"Formatos: {', '.join(self.supported_formats)}")
    
    def load_whisper_model(self) -> None:
        """Carrega o modelo Faster-Whisper."""
        if self.whisper_model is not None:
            return
        
        model_name = self.config.get('whisper_model', 'base')
        device = self.config.get('whisper_device', 'auto')
        
        self.logger.info(f"Carregando modelo Faster-Whisper: {model_name}")
        
        try:
            if device == 'auto':
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
            
            compute_type = "float16" if device == "cuda" else "int8"
            
            self.whisper_model = WhisperModel(model_name, device=device, compute_type=compute_type)
            self.logger.info(f"Modelo carregado no dispositivo: {device} com {compute_type}")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar modelo Faster-Whisper: {e}")
            raise
    
    def find_video_files(self) -> List[Path]:
        """
        Encontra todos os arquivos de vídeo na pasta de entrada.
        
        Returns:
            Lista de caminhos para arquivos de vídeo
        """
        video_files = []
        
        for file_path in self.input_folder.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                # Verificar tamanho do arquivo
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                max_size = self.config['max_file_size_mb']
                
                if max_size > 0 and file_size_mb > max_size:
                    self.logger.warning(f"⚠️ Arquivo muito grande ({file_size_mb:.1f}MB): {file_path.name}")
                    continue
                
                # Verificar se já foi processado
                if str(file_path) not in self.processed_files:
                    video_files.append(file_path)
        
        return video_files
    
    def transcribe_video(self, video_path: Path) -> Optional[Dict]:
        """
        Transcreve um arquivo de vídeo convertendo para MP3 e usando Faster-Whisper.
        """
        self.logger.info(f"Preparando: {video_path.name}")
        
        mp3_path = None
        try:
            # 1. Extração de Áudio
            self.logger.info(f"Extraindo áudio leve de {video_path.name}...")
            temp_dir = tempfile.gettempdir()
            mp3_path = Path(temp_dir) / f"{video_path.stem}_temp.mp3"
            
            if mp3_path.exists():
                mp3_path.unlink()
                
            subprocess.run([
                "ffmpeg", "-y", "-i", str(video_path), 
                "-vn", "-acodec", "libmp3lame", "-ab", "128k", "-ac", "1",
                str(mp3_path)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 2. Transcrição
            self.logger.info(f"Transcrevendo: {video_path.name}")
            self.load_whisper_model()
            
            language = None if self.config['whisper_language'] == 'auto' else self.config['whisper_language']
            
            start_time = time.time()
            segments, info = self.whisper_model.transcribe(
                str(mp3_path),
                language=language,
                beam_size=5
            )
            
            # segments é um generator
            text = ""
            for segment in segments:
                text += segment.text + " "
                
            duration = time.time() - start_time
            self.logger.info(f"Transcrição concluída em {duration:.1f}s")
            
            return {
                "text": text.strip(),
                "language": info.language
            }
            
        except Exception as e:
            self.logger.error(f"Erro na transcrição de {video_path.name}: {e}")
            return None
        finally:
            if mp3_path and mp3_path.exists():
                mp3_path.unlink()
    
    def save_transcription(self, video_path: Path, transcription: Dict) -> Optional[Path]:
        """
        Salva a transcrição em arquivo TXT.
        
        Args:
            video_path: Caminho do vídeo original
            transcription: Resultado da transcrição do Whisper
            
        Returns:
            Caminho do arquivo TXT salvo ou None se erro
        """
        try:
            # Determinar pasta de saída
            output_dir = self.output_folder
            
            # Criar subpasta por data se configurado
            if self.config['create_date_folders']:
                date_str = datetime.now().strftime('%Y-%m-%d')
                output_dir = output_dir / date_str
                output_dir.mkdir(parents=True, exist_ok=True)
            
            # Gerar nome do arquivo
            base_name = video_path.stem
            if self.config['include_timestamp']:
                timestamp = datetime.now().strftime('%H%M%S')
                txt_filename = f"{base_name}_{timestamp}.txt"
            else:
                txt_filename = f"{base_name}.txt"
            
            txt_path = output_dir / txt_filename
            
            # Extrair texto da transcrição
            text = transcription.get('text', '').strip()
            
            if not text:
                self.logger.warning(f"⚠️ Transcrição vazia para: {video_path.name}")
                return None
            
            # Salvar arquivo TXT
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"# Transcrição de: {video_path.name}\n")
                f.write(f"# Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Modelo: {self.config['whisper_model']}\n")
                f.write(f"# Idioma: {transcription.get('language', 'auto')}\n")
                f.write("\n" + "="*50 + "\n\n")
                f.write(text)
                f.write("\n")
            
            self.logger.info(f"Transcricao salva: {txt_path}")
            return txt_path
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar transcricao: {e}")
            return None
    
    def process_video(self, video_path: Path) -> bool:
        """
        Processa um único arquivo de vídeo.
        
        Args:
            video_path: Caminho para o arquivo de vídeo
            
        Returns:
            True se processado com sucesso, False caso contrário
        """
        self.logger.info(f"Processando: {video_path.name}")
        
        try:
            # Transcrever vídeo
            transcription = self.transcribe_video(video_path)
            if not transcription:
                return False
            
            # Salvar transcrição
            txt_path = self.save_transcription(video_path, transcription)
            if not txt_path:
                return False
            
            # Marcar como processado
            self.processed_files.add(str(video_path))
            
            self.logger.info(f"Processamento concluido: {video_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro no processamento de {video_path.name}: {e}")
            return False
    
    def process_existing_files(self) -> None:
        """Processa arquivos existentes na pasta de entrada."""
        if not self.config['process_existing']:
            return
        
        self.logger.info("🔍 Procurando arquivos existentes...")
        video_files = self.find_video_files()
        
        if not video_files:
            self.logger.info("📭 Nenhum arquivo de vídeo encontrado")
            return
        
        self.logger.info(f"📹 Encontrados {len(video_files)} arquivos para processar")
        
        for video_path in video_files:
            self.process_video(video_path)
    
    def monitor_folder(self) -> None:
        """Monitora a pasta de entrada por novos arquivos."""
        self.logger.info(f"👁️ Monitorando pasta: {self.input_folder}")
        self.logger.info(f"⏱️ Intervalo: {self.config['monitor_interval']}s")
        
        while True:
            try:
                # Procurar novos arquivos
                video_files = self.find_video_files()
                
                if video_files:
                    self.logger.info(f"🆕 Encontrados {len(video_files)} novos arquivos")
                    
                    for video_path in video_files:
                        self.process_video(video_path)
                
                # Aguardar próxima verificação
                time.sleep(self.config['monitor_interval'])
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Monitoramento interrompido")
                break
            except Exception as e:
                self.logger.error(f"Erro no monitoramento: {e}")
                time.sleep(10)  # Aguardar antes de tentar novamente
    
    def run(self) -> None:
        """Executa o processador de vídeos."""
        self.logger.info("🚀 Iniciando Video Processor")
        
        try:
            # Processar arquivos existentes
            self.process_existing_files()
            
            # Iniciar monitoramento se configurado
            if self.config['auto_monitor']:
                self.monitor_folder()
            else:
                self.logger.info("Processamento de arquivos existentes concluido")
            
        except Exception as e:
            self.logger.error(f"Erro fatal no processador: {e}")
            raise