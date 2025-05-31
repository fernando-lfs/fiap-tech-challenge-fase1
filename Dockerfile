# Usa uma imagem base leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.8.2

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Copia os arquivos de dependências primeiro para aproveitar o cache do Docker
COPY pyproject.toml poetry.lock ./

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi && \
    pip uninstall -y poetry

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta que será usada pela aplicação
EXPOSE 8000

# Cria usuário não-root para rodar a aplicação
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
