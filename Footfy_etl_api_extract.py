import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, String
from sqlalchemy.dialects.oracle import FLOAT as ORACLE_FLOAT, CLOB
import oracledb

oracledb.init_oracle_client()


##INSIRA AQUI OS DADOS DE CONEXAO COM O BANCO DE DADOS
usuario = 'rm559344'
senha = 'fiap24'
host = 'oracle.fiap.com.br'
porta = '1521'
service_name = 'orcl'
table_name = 'TBL_SHOES_COMPARISON'

str_conexao = f'oracle+oracledb://{usuario}:{senha}@{host}:{porta}/?service_name={service_name}'
engine = create_engine(str_conexao)

dataset_name = 'mariyamalshatta/nike-vs-addidas-unspervised-clustering'
output_dir = 'datasets/nike_vs_adidas'
os.makedirs(output_dir, exist_ok=True)

print("Arquivos encontrados:", os.listdir(output_dir))

api = KaggleApi()
api.authenticate()
api.dataset_download_files(dataset_name, path=output_dir, unzip=True)

csv_file_name = next((f for f in os.listdir(output_dir) if f.endswith(".csv")), None)
if not csv_file_name:
    raise FileNotFoundError("Nenhum arquivo CSV encontrado na pasta de download.")

csv_path = os.path.join(output_dir, csv_file_name)
print(f"Lendo arquivo CSV: {csv_file_name}")
df = pd.read_csv(csv_path)

df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

dtypes_oracle = {}
for col in df.columns:
    if pd.api.types.is_integer_dtype(df[col]):
        dtypes_oracle[col] = Integer()
    elif pd.api.types.is_float_dtype(df[col]):
        dtypes_oracle[col] = ORACLE_FLOAT(binary_precision=53)
    elif pd.api.types.is_string_dtype(df[col]):
        max_len = df[col].astype(str).map(len).max()
        if max_len > 4000:
            dtypes_oracle[col] = String().with_variant(CLOB(), "oracle")
        else:
            dtypes_oracle[col] = String(int(min(max_len * 1.5, 4000)))

columns_sql = []
for col, dtype in dtypes_oracle.items():
    if isinstance(dtype, Integer):
        col_type = "NUMBER"
    elif isinstance(dtype, ORACLE_FLOAT):
        col_type = "FLOAT"
    elif isinstance(dtype, String) and hasattr(dtype, "impl") and isinstance(dtype.impl, CLOB):
        col_type = "CLOB"
    elif isinstance(dtype, String):
        col_type = f"VARCHAR2({dtype.length})"
    else:
        col_type = "VARCHAR2(1000)"  # fallback
    columns_sql.append(f"{col} {col_type}")

sql_create = f"""
BEGIN
   EXECUTE IMMEDIATE '
   CREATE TABLE {table_name} (
       {', '.join(columns_sql)}
   )';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -955 THEN
         RAISE;
      END IF;
END;
"""

with engine.connect() as conn:
    conn.execute(text(sql_create))
    print(f"Tabela '{table_name}' verificada/criada com sucesso.")

try:
    df.to_sql(
        table_name,
        con=engine,
        if_exists='append',
        index=False,
        dtype=dtypes_oracle
    )
    print(f"Dados inseridos com sucesso na tabela '{table_name}'!")
except Exception as e:
    print(f"Erro ao inserir dados: {e}")
