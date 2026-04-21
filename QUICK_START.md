# 🚀 GUIA DE INÍCIO RÁPIDO

## ⚡ Execução Simples (3 passos)

### 1️⃣ **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 2️⃣ **Configurar Pasta de Vídeos**
Edite o arquivo `.env` e configure:
```env
INPUT_FOLDER_PATH=C:\Seus Videos Aqui
```

### 3️⃣ **Executar**
```bash
python run.py
```

## 🎯 **Uso Direto (sem configuração)**

```bash
# Transcrever pasta específica
python run.py "C:\Videos"

# Especificar pasta de entrada e saída
python run.py "C:\Videos" "C:\Transcricoes"
```

## 📁 **Resultado**

Os arquivos TXT aparecerão em:
```
data/outputs/
├── 2024-01-15/
│   ├── video1_143052.txt
│   ├── video2_143125.txt
│   └── ...
```

## ⚙️ **Configurações Principais (.env)**

```env
# Pasta com os vídeos
INPUT_FOLDER_PATH=D:\Seus Videos Aqui

# Modelo Whisper (tiny=rápido, large-v3=melhor qualidade)
WHISPER_MODEL=base

# Idioma (pt=português, en=inglês, auto=detectar)
WHISPER_LANGUAGE=pt

# Monitoramento automático
AUTO_MONITOR=true
MONITOR_INTERVAL=30
```

## 🎬 **Formatos Suportados**

✅ MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V

## 🔧 **Solução de Problemas**

### ❌ "Pasta de entrada não configurada"
- Configure `INPUT_FOLDER_PATH` no `.env`
- Ou use: `python run.py "C:\Sua Pasta"`

### ❌ "Modelo Whisper não encontrado"
- Execute: `pip install openai-whisper`
- Aguarde o download do modelo na primeira execução

### ❌ "Erro de memória"
- Use modelo menor: `WHISPER_MODEL=tiny`
- Ou: `WHISPER_MODEL=base`

## 🚀 **Execução Automática**

O sistema pode:
- ✅ Monitorar pasta automaticamente
- ✅ Processar novos vídeos em tempo real
- ✅ Organizar saída por data
- ✅ Incluir timestamp nos nomes

Para parar: **Ctrl+C**

---

**🎯 Objetivo**: Você coloca vídeos numa pasta → Sistema gera arquivos TXT automaticamente!