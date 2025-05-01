import requests
import pandas as pd
import duckdb

# 1. Faz a requisição da API do IntraCTI
url = "https://intracti.com/api/passagens"
response = requests.get(url)
dados = response.json()  # Isso retorna uma lista de dicionários

# 2. Cria um DataFrame com os dados principais
df_principal = pd.json_normalize(dados)

# 3. Trata os comentários (explode em outra tabela, se existirem)
comentarios_exploded = pd.json_normalize(
    dados,
    record_path="comentarios",
    meta=["id"],  # Cria relação com o id da passagem
    errors='ignore'
)

# 4. Conecta com DuckDB
con = duckdb.connect()

# 5. Carrega os DataFrames no DuckDB
con.register("passagens", df_principal)
con.register("comentarios", comentarios_exploded)

# 6. Exemplo de consulta com categorização
resultado = con.execute("""
    SELECT 
        id,
        nome,
        data,
        titulo,
        tipo_passagem,
        CASE 
            WHEN tipo_passagem ILIKE '%incidente%' THEN 'Incidente'
            WHEN tipo_passagem ILIKE '%change%' THEN 'Mudança'
            WHEN tipo_passagem ILIKE '%task%' THEN 'Tarefa'
            ELSE 'Outro'
        END AS categoria
    FROM passagens
    ORDER BY data DESC
""").df()

print("Resumo das passagens categorizadas:")
print(resultado.head())

# 7. Comentários separados (se quiser unir por ID depois, faça um merge)
print("\nComentários extraídos:")
print(comentarios_exploded.head())
