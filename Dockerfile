# Video Transcription Agent - Dockerfile
# =====================================

# Multi-stage build para otimização
FROM python:3.11-slim as base

# Metadados
LABEL maintainer="Video Transcription Team <dev@transcription.com>"
LABEL description="Sistema inteligente para transcrição de vídeos com Whisper"
LABEL version="1.0.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN groupadd -r transcription && useradd -r -g transcription transcription

# Diretório de trabalho
WORKDIR /app

# Stage para dependências
FROM base as dependencies

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Stage de desenvolvimento
FROM dependencies as development

# Instalar dependências de desenvolvimento
RUN pip install --no-cache-dir \
    pytest \
    pytest-asyncio \
    pytest-cov \
    black \
    flake8 \
    isort \
    mypy

# Copiar código fonte
COPY . .

# Ajustar permissões
RUN chown -R transcription:transcription /app

# Usuário não-root
USER transcription

# Comando padrão para desenvolvimento
CMD ["python", "src/main.py", "--dev-mode"]

# Stage de produção
FROM dependencies as production

# Copiar apenas arquivos necessários
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY requirements.txt .

# Criar diretórios necessários
RUN mkdir -p data/cache data/outputs data/logs

# Ajustar permissões
RUN chown -R transcription:transcription /app

# Usuário não-root
USER transcription

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ready || exit 1

# Expor portas
EXPOSE 8000 8080

# Comando padrão
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage para GPU (CUDA)
FROM nvidia/cuda:11.8-runtime-ubuntu22.04 as gpu-base

# Instalar Python e dependências
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-pip \
    python3.11-venv \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar symlink para python
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Variáveis de ambiente para GPU
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    CUDA_VISIBLE_DEVICES=0

WORKDIR /app

# Instalar PyTorch com CUDA
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Copiar e instalar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Criar usuário
RUN groupadd -r transcription && useradd -r -g transcription transcription
RUN mkdir -p data/cache data/outputs data/logs
RUN chown -R transcription:transcription /app

USER transcription

# Comando para GPU
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]