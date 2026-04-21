# 🤝 GUIA DE CONTRIBUIÇÃO

Obrigado por considerar contribuir com o **Video Transcription Agent**! Este documento fornece diretrizes para contribuições efetivas.

## 📋 ÍNDICE

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Padrões de Código](#padrões-de-código)
- [Processo de Pull Request](#processo-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Funcionalidades](#sugerir-funcionalidades)

## 📜 CÓDIGO DE CONDUTA

### Nossos Compromissos
- **Respeito**: Tratar todos com dignidade e respeito
- **Inclusão**: Ambiente acolhedor para todos os backgrounds
- **Colaboração**: Trabalhar juntos de forma construtiva
- **Profissionalismo**: Manter discussões focadas e produtivas

### Comportamentos Esperados
✅ Usar linguagem acolhedora e inclusiva  
✅ Respeitar diferentes pontos de vista  
✅ Aceitar críticas construtivas graciosamente  
✅ Focar no que é melhor para a comunidade  
✅ Mostrar empatia com outros membros  

### Comportamentos Inaceitáveis
❌ Linguagem ou imagens sexualizadas  
❌ Trolling, comentários insultuosos/depreciativos  
❌ Assédio público ou privado  
❌ Publicar informações privadas sem permissão  
❌ Outras condutas inadequadas em ambiente profissional  

## 🚀 COMO CONTRIBUIR

### Tipos de Contribuição

#### 🐛 Correção de Bugs
- Identifique bugs através de issues ou uso próprio
- Verifique se já não existe issue similar
- Crie issue detalhada se necessário
- Implemente correção seguindo padrões

#### ✨ Novas Funcionalidades
- Discuta a funcionalidade em issue primeiro
- Aguarde aprovação antes de implementar
- Siga arquitetura e padrões existentes
- Inclua testes e documentação

#### 📚 Documentação
- Melhore clareza e completude
- Adicione exemplos práticos
- Corrija erros de digitação
- Traduza para outros idiomas

#### 🧪 Testes
- Aumente cobertura de testes
- Adicione testes de edge cases
- Melhore testes existentes
- Adicione testes de performance

## ⚙️ CONFIGURAÇÃO DO AMBIENTE

### 1. Fork e Clone
```bash
# Fork no GitHub, depois:
git clone https://github.com/SEU-USUARIO/transcrever-videos.git
cd transcrever-videos

# Adicionar upstream
git remote add upstream https://github.com/ORIGINAL-OWNER/transcrever-videos.git
```

### 2. Ambiente de Desenvolvimento
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
pip install -e ".[dev]"  # Dependências de desenvolvimento

# Configurar pre-commit hooks
pre-commit install
```

### 3. Configuração Inicial
```bash
# Copiar configurações de exemplo
cp config/settings.template.yaml config/settings.yaml

# Configurar Google Drive (opcional para desenvolvimento)
python scripts/setup.py --configure-drive

# Executar testes para verificar setup
pytest tests/ -v
```

### 4. Executar em Modo Desenvolvimento
```bash
# Terminal 1: API
python src/main.py --dev-mode

# Terminal 2: Workers (opcional)
celery -A src.workers.main worker --loglevel=debug

# Terminal 3: Redis (se não estiver rodando)
redis-server
```

## 📝 PADRÕES DE CÓDIGO

### Python Style Guide
Seguimos **PEP 8** com algumas adaptações:

```python
# Imports organizados
import os
import sys
from pathlib import Path

import requests
import yaml
from fastapi import FastAPI

from src.core.transcription import TranscriptionEngine
from src.utils.logger import get_logger

# Constantes em UPPER_CASE
MAX_FILE_SIZE = 2048  # MB
DEFAULT_MODEL = "base"

# Classes em PascalCase
class VideoProcessor:
    """Processador de vídeos com documentação clara."""
    
    def __init__(self, config: dict) -> None:
        self.config = config
        self._logger = get_logger(__name__)
    
    def process_video(self, file_path: Path) -> dict:
        """
        Processa um vídeo e retorna metadados.
        
        Args:
            file_path: Caminho para o arquivo de vídeo
            
        Returns:
            Dict com metadados do vídeo processado
            
        Raises:
            VideoProcessingError: Se o processamento falhar
        """
        # Implementação...
        pass

# Funções em snake_case
def validate_video_format(file_path: Path) -> bool:
    """Valida se o formato do vídeo é suportado."""
    supported_formats = [".mp4", ".avi", ".mov"]
    return file_path.suffix.lower() in supported_formats
```

### Configuração de Ferramentas

#### Black (Formatação)
```toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
```

#### isort (Imports)
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

#### mypy (Type Checking)
```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
disallow_untyped_defs = true
```

### Executar Verificações
```bash
# Formatação automática
black src/ tests/
isort src/ tests/

# Verificações
flake8 src/ tests/
mypy src/
pytest tests/ --cov=src --cov-report=html
```

## 🔄 PROCESSO DE PULL REQUEST

### 1. Preparação
```bash
# Atualizar fork
git fetch upstream
git checkout main
git merge upstream/main

# Criar branch para feature
git checkout -b feature/nome-da-funcionalidade
```

### 2. Desenvolvimento
```bash
# Fazer mudanças
# Adicionar testes
# Atualizar documentação

# Commit seguindo padrão
git add .
git commit -m "feat: adicionar funcionalidade X

- Implementa processamento Y
- Adiciona testes para Z
- Atualiza documentação

Closes #123"
```

### 3. Antes do PR
```bash
# Executar todos os testes
pytest tests/ -v --cov=src

# Verificar qualidade do código
black --check src/ tests/
flake8 src/ tests/
mypy src/

# Atualizar com main
git fetch upstream
git rebase upstream/main
```

### 4. Criar Pull Request

#### Template de PR
```markdown
## 📝 Descrição
Breve descrição das mudanças implementadas.

## 🎯 Tipo de Mudança
- [ ] Bug fix (mudança que corrige um problema)
- [ ] Nova funcionalidade (mudança que adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação (mudança apenas na documentação)

## 🧪 Como Testar
1. Passos para reproduzir/testar
2. Comandos específicos
3. Resultados esperados

## ✅ Checklist
- [ ] Código segue padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Mudanças foram testadas localmente
- [ ] Não há conflitos com main

## 📸 Screenshots (se aplicável)
Adicione screenshots para mudanças visuais.

## 🔗 Issues Relacionadas
Closes #123
Related to #456
```

### 5. Review Process
- **Automated Checks**: CI/CD deve passar
- **Code Review**: Pelo menos 1 aprovação
- **Testing**: Testes manuais se necessário
- **Documentation**: Verificar se docs estão atualizadas

## 🐛 REPORTAR BUGS

### Template de Bug Report
```markdown
## 🐛 Descrição do Bug
Descrição clara e concisa do problema.

## 🔄 Passos para Reproduzir
1. Vá para '...'
2. Clique em '...'
3. Execute '...'
4. Veja o erro

## ✅ Comportamento Esperado
O que deveria acontecer.

## ❌ Comportamento Atual
O que está acontecendo.

## 📸 Screenshots
Se aplicável, adicione screenshots.

## 🖥️ Ambiente
- OS: [e.g. Windows 10, Ubuntu 20.04]
- Python: [e.g. 3.9.7]
- Versão do projeto: [e.g. 1.0.0]
- Whisper model: [e.g. base]

## 📋 Logs
```
Cole logs relevantes aqui
```

## 📝 Contexto Adicional
Qualquer outra informação relevante.
```

### Prioridades de Bug
- **🔴 Critical**: Sistema não funciona
- **🟠 High**: Funcionalidade principal quebrada
- **🟡 Medium**: Funcionalidade secundária com problema
- **🟢 Low**: Problema cosmético ou edge case

## ✨ SUGERIR FUNCIONALIDADES

### Template de Feature Request
```markdown
## 🚀 Funcionalidade Solicitada
Descrição clara da funcionalidade desejada.

## 🎯 Problema que Resolve
Qual problema esta funcionalidade resolveria?

## 💡 Solução Proposta
Como você imagina que isso funcionaria?

## 🔄 Alternativas Consideradas
Outras abordagens que você considerou?

## 📈 Benefícios
- Benefício 1
- Benefício 2
- Benefício 3

## 🎨 Mockups/Exemplos
Se aplicável, adicione mockups ou exemplos.

## 📊 Prioridade
- [ ] Must have (essencial)
- [ ] Should have (importante)
- [ ] Could have (desejável)
- [ ] Won't have (não prioritário)
```

## 🏷️ LABELS E MILESTONES

### Labels Principais
- `bug`: Correção de bugs
- `enhancement`: Novas funcionalidades
- `documentation`: Melhorias na documentação
- `good first issue`: Ideal para novos contribuidores
- `help wanted`: Precisa de ajuda da comunidade
- `priority: high/medium/low`: Nível de prioridade
- `status: in-progress`: Em desenvolvimento
- `status: needs-review`: Aguardando review

### Milestones
- **v1.0.0**: Release inicial
- **v1.1.0**: Funcionalidades adicionais
- **v2.0.0**: Breaking changes

## 🎉 RECONHECIMENTO

Contribuidores são reconhecidos através de:
- **Contributors.md**: Lista de todos os contribuidores
- **Release Notes**: Menção em releases
- **GitHub**: Perfil aparece na seção de contribuidores
- **Discord**: Role especial no servidor (se aplicável)

## 📞 SUPORTE

### Canais de Comunicação
- **GitHub Issues**: Para bugs e features
- **GitHub Discussions**: Para dúvidas gerais
- **Email**: dev@transcription.com
- **Discord**: [Link do servidor] (se aplicável)

### Horários de Resposta
- **Issues críticos**: 24 horas
- **Issues normais**: 3-5 dias úteis
- **Pull Requests**: 2-7 dias úteis
- **Discussões**: Melhor esforço

---

**Obrigado por contribuir! Juntos construímos um projeto melhor. 🚀**