# --- SCRIPT PARA PROCESSAR CSV E EXTRAIR COR/OBJETIVO DA DESCRIÇÃO ---

import pandas as pd
import os
import re
import datetime

# --- Configurações ---
# !! IMPORTANTE: Certifique-se de que o nome do arquivo de entrada está correto !!
CAMINHO_BASE = r"C:\Users\morae\desktop\scrapping" # Adapte se necessário
NOME_ARQUIVO_ENTRADA = "produtos_artwalk_v31_1340p.csv" # O SEU ARQUIVO GERADO
NOME_ARQUIVO_SAIDA = "produtos_artwalk_v31_1340p_processado.csv" # Novo arquivo de saída

CAMINHO_CSV_ENTRADA = os.path.join(CAMINHO_BASE, NOME_ARQUIVO_ENTRADA)
CAMINHO_CSV_SAIDA = os.path.join(CAMINHO_BASE, NOME_ARQUIVO_SAIDA)

# Colunas relevantes
COLUNA_DESCRICAO = "descricao"
COLUNA_COR = "cor"
COLUNA_OBJETIVO = "objetivo"

# --- Listas de Palavras-Chave (Reutilizadas do Scraper) ---
# (Considere refinar estas listas se os resultados não forem precisos)
CORES_PALAVRAS_CHAVE = [
    "branco", "preto", "azul", "vermelho", "verde", "cinza", "rosa",
    "amarelo", "laranja", "marrom", "bege", "dourado", "prata", "roxo",
    "vinho", "creme", "turquesa", "grafite", "multicolor", "off-white", "bordo",
    "marinho", "oliva", "caqui", "salmão", "lilás", "coral", "ciano", "magenta",
    "índigo", "violeta", "lavanda", "esmeralda", "rubi", "âmbar", "caramelo",
    "areia", "chumbo", "terracota", "ocre", "bordô" # Adicionadas mais cores
]
OBJETIVOS_PALAVRAS_CHAVE = [
    "corrida", "caminhada", "treino", "academia", "fitness", "esportivo", "performance", # Atividade Física
    "basquete", "skate", "volei", "tennis", "futebol", # Esportes Específicos
    "casual", "dia a dia", "passeio", "urbano", "trabalho", # Uso Diário / Casual
    "estilo", "moda", "streetwear", "lifestyle", # Estilo / Moda
    "aventura", "trilha", "outdoor" # Aventura
]

# --- Funções de Extração ---

def extrair_cor_da_descricao(descricao):
    """Tenta encontrar a primeira cor mencionada na descrição."""
    if pd.isna(descricao) or not isinstance(descricao, str) or not descricao.strip():
        return "Não informado"

    desc_lower = descricao.lower()
    # Itera pelas cores, dando prioridade às primeiras encontradas na lista
    for cor in CORES_PALAVRAS_CHAVE:
        # Usar word boundaries (\b) para evitar substrings (ex: 'rosa' em 'prosa')
        # Usar re.escape para tratar caracteres especiais se houver (improvável aqui)
        if re.search(r'\b' + re.escape(cor) + r'\b', desc_lower):
            # Casos especiais de capitalização se necessário
            if cor == "off-white": return "Off-White"
            return cor.capitalize()
    return "Não informado"

def extrair_objetivo_da_descricao(descricao):
    """Tenta encontrar o primeiro objetivo/uso mencionado na descrição."""
    if pd.isna(descricao) or not isinstance(descricao, str) or not descricao.strip():
        return "Não informado"

    desc_lower = descricao.lower()
    objetivos_encontrados = []

    # Verifica palavras-chave principais
    for objetivo in OBJETIVOS_PALAVRAS_CHAVE:
        if re.search(r'\b' + re.escape(objetivo) + r'\b', desc_lower):
            # Tratamento especial para "dia a dia"
            if objetivo == "dia a dia":
                objetivos_encontrados.append("Dia a Dia")
            else:
                objetivos_encontrados.append(objetivo.capitalize())

    # Se encontrou algum, retorna o primeiro (ou pode juntar se preferir)
    if objetivos_encontrados:
        # Pode retornar o primeiro encontrado ou uma lista:
        # return objetivos_encontrados[0]
        return " / ".join(list(dict.fromkeys(objetivos_encontrados[:2]))) # Pega os 2 primeiros únicos

    # Fallback para termos mais genéricos se nenhum primário for encontrado
    if "estilo" in desc_lower or "moda" in desc_lower or "streetwear" in desc_lower:
        return "Estilo / Moda"
    if "conforto" in desc_lower or "casual" in desc_lower or "passeio" in desc_lower:
        return "Casual / Conforto"
    if "trilha" in desc_lower or "aventura" in desc_lower or "outdoor" in desc_lower:
         return "Aventura / Trilha"

    return "Não informado"

# --- Processamento Principal ---
print(f"--- Iniciando Processamento do Arquivo: {NOME_ARQUIVO_ENTRADA} ---")

try:
    # 1. Ler o arquivo CSV de entrada
    print(f"1. Lendo CSV de entrada: {CAMINHO_CSV_ENTRADA}...")
    # Detectar o separador correto (assumindo que seja ';')
    df = pd.read_csv(CAMINHO_CSV_ENTRADA, sep=';', encoding='utf-8')
    print(f"   -> Leitura concluída. {len(df)} linhas encontradas.")

    # 2. Verificar se as colunas necessárias existem
    if COLUNA_DESCRICAO not in df.columns:
        raise ValueError(f"Coluna '{COLUNA_DESCRICAO}' não encontrada no arquivo CSV.")
    if COLUNA_COR not in df.columns:
        print(f"   (Aviso) Coluna '{COLUNA_COR}' não encontrada. Criando coluna...")
        df[COLUNA_COR] = "Não informado"
    if COLUNA_OBJETIVO not in df.columns:
        print(f"   (Aviso) Coluna '{COLUNA_OBJETIVO}' não encontrada. Criando coluna...")
        df[COLUNA_OBJETIVO] = "Não informado"

    # 3. Aplicar as funções de extração para preencher as colunas
    print(f"2. Processando coluna '{COLUNA_DESCRICAO}' para extrair Cor e Objetivo...")

    # Usar .apply() para eficiência
    df[COLUNA_COR] = df[COLUNA_DESCRICAO].apply(extrair_cor_da_descricao)
    df[COLUNA_OBJETIVO] = df[COLUNA_DESCRICAO].apply(extrair_objetivo_da_descricao)

    print("   -> Processamento concluído.")

    # 4. Salvar o DataFrame atualizado em um novo arquivo CSV
    print(f"3. Salvando resultados em: {CAMINHO_CSV_SAIDA}...")
    # Usa sep=';' e encoding='utf-8-sig' para compatibilidade com Excel
    df.to_csv(CAMINHO_CSV_SAIDA, sep=';', encoding='utf-8-sig', index=False)
    print(f"   -> Arquivo salvo com sucesso!")

except FileNotFoundError:
    print(f"ERRO: Arquivo de entrada não encontrado em: {CAMINHO_CSV_ENTRADA}")
except ValueError as ve:
    print(f"ERRO: {ve}")
except Exception as e:
    print(f"ERRO INESPERADO durante o processamento: {e}")
    traceback.print_exc()

print("\n--- Processamento Finalizado ---")