from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from sqlalchemy import create_engine, text
import uvicorn
import re
from datetime import datetime
import os

# --------- Conexão com banco PostgreSQL ---------
engine = create_engine("postgresql://footify:Footify123@postgres_db:5432/footifydb")
#engine = create_engine("postgresql://footify:Footify123@localhost:5432/footifydb")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai_client = genai.Client(api_key="COLOQUE SUA API KEY AQUI")
usuarios = {}

class UserRequest(BaseModel):
    user_id: str
    mensagem: str


# --------- Contexto de produtos ---------
def gerar_contexto_tenis():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT nome_produto, preco_atual, cor, objetivo, url_site, loja, categoria, genero_destinado FROM produtos"))
        categorias_organizadas = {}
        for row in result:
            modalidade = row.objetivo or "Outros"
            if modalidade not in categorias_organizadas:
                categorias_organizadas[modalidade] = []
            categorias_organizadas[modalidade].append(
                f"👟 **{row.nome_produto}** ({row.loja})\n"
                f"💰 Preço: R$ {row.preco_atual / 100:.2f} | 🎨 {row.cor or 'Cor não informada'}\n"
                f"🔗 [Ver produto]({row.url_site})"
            )

    contexto = "📦 Aqui estão os tênis disponíveis. Use **somente** esses produtos nas suas respostas:\n\n"
    for modalidade, produtos in categorias_organizadas.items():
        contexto += f"🏷️ **{modalidade.upper()}**\n\n"
        for p in produtos[:3]:
            contexto += p + "\n\n"
        contexto += f"👉 _Para ver mais opções de **{modalidade.lower()}**, diga: 'ver mais {modalidade.lower()}'_\n\n---\n\n"
    return contexto

# --------- Contexto do sistema ---------
def gerar_contexto_sistema(nome=None, genero=None):
    base = (
        "você não sabe matematica, somente sabe sobre calçados.\n"
        "Você é um assistente simpático e especializado em calçados.\n"
        "Seu nome é Footify, uma IA que sabe tudo sobre calçados, e você trabalha na Footify, uma loja de calçados.\n"
        "Se o cliente perguntar para que time você torce, diga que torce para o corinthians e que o palmeiras não tem mundial.\n"
        "Seu objetivo é ajudar o cliente a encontrar o calçado ideal.\n"
        "Você deve fazer perguntas para entender o que o cliente procura.\n"
        "Se o cliente não souber o que quer, faça sugestões com base nos produtos disponíveis.\n"
        "Se o cliente desviar do assunto, traga a conversa de volta para calçados.\n"
        "Se o cliente usar palavras ofensivas, responda de forma educada e firme, pedindo respeito.\n"
        "Sugira calçados com base no que o cliente procura (conforto, corrida, estilo, etc.).\n"
        "Use apenas os produtos listados no contexto. Não invente modelos ou marcas.\n"
        "Mostre o nome, preço, cor, objetivo e link do produto.\n"
    )
    if nome:
        base += f"O nome do cliente é {nome}.\n"
    if genero:
        base += f"O cliente está buscando calçados do gênero {genero}.\n"
    return base

# --------- Filtro de ofensas ---------
palavras_proibidas = [
    "pinto", "buceta", "rola", "pau", "caralho", "viado", "bosta", "merda",
    "gostoso", "gostosa", "puta", "boquete", "punheta", "xereca", "cu",
    "foda", "porra", "cacete", "bucetuda", "arrombado", "babaca", "escroto",
    "vagabunda", "cornão", "otário", "fdp", "desgraçado", "nojento", "sexo", "sexual", "sex", "transa", "transar", "bunda"
]

def contem_ofensa(texto: str) -> bool:
    texto = texto.lower()
    palavras = re.findall(r'\b\w+\b', texto)
    return any(p in palavras_proibidas for p in palavras)

# --------- Resposta via Gemini ---------
def responder_com_gemini(historico: list, nome=None, genero=None) -> str:
    try:
        contexto_inicial = genai.types.Content(
            role="user",
            parts=[genai.types.Part(text=gerar_contexto_sistema(nome, genero))]
        )
        contexto_tenis = genai.types.Content(
            role="user",
            parts=[genai.types.Part(text=gerar_contexto_tenis())]
        )
        mensagens = [
            genai.types.Content(role=msg["role"], parts=[genai.types.Part(text=msg["text"])])
            for msg in historico
        ]
        mensagens_com_contexto = [contexto_inicial, contexto_tenis] + mensagens
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=mensagens_com_contexto
        )
        return getattr(response, "text", "").strip() or "Desculpe, não consegui gerar uma resposta agora. Pode tentar novamente?"
    except Exception as e:
        print(f"[ERRO] Ao tentar extrair texto: {e}")
        return "Desculpe, houve um erro ao processar a resposta da IA."

# --------- Endpoints FastAPI ---------
@app.post("/perguntar")
async def responder_pergunta(request: UserRequest):
    texto = request.mensagem.strip()
    user_id = request.user_id.strip()

    if user_id not in usuarios:
        usuarios[user_id] = {
            "user_id": user_id,
           # "nome": None,
            "genero": None,
            "historico": []
        }

    estado = usuarios[user_id]

    if contem_ofensa(texto):
        resposta = (
            "⚠️ Vamos manter o respeito, por favor. Estou aqui pra te ajudar com calçados 🙂"
            if not any(p in texto.lower() for p in ["desculpa", "perdão", "foi mal", "me desculpe"])
            else "Tudo certo, sem problemas! Vamos continuar 😄 Me diga: o que você procura em um calçado?"
        )
        estado["historico"].append({"role": "user", "text": texto})
        estado["historico"].append({"role": "model", "text": resposta})
        return {"resposta": resposta}

    
    if not estado["historico"]:
        agora = datetime.now().hour
        if 5 <= agora < 12:
            saudacao = "Bom dia"
        elif 12 <= agora < 18:
            saudacao = "Boa tarde"
        else:
            saudacao = "Boa noite"

        estado["historico"].append({"role": "user", "text": texto})
        resposta = f"{saudacao}! 😊 Bem-vindo à Footify! Qual seu nome, por favor?"
        estado["historico"].append({"role": "model", "text": resposta})
        return {"resposta": resposta}


   # if not estado["nome"] and len(texto.split()) <= 3 and texto.isalpha():
   #     if texto.lower() in ["oi", "olá", "ola", "e aí", "bom dia", "boa tarde", "boa noite", "oii", "oie"]:
   #         resposta = "Prazer! 😊 Qual seu nome, por favor?"
   #     else:
   #         estado["nome"] = texto.title()
   #         resposta = f"Prazer, {estado['nome']}! 😄 Agora me diga: o que você está buscando em um calçado hoje?"
   #     estado["historico"].append({"role": "user", "text": texto})
   #     estado["historico"].append({"role": "model", "text": resposta})
   #     return {"resposta": resposta}

    if not estado["genero"]:
        if "masculino" in texto.lower():
            estado["genero"] = "masculino"
        elif "feminino" in texto.lower():
            estado["genero"] = "feminino"

    estado["historico"].append({"role": "user", "text": texto})
    resposta = responder_com_gemini(estado["historico"], estado["genero"])
    #resposta = responder_com_gemini(estado["historico"], estado["nome"], estado["genero"])
    estado["historico"].append({"role": "model", "text": resposta})
    return {"resposta": resposta}

@app.post("/resetar")
async def resetar_conversa(request: UserRequest):
    user_id = request.user_id.strip()
    usuarios[user_id] = {
        "user_id": user_id,
      #  "nome": None,
        "genero": None,
        "historico": []
        }
    return {"status": f"Conversa reiniciada para {user_id}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)