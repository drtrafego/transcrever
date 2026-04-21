@echo off
echo 🎥 Video Transcription Agent - Instalacao
echo ==========================================

echo.
echo 📦 Instalando dependencias Python...
pip install -r requirements.txt

echo.
echo 📁 Criando pastas necessarias...
if not exist "data\cache" mkdir "data\cache"
if not exist "data\logs" mkdir "data\logs"
if not exist "data\outputs" mkdir "data\outputs"

echo.
echo ✅ Instalacao concluida!
echo.
echo 📋 Proximos passos:
echo 1. Edite o arquivo .env com suas configuracoes
echo 2. Configure INPUT_FOLDER_PATH com a pasta dos seus videos
echo 3. Execute: python run.py
echo.
pause