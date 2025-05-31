# Usa uma imagem base leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências primeiro para aproveitar o cache do Docker
COPY pyproject.toml poetry.lock ./

# Instala o Poetry e as dependências do projeto
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta que será usada pela aplicação
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
