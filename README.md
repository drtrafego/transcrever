# 🎥 Video Transcription Agent

Sistema **SUPER SIMPLES** de transcrição de vídeos usando OpenAI Whisper.

## 🚀 USO RÁPIDO (3 passos)

### 1️⃣ Instalar
```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar (automático)
```bash
python configurar.py
```

### 3️⃣ Usar
```bash
python run.py
```

## 💡 AINDA MAIS SIMPLES

Sem configuração, direto:
```bash
python run.py "C:\Sua\Pasta\De\Videos"
```

## 📁 Resultado

Os arquivos TXT aparecerão em:
```
data/outputs/
├── 2024-01-15/
│   ├── video1_143052.txt
│   ├── video2_143125.txt
│   └── ...
```

## ⚙️ Configurações Principais

- **Modelo**: `tiny` (rápido) → `base` (equilibrado) → `large-v3` (máxima qualidade)
- **Idioma**: `pt` (português), `en` (inglês), `auto` (detectar)
- **Formatos**: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V

## 🔧 Comandos Úteis

```bash
python run.py --help                    # Ver opções
python run.py "C:\Videos"               # Pasta específica
python run.py "C:\Videos" "C:\Saida"    # Entrada + saída
python configurar.py                    # Reconfigurar
```

## 🎯 Características

✅ **Zero configuração** - Funciona direto  
✅ **Monitoramento automático** - Detecta novos vídeos  
✅ **Múltiplos formatos** - Todos os principais  
✅ **Organização automática** - Por data  
✅ **Logs detalhados** - Para acompanhar progresso  

## 🐛 Problemas?

1. **FFmpeg não encontrado**: Instale em https://ffmpeg.org/
2. **Modelo não carrega**: Verifique internet (primeira vez)
3. **Vídeo não processa**: Verifique formato e logs em `data/logs/`

**Pronto! Agora é só usar! 🎉**

---

## 🏗️ ARQUITETURA TÉCNICA

### Stack Principal
- **Backend**: Python 3.9+ (processamento principal)
- **AI Engine**: OpenAI Whisper (local/API)
- **Storage**: Google Drive API + Local cache
- **Queue System**: Redis/Celery para processamento assíncrono
- **Database**: SQLite/PostgreSQL para tracking
- **Monitoring**: Logs estruturados + Dashboard web

### Componentes Core
1. **Drive Monitor**: Detecta novos vídeos automaticamente
2. **Video Processor**: Download, conversão e preparação
3. **Transcription Engine**: Interface com Whisper
4. **Output Manager**: Formatação e entrega de resultados
5. **Progress Tracker**: Monitoramento em tempo real

## 🚀 FUNCIONALIDADES

### ✅ Core Features
- [x] Monitoramento automático de pasta do Drive
- [x] Suporte a múltiplos formatos (MP4, AVI, MOV, MKV, etc.)
- [x] Transcrição com timestamps precisos
- [x] Processamento em lote otimizado
- [x] Sistema de retry para falhas
- [x] Cache inteligente para evitar reprocessamento

### 🔄 Processamento
- **Queue System**: Fila inteligente com priorização
- **Parallel Processing**: Múltiplos workers simultâneos
- **Error Handling**: Recovery automático e logs detalhados
- **Progress Tracking**: Status em tempo real de cada vídeo

### 📤 Outputs Suportados
- **TXT**: Texto puro limpo
- **SRT**: Legendas com timestamps
- **VTT**: WebVTT para web
- **JSON**: Dados estruturados com metadados
- **CSV**: Planilha para análise

## 🛠️ TECNOLOGIAS

### Backend & Processing
```
Python 3.9+
├── openai-whisper (AI transcription)
├── google-api-python-client (Drive integration)
├── ffmpeg-python (video processing)
├── celery (async tasks)
├── redis (queue management)
├── sqlalchemy (database ORM)
└── pydantic (data validation)
```

### Monitoring & Web Interface
```
FastAPI (web dashboard)
├── uvicorn (ASGI server)
├── jinja2 (templates)
├── websockets (real-time updates)
└── prometheus (metrics)
```

## 📁 ESTRUTURA DO PROJETO

```
transcrever-videos/
├── 📁 src/
│   ├── 📁 core/
│   │   ├── drive_monitor.py      # Google Drive integration
│   │   ├── video_processor.py    # Video handling & conversion
│   │   ├── transcription.py      # Whisper interface
│   │   └── output_manager.py     # Results formatting
│   ├── 📁 workers/
│   │   ├── transcription_worker.py
│   │   └── cleanup_worker.py
│   ├── 📁 api/
│   │   ├── main.py              # FastAPI app
│   │   ├── routes/
│   │   └── websockets/
│   └── 📁 utils/
│       ├── config.py
│       ├── logger.py
│       └── helpers.py
├── 📁 config/
│   ├── settings.yaml
│   ├── drive_credentials.json
│   └── whisper_config.yaml
├── 📁 data/
│   ├── 📁 cache/               # Temporary video files
│   ├── 📁 outputs/             # Generated transcriptions
│   └── 📁 logs/                # Application logs
├── 📁 scripts/
│   ├── setup.py               # Initial setup
│   ├── deploy.py              # Deployment automation
│   └── backup.py              # Data backup
├── 📁 tests/
├── 📁 docs/
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## ⚡ QUICK START

### 1. Instalação Rápida
```bash
# Clone e setup
git clone <repo-url>
cd transcrever-videos
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup Google Drive API
python scripts/setup.py --configure-drive

# Iniciar processamento
python src/main.py --start-monitoring
```

### 2. Configuração Mínima
```yaml
# config/settings.yaml
drive:
  folder_id: "your-drive-folder-id"
  check_interval: 300  # 5 minutes

whisper:
  model: "base"  # tiny, base, small, medium, large
  language: "pt"  # auto-detect if null

processing:
  max_workers: 2
  chunk_size: 30  # seconds
```

## 🔧 CONFIGURAÇÕES AVANÇADAS

### Performance Tuning
- **GPU Support**: CUDA para Whisper acelerado
- **Memory Management**: Processamento em chunks
- **Concurrent Processing**: Workers paralelos configuráveis
- **Cache Strategy**: Redis para resultados intermediários

### Monitoramento
- **Real-time Dashboard**: Interface web para acompanhamento
- **Logs Estruturados**: JSON logs para análise
- **Metrics**: Prometheus + Grafana integration
- **Alertas**: Notificações para falhas críticas

## 🚀 DEPLOY OPTIONS

### Local Development
```bash
# Desenvolvimento local
python src/main.py --dev-mode
```

### Production (Railway)
```bash
# Deploy automático
railway login
railway init
railway up
```

### Docker
```bash
# Container local
docker-compose up -d
```

## 📊 MONITORAMENTO

### Dashboard Features
- ✅ Status de processamento em tempo real
- ✅ Fila de vídeos pendentes
- ✅ Histórico de transcrições
- ✅ Métricas de performance
- ✅ Logs de erro centralizados

### Métricas Importantes
- **Throughput**: Vídeos processados por hora
- **Accuracy**: Taxa de sucesso das transcrições
- **Latency**: Tempo médio de processamento
- **Resource Usage**: CPU, RAM, Storage

## 🔒 SEGURANÇA & COMPLIANCE

- **API Keys**: Gerenciamento seguro de credenciais
- **Data Privacy**: Processamento local opcional
- **Access Control**: Autenticação para dashboard
- **Audit Trail**: Log completo de todas as operações

## 🤝 CONTRIBUIÇÃO

### Development Workflow
1. Fork do repositório
2. Feature branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Add: nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Pull Request

### Code Standards
- **Python**: PEP 8 + Black formatter
- **Tests**: Pytest com coverage > 80%
- **Docs**: Docstrings obrigatórias
- **Type Hints**: Typing completo

## 📞 SUPORTE

- **Issues**: GitHub Issues para bugs
- **Discussions**: GitHub Discussions para dúvidas
- **Wiki**: Documentação detalhada
- **Email**: suporte@projeto.com

---

**Desenvolvido com ❤️ para automação inteligente de transcrições**

*Última atualização: Janeiro 2024*