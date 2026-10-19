# 📌 Arquitetura da Solução

O projeto foi estruturado em Python utilizando **Playwright** para a automação web e **FastAPI** para a disponibilização da API REST com documentação OpenAPI/Swagger.
---

## ⚙️ Tecnologias e Decisões Técnicas

* **Python 3.10+**
* **Playwright**: Escolhido por oferecer excelente desempenho na execução assíncrona, gestão eficiente de contextos de navegação em modo *headless* e suporte nativo robusto a seletores CSS/XPath.
* **FastAPI**: Utilizado pela alta performance, suporte nativo a operações assíncronas (`async/await`) e geração automática da documentação Swagger UI.
* **Uvicorn**: Servidor ASGI leve para execução da API.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.10 ou superior instalado.
* `pip` e `venv` configurados.

### 1. Clonar o repositório e criar o ambiente virtual
```bash
# Entrar na pasta do projeto
cd desafio-mostqi

# Criar ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual (macOS/Linux)
source venv/bin/activate

# No Windows (Command Prompt):
# venv\Scripts\activate


##Instalar as dependências
pip install -r requirements.txt
playwright install

##Iniciar o servidor da API
uvicorn main:app --reload

A API estará a rodar em http://127.0.0.1:8000.
