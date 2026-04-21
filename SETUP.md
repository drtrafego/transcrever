# 🚀 GUIA DE INSTALAÇÃO E CONFIGURAÇÃO

## 📋 PRÉ-REQUISITOS

### Sistema Operacional
- **Windows 10/11** (recomendado)
- **Linux Ubuntu 20.04+** ou **macOS 12+**
- **RAM**: Mínimo 8GB (16GB recomendado)
- **Storage**: 50GB livres (para cache de vídeos)
- **CPU**: 4+ cores (8+ recomendado)

### Software Necessário
```bash
# Essenciais
✅ Python 3.9+ (3.11 recomendado)
✅ Git 2.30+
✅ FFmpeg 4.4+
✅ Redis 6.0+ (ou Docker)

# Opcionais (para performance)
🔧 CUDA 11.8+ (para GPU acceleration)
🔧 Docker Desktop (para containerização)
🔧 PostgreSQL 14+ (alternativa ao SQLite)
```

## 🔧 INSTALAÇÃO PASSO A PASSO

### 1. Preparação do Ambiente

#### Windows
```powershell
# Instalar Python via Microsoft Store ou python.org
# Verificar instalação
python --version
pip --version

# Instalar FFmpeg via Chocolatey
choco install ffmpeg

# Ou baixar manualmente de: https://ffmpeg.org/download.html
```

#### Linux (Ubuntu/Debian)
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3.11 python3.11-venv python3-pip git ffmpeg redis-server

# Verificar instalações
python3.11 --version
ffmpeg -version
redis-cli ping
```

#### macOS
```bash
# Instalar Homebrew se necessário
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependências
brew install python@3.11 git ffmpeg redis

# Iniciar Redis
brew services start redis
```

### 2. Clone e Setup do Projeto

```bash
# Clone do repositório
git clone https://github.com/seu-usuario/transcrever-videos.git
cd transcrever-videos

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configuração do Google Drive API

#### 3.1 Criar Projeto no Google Cloud Console
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione existente
3. Ative a **Google Drive API**
4. Vá em **Credenciais** → **Criar Credenciais** → **ID do cliente OAuth 2.0**
5. Configure como **Aplicativo de desktop**
6. Baixe o arquivo JSON das credenciais

#### 3.2 Configurar Credenciais
```bash
# Copiar arquivo de credenciais
cp ~/Downloads/credentials.json config/drive_credentials.json

# Executar setup inicial
python scripts/setup.py --configure-drive
```

#### 3.3 Obter ID da Pasta do Drive
```bash
# Método 1: Via URL do Drive
# URL: https://drive.google.com/drive/folders/1ABC123XYZ789
# ID: 1ABC123XYZ789

# Método 2: Via script
python scripts/get_folder_id.py --folder-name "Meus Videos"
```

### 4. Configuração do Whisper

#### 4.1 Instalação Básica (CPU)
```bash
# Whisper já incluído no requirements.txt
# Testar instalação
python -c "import whisper; print('Whisper OK')"
```

#### 4.2 Configuração GPU (Opcional)
```bash
# Para NVIDIA GPUs com CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verificar CUDA
python -c "import torch; print(f'CUDA disponível: {torch.cuda.is_available()}')"
```

#### 4.3 Download de Modelos
```bash
# Download automático dos modelos Whisper
python scripts/download_models.py --models tiny,base,small

# Ou download manual
python -c "import whisper; whisper.load_model('base')"
```

### 5. Configuração do Banco de Dados

#### 5.1 SQLite (Padrão - Desenvolvimento)
```bash
# Criar banco e tabelas
python scripts/init_database.py --db-type sqlite

# Verificar criação
ls -la data/database.sqlite
```

#### 5.2 PostgreSQL (Produção)
```bash
# Instalar PostgreSQL
# Windows: https://www.postgresql.org/download/windows/
# Linux: sudo apt install postgresql postgresql-contrib
# macOS: brew install postgresql

# Criar banco
createdb transcrever_videos

# Configurar connection string
export DATABASE_URL="postgresql://user:password@localhost/transcrever_videos"

# Inicializar banco
python scripts/init_database.py --db-type postgresql
```

### 6. Configuração do Redis

#### 6.1 Instalação Local
```bash
# Windows (via Chocolatey)
choco install redis-64

# Linux
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis

# macOS
brew install redis
brew services start redis
```

#### 6.2 Configuração Docker (Alternativa)
```bash
# Executar Redis via Docker
docker run -d --name redis-transcription -p 6379:6379 redis:7-alpine

# Verificar funcionamento
docker exec redis-transcription redis-cli ping
```

### 7. Configuração de Ambiente

#### 7.1 Arquivo de Configuração Principal
```bash
# Copiar template de configuração
cp config/settings.template.yaml config/settings.yaml

# Editar configurações
nano config/settings.yaml  # ou seu editor preferido
```

#### 7.2 Variáveis de Ambiente
```bash
# Criar arquivo .env
cat > .env << EOF
# Database
DATABASE_URL=sqlite:///data/database.sqlite
REDIS_URL=redis://localhost:6379/0

# Google Drive
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here

# Whisper
WHISPER_MODEL=base
WHISPER_DEVICE=cpu

# Logging
LOG_LEVEL=INFO
LOG_FILE=data/logs/app.log

# Workers
CELERY_WORKERS=2
CELERY_CONCURRENCY=4
EOF
```

## ⚙️ CONFIGURAÇÕES DETALHADAS

### 1. Configuração do Whisper
```yaml
# config/whisper_config.yaml
whisper:
  model: "base"  # tiny, base, small, medium, large
  device: "cpu"  # cpu, cuda
  language: "pt"  # auto, pt, en, es, etc.
  
  # Configurações avançadas
  fp16: false  # Half precision (GPU only)
  temperature: 0.0  # Sampling temperature
  compression_ratio_threshold: 2.4
  logprob_threshold: -1.0
  no_speech_threshold: 0.6
  
  # Processamento em chunks
  chunk_length: 30  # segundos
  overlap: 5  # segundos de sobreposição
```

### 2. Configuração de Performance
```yaml
# config/performance.yaml
processing:
  max_workers: 4
  max_concurrent_downloads: 2
  chunk_size_mb: 100
  
  # Timeouts
  download_timeout: 1800  # 30 minutos
  transcription_timeout: 3600  # 1 hora
  
  # Retry policy
  max_retries: 3
  retry_delay: 60  # segundos
  exponential_backoff: true

cache:
  max_size_gb: 10
  cleanup_interval: 3600  # 1 hora
  ttl_hours: 24
```

### 3. Configuração de Monitoramento
```yaml
# config/monitoring.yaml
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "data/logs/app.log"
  max_size_mb: 100
  backup_count: 5

metrics:
  enabled: true
  port: 9090
  path: "/metrics"
  
dashboard:
  enabled: true
  port: 8080
  auth_required: false
```

## 🧪 VERIFICAÇÃO DA INSTALAÇÃO

### 1. Testes Básicos
```bash
# Testar importações Python
python scripts/test_imports.py

# Testar conectividade Google Drive
python scripts/test_drive_connection.py

# Testar Whisper
python scripts/test_whisper.py --model tiny

# Testar Redis
python scripts/test_redis.py

# Testar banco de dados
python scripts/test_database.py
```

### 2. Teste End-to-End
```bash
# Executar teste completo com vídeo de exemplo
python scripts/test_full_pipeline.py --test-video data/samples/test.mp4
```

### 3. Health Check
```bash
# Verificar saúde do sistema
python src/health_check.py --all

# Saída esperada:
# ✅ Python environment: OK
# ✅ Dependencies: OK
# ✅ Google Drive API: OK
# ✅ Whisper models: OK
# ✅ Redis connection: OK
# ✅ Database: OK
# ✅ FFmpeg: OK
```

## 🚀 PRIMEIRA EXECUÇÃO

### 1. Modo Desenvolvimento
```bash
# Iniciar em modo debug
python src/main.py --dev-mode --log-level DEBUG

# Em outro terminal, iniciar worker
celery -A src.workers.main worker --loglevel=info
```

### 2. Modo Produção
```bash
# Iniciar todos os serviços
python scripts/start_production.py

# Ou manualmente:
# Terminal 1: API
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Workers
celery -A src.workers.main worker --loglevel=info --concurrency=4

# Terminal 3: Monitor
celery -A src.workers.main flower --port=5555
```

### 3. Acessar Dashboard
```bash
# Abrir no navegador
http://localhost:8080  # Dashboard principal
http://localhost:5555  # Celery Flower (monitoramento)
```

## 🔧 TROUBLESHOOTING

### Problemas Comuns

#### 1. Erro de Importação do Whisper
```bash
# Problema: ModuleNotFoundError: No module named 'whisper'
# Solução:
pip install --upgrade openai-whisper
```

#### 2. Erro de Conexão com Google Drive
```bash
# Problema: google.auth.exceptions.RefreshError
# Solução:
rm config/token.json  # Remove token expirado
python scripts/setup.py --configure-drive  # Reautentica
```

#### 3. FFmpeg não encontrado
```bash
# Windows:
# Baixar de https://ffmpeg.org/download.html
# Adicionar ao PATH do sistema

# Linux:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg
```

#### 4. Redis Connection Error
```bash
# Verificar se Redis está rodando
redis-cli ping

# Se não estiver:
# Windows: net start redis
# Linux: sudo systemctl start redis
# macOS: brew services start redis
```

#### 5. Problemas de Permissão
```bash
# Linux/macOS - ajustar permissões
chmod +x scripts/*.py
sudo chown -R $USER:$USER data/
```

## 📚 PRÓXIMOS PASSOS

Após a instalação bem-sucedida:

1. **Configurar pasta do Drive**: Definir pasta específica para monitoramento
2. **Testar com vídeo pequeno**: Validar pipeline completo
3. **Configurar notificações**: Setup de alertas para falhas
4. **Otimizar performance**: Ajustar workers conforme hardware
5. **Setup backup**: Configurar backup automático dos resultados

---

**🎉 Instalação concluída! O sistema está pronto para transcrever seus vídeos.**

Para dúvidas, consulte a [documentação completa](README.md) ou abra uma [issue no GitHub](https://github.com/seu-usuario/transcrever-videos/issues).