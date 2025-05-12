# 👟 Footify – Assistente de IA para Calçados

Footify é um assistente virtual especializado em calçados, desenvolvido com FastAPI no back-end e interface moderna em HTML, CSS e JavaScript. A IA responde de forma personalizada utilizando o modelo Gemini, com base em um banco de dados real de produtos.

---

## 🚀 Tecnologias Utilizadas

### 🧠 Back-End
- [Endpoint FastAPI de pergunta](http://127.0.0.1:5500/perguntar) + Uvicorn 
- [Endpoint FastAPI de reset de sessao](http://127.0.0.1:5500/resetar) + Uvicorn
- [Documentacao Endpoints](http://127.0.0.1:5500/docs) + Uvicorn
- [Google Gemini](https://ai.google.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/) + PostgreSQL
- Armazenamento de sessões por `user_id` (gerado no front)

### 🎨 Front-End
- HTML5, CSS3 (responsivo)
- JavaScript (ES6+)
- Vercel (deploy automático do front)

### 🐳 Infraestrutura
- Aplicação back-end containerizada com **Docker**
- Banco de dados PostgreSQL rodando em container local
- Exposição da API via **Ngrok**

---

## 🌐 Arquitetura

```txt
[ Usuário (navegador) ]
        |
        v
[ Vercel (front-end) ]  -->  [ Ngrok ]  -->  [ FastAPI + Gemini + PostgreSQL (Docker local) ]
```

---

## 🧭 Como executar localmente

### Pré-requisitos:
- Docker e Docker Compose instalados
- Conta no [Ngrok](https://ngrok.com/)
- Conta Google com acesso à API Gemini (e chave configurada)

### 1. Clone o projeto

```bash
Clone o projeto:
------> https://github.com/ryansantosxd/footify.git <------
cd footify
```

### 2. Suba os containers (PostgreSQL e API)

```bash
docker compose -f docker/docker-compose.yml up --build -d
```

### 3. Inicie o Ngrok

```bash
ngrok http 8000
```

Copie o link gerado (`https://xxxxx.ngrok-free.app`) e use-o no front-end.

### 4. Deploy do Front-End

O front-end está hospedado na **Vercel**:  
📍 `https://footify.vercel.app`

Você pode substituir os endpoints em `app.js` com a URL do seu Ngrok.

---

## 📁 Estrutura dos arquivos

```
footify/
├── docker/                 # Compose e configs de Docker
├── backend/                # Código FastAPI (main.py)
├── front/                  # HTML, CSS e JS (Vercel)
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── image/...
└── README.md
```

---

## 🔐 Sessão por usuário

- Cada cliente recebe um `user_id` salvo via `localStorage`.
- Esse `user_id` é enviado nas requisições e vinculado a uma sessão exclusiva no back-end.
- As sessões são mantidas em memória (dicionário Python) e reiniciadas automaticamente ao carregar a página.

---

## 💬 Contato

Projeto acadêmico/desenvolvimento por estudandes de engenharia de dados da FIAP (Richard, Marcio, Grazi, Pedro, Everton).

---
