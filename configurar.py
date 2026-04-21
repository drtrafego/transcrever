#!/usr/bin/env python3
"""
⚙️ Configuração Automática - Video Transcription Agent

Script para configurar automaticamente o sistema de transcrição.
Você só precisa informar a pasta dos seus vídeos!

Uso:
    python configurar.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv, set_key

def clear_screen():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Imprime o cabeçalho."""
    print("🎥" + "=" * 60 + "🎥")
    print("    VIDEO TRANSCRIPTION AGENT - CONFIGURAÇÃO AUTOMÁTICA")
    print("🎥" + "=" * 60 + "🎥")
    print()

def get_folder_input(prompt, default=None):
    """Solicita uma pasta do usuário com validação."""
    while True:
        if default:
            folder = input(f"{prompt} (padrão: {default}): ").strip()
            if not folder:
                folder = default
        else:
            folder = input(f"{prompt}: ").strip()
        
        if not folder:
            print("❌ Por favor, informe uma pasta válida!")
            continue
        
        # Converter para Path e normalizar
        folder_path = Path(folder).resolve()
        
        # Verificar se existe (para pasta de entrada) ou criar (para pasta de saída)
        if "entrada" in prompt.lower() or "vídeos" in prompt.lower():
            if folder_path.exists() and folder_path.is_dir():
                return str(folder_path)
            else:
                print(f"❌ Pasta não encontrada: {folder_path}")
                print("   Verifique se o caminho está correto.")
                continue
        else:
            # Para pasta de saída, criar se não existir
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
                return str(folder_path)
            except Exception as e:
                print(f"❌ Erro ao criar pasta: {e}")
                continue

def configure_env():
    """Configura o arquivo .env interativamente."""
    print("📝 CONFIGURAÇÃO DO SISTEMA")
    print("-" * 40)
    
    # Carregar .env existente
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv()
    
    # 1. Pasta de entrada (obrigatória)
    print("1️⃣ PASTA DOS VÍDEOS (obrigatória)")
    print("   Onde estão os vídeos que você quer transcrever?")
    current_input = os.getenv("INPUT_FOLDER_PATH", "")
    if current_input:
        print(f"   Atual: {current_input}")
    
    input_folder = get_folder_input("📁 Pasta dos vídeos", current_input if current_input else None)
    
    # 2. Pasta de saída (opcional)
    print("\n2️⃣ PASTA DE SAÍDA (opcional)")
    print("   Onde salvar as transcrições? (deixe vazio para usar 'data/outputs')")
    current_output = os.getenv("OUTPUT_FOLDER_PATH", "")
    if current_output:
        print(f"   Atual: {current_output}")
    
    output_folder = input(f"📁 Pasta de saída (padrão: data/outputs): ").strip()
    if not output_folder:
        output_folder = str(Path("data/outputs").resolve())
    else:
        output_folder = str(Path(output_folder).resolve())
        Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # 3. Modelo Whisper
    print("\n3️⃣ MODELO WHISPER")
    print("   tiny   = Mais rápido, qualidade básica")
    print("   base   = Equilibrado (recomendado)")
    print("   small  = Boa qualidade")
    print("   medium = Alta qualidade")
    print("   large-v3 = Máxima qualidade (mais lento)")
    
    current_model = os.getenv("WHISPER_MODEL", "base")
    model = input(f"🎤 Modelo (padrão: {current_model}): ").strip()
    if not model:
        model = current_model
    
    # 4. Idioma
    print("\n4️⃣ IDIOMA")
    print("   pt   = Português")
    print("   en   = Inglês")
    print("   auto = Detectar automaticamente")
    
    current_lang = os.getenv("WHISPER_LANGUAGE", "pt")
    language = input(f"🌍 Idioma (padrão: {current_lang}): ").strip()
    if not language:
        language = current_lang
    
    # 5. Monitoramento automático
    print("\n5️⃣ MONITORAMENTO AUTOMÁTICO")
    print("   Quer que o sistema monitore automaticamente por novos vídeos?")
    
    current_auto = os.getenv("AUTO_MONITOR", "true")
    auto_monitor = input(f"🔄 Monitorar automaticamente? (s/n, padrão: {'s' if current_auto.lower() == 'true' else 'n'}): ").strip().lower()
    if not auto_monitor:
        auto_monitor = "s" if current_auto.lower() == "true" else "n"
    auto_monitor = "true" if auto_monitor in ["s", "sim", "y", "yes", "true"] else "false"
    
    # Salvar configurações
    print("\n💾 Salvando configurações...")
    
    configs = {
        "INPUT_FOLDER_PATH": input_folder,
        "OUTPUT_FOLDER_PATH": output_folder,
        "WHISPER_MODEL": model,
        "WHISPER_LANGUAGE": language,
        "AUTO_MONITOR": auto_monitor,
        "MONITOR_INTERVAL": "30",
        "SUPPORTED_FORMATS": "mp4,avi,mov,mkv,wmv,flv,webm,m4v",
        "MAX_FILE_SIZE_MB": "500",
        "CONCURRENT_VIDEOS": "1",
        "OUTPUT_FORMAT": "txt",
        "INCLUDE_TIMESTAMPS": "false",
        "CREATE_DATE_FOLDERS": "true",
        "PROCESS_EXISTING_FILES": "true",
        "LOG_LEVEL": "INFO",
        "LOG_TO_FILE": "true"
    }
    
    for key, value in configs.items():
        set_key(".env", key, value)
    
    print("✅ Configurações salvas!")
    
    return input_folder, output_folder, model, language, auto_monitor

def show_summary(input_folder, output_folder, model, language, auto_monitor):
    """Mostra um resumo da configuração."""
    print("\n" + "🎯" + "=" * 50 + "🎯")
    print("           CONFIGURAÇÃO CONCLUÍDA!")
    print("🎯" + "=" * 50 + "🎯")
    print()
    print(f"📁 Pasta dos vídeos:     {input_folder}")
    print(f"📁 Pasta de saída:       {output_folder}")
    print(f"🎤 Modelo Whisper:       {model}")
    print(f"🌍 Idioma:               {language}")
    print(f"🔄 Monitoramento auto:   {'Sim' if auto_monitor == 'true' else 'Não'}")
    print()
    print("🚀 COMO USAR:")
    print("   python run.py                    # Usar configurações salvas")
    print(f'   python run.py "{input_folder}"   # Pasta específica')
    print()
    print("📋 COMANDOS ÚTEIS:")
    print("   python run.py --help            # Ver todas as opções")
    print("   python teste_rapido.py          # Testar se tudo está OK")
    print()

def main():
    """Função principal."""
    clear_screen()
    print_header()
    
    try:
        # Verificar se estamos na pasta correta
        if not Path("src/main.py").exists():
            print("❌ Erro: Execute este script na pasta raiz do projeto!")
            print("   (onde está o arquivo src/main.py)")
            sys.exit(1)
        
        # Configurar
        input_folder, output_folder, model, language, auto_monitor = configure_env()
        
        # Mostrar resumo
        show_summary(input_folder, output_folder, model, language, auto_monitor)
        
        # Perguntar se quer testar
        print("🧪 Quer testar se tudo está funcionando?")
        test = input("   Digite 's' para testar agora: ").strip().lower()
        
        if test in ["s", "sim", "y", "yes"]:
            print("\n🔄 Executando teste...")
            os.system("python teste_rapido.py")
        
        print("\n✨ Pronto! Seu sistema está configurado e pronto para usar!")
        
    except KeyboardInterrupt:
        print("\n\n❌ Configuração cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante a configuração: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()