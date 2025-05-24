# Vitibrasil API

API REST em Python (FastAPI) para raspagem de dados do Vitibrasil/Embrapa com fallback local e autenticação JWT.

## Instalação

1. Instale Python 3.10+ usando [pyenv](https://github.com/pyenv/pyenv).
2. Instale o Poetry: `pip install poetry`
3. Clone o repositório e instale as dependências:
   ```bash
   poetry install
   ```
4. Configure variáveis no `.env` (já fornecido).

## Execução

```bash
poetry run uvicorn app.main:app --reload
```

## Endpoints

- `GET /v1/producao`
- `GET /v1/processamento`
- `GET /v1/comercializacao`
- `GET /v1/importacao`
- `GET /v1/exportacao`

Todos protegidos por JWT. Gere um token via endpoint de autenticação (exemplo será adicionado).

## Estrutura da Resposta

```json
{
  "fonte": "online" | "local",
  "timestamp": "YYYY-MM-DDThh:mm:ssZ",
  "dados": [ ... ]
}
```

## Backup Local

- Arquivos de backup devem estar em `/data` (CSV ou JSON).

## Logs

- Logs em `/logs/app.log`.

## Testes

```bash
poetry run pytest
```

---

Documentação automática disponível em `/docs` e `/redoc`.
