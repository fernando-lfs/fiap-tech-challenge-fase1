# 📘 Visão Geral do Projeto

Vitibrasil API é uma API REST desenvolvida em Python com FastAPI para raspagem automática de dados públicos do portal Vitibrasil/Embrapa(http://vitibrasil.cnpuv.embrapa.br/index.php). O sistema implementa fallback local (CSV/JSON) e autenticação JWT, garantindo alta disponibilidade e segurança. O objetivo é facilitar o acesso estruturado a dados de produção, processamento, comercialização, importação e exportação do setor vitivinícola brasileiro diretamente da fonte oficial.

---

## 📁 Estrutura do Projeto

```
vitibrasil_api/
├── app/
│   ├── adapters/       # Scraping e fallback local
│   ├── core/           # Configurações e segurança
│   ├── models/         # Schemas Pydantic
│   ├── routers/        # Rotas da API
│   └── services/       # Lógica de negócio
├── data/               # Backups locais (CSV/JSON)
├── tests/             # Testes automatizados
└── README.md
```

---

## 📦 Tecnologias & Ferramentas Utilizadas

- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI
- **Gerenciador de ambiente:** pyenv
- **Gerenciador de dependências:** Poetry
- **Servidor ASGI:** Uvicorn
- **Scraping:** requests, beautifulsoup4
- **Autenticação:** JWT (via PyJWT)
- **Validação de dados:** Pydantic
- **Logs:** logging (arquivo/console)
- **Testes:** pytest

---

## ⚙️ Pré-requisitos

- Python 3.10 ou superior (recomendado instalar via [pyenv](https://github.com/pyenv/pyenv))
- Poetry (`pip install poetry`)
- Git

---

## 🚀 Instalação & Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/fernando-lfs/fiap-tech-challenge-fase1.git
   cd fiap-tech-challenge-fase1
   ```
2. **Configure o Python local:**
   ```bash
   pyenv install 3.10.0
   pyenv local 3.10.0
   ```
3. **Instale as dependências:**
   ```bash
   poetry install
   ```
4. **Configure variáveis de ambiente:**
   - Copie o arquivo `.env.example` para `.env` e ajuste as variáveis conforme necessário (exemplo de variáveis: `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`).
5. **(Opcional) Atualize backups locais:**
   - Certifique-se de que os arquivos de backup estejam em `/data` (formatos CSV ou JSON).

---

## 📝 Uso & Exemplos

### Iniciando a API

```bash
poetry run uvicorn app.main:app --reload
```

Acesse a documentação automática em [http://localhost:8000/docs](http://localhost:8000/docs) ou [http://localhost:8000/redoc](http://localhost:8000/redoc).

### Endpoints Principais (JWT obrigatório)

- `POST /v1/auth/cadastro` — Cadastro de usuário
- `POST /v1/auth/login` — Login e geração de token JWT
- `GET /v1/producao` — Dados de produção
- `GET /v1/processamento` — Dados de processamento
- `GET /v1/comercializacao` — Dados de comercialização
- `GET /v1/importacao` — Dados de importação
- `GET /v1/exportacao` — Dados de exportação

#### Exemplo: Login e uso do JWT

1. **Obter token:**
   ```bash
   curl -X POST http://localhost:8000/v1/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
   ```
   Resposta:
   ```json
   {
     "access_token": "<TOKEN>",
     "token_type": "bearer"
   }
   ```
2. **Acessar endpoint protegido:**
   ```bash
   curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/v1/producao
   ```

#### Estrutura da Resposta

```json
{
  "fonte": "online" | "local",
  "timestamp": "2025-05-31T10:20:37Z",
  "dados": [ ... ]
}
```

#### Testes

```bash
poetry run pytest
```

---

## 🛠️ Deploy em Nuvem

1. **Heroku/Render/AWS:**
   - Crie um app na plataforma desejada.
   - Defina variáveis de ambiente conforme o arquivo `.env` local.
   - Configure buildpacks para Python 3.10+.
   - Comando de inicialização:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
2. **Backup e logs:**
   - Garanta persistência para `/data` (backups) e `/logs`.
3. **Acesso:**
   - Acesse via `https://<seu-app>.herokuapp.com/docs` ou domínio da nuvem escolhida.

---

## 📚 Referências & Recursos Adicionais

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Vitibrasil/Embrapa](http://vitibrasil.cnpuv.embrapa.br/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Repositório no GitHub](https://github.com/fernando-lfs/fiap-tech-challenge-fase1)

---

## ⚖️ Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## ✉️ Contato / Autor

- Fernando LFS — [GitHub](https://github.com/fernando-lfs) | [LinkedIn](https://www.linkedin.com/in/fernando-lfs/)

---

> Projeto desenvolvido para o FIAP Tech Challenge — Fase 1.
