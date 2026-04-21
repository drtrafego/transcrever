#!/usr/bin/env python3
"""
🚀 Script de Execução Rápida - Video Transcription Agent

Script simples para executar o sistema de transcrição.

Uso:
    python run.py                    # Usar configurações do .env
    python run.py "C:/Videos"        # Especificar pasta de entrada
    python run.py "C:/Videos" "C:/Saida"  # Especificar entrada e saída

Autor: Video Transcription Agent
Data: 2024
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Executa o sistema de transcrição."""
    
    # Construir comando base
    cmd = [sys.executable, "src/main.py"]
    
    # Se for --help, passar direto
    if len(sys.argv) >= 2 and sys.argv[1] in ["--help", "-h"]:
        cmd.append("--help")
    else:
        # Processar argumentos
        args = sys.argv[1:]
        i = 0
        
        # Argumentos posicionais (pasta de entrada e saída)
        positional_args = []
        while i < len(args) and not args[i].startswith('--'):
            positional_args.append(args[i])
            i += 1
        
        # Adicionar pasta de entrada
        if len(positional_args) >= 1:
            cmd.extend(["--input-folder", positional_args[0]])
            print(f"📁 Pasta de entrada: {positional_args[0]}")
        
        # Adicionar pasta de saída
        if len(positional_args) >= 2:
            cmd.extend(["--output-folder", positional_args[1]])
            print(f"📁 Pasta de saída: {positional_args[1]}")
        
        # Processar argumentos nomeados (--model, --language, etc.)
        while i < len(args):
            if args[i] in ["--model", "-m"] and i + 1 < len(args):
                cmd.extend([args[i], args[i + 1]])
                print(f"🎤 Modelo: {args[i + 1]}")
                i += 2
            elif args[i] in ["--language", "-l"] and i + 1 < len(args):
                cmd.extend([args[i], args[i + 1]])
                print(f"🌍 Idioma: {args[i + 1]}")
                i += 2
            else:
                # Passar outros argumentos diretamente
                cmd.append(args[i])
                i += 1
        
        print("🎥 Iniciando Video Transcription Agent...")
        print("   Para parar, pressione Ctrl+C")
        print("-" * 50)
    
    # Verificar se o arquivo principal existe
    main_file = Path("src/main.py")
    if not main_file.exists():
        print("❌ Erro: Arquivo src/main.py não encontrado!")
        print("   Execute este script a partir da pasta raiz do projeto.")
        sys.exit(1)
    
    try:
        # Executar o sistema
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro na execução: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()