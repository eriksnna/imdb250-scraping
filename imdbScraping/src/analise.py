import pandas as pd
import os
from sqlalchemy import create_engine

def classificar_filme(nota):
    if pd.isna(nota): return "N/A"
    if nota >= 9.0: return "Obra-prima"
    elif nota >= 8.0: return "Excelente"
    elif nota >= 7.0: return "Bom"
    else: return "Mediano"

def gerar_relatorios(db_url, arquivo_saida):
    print("\niniciando análise de dados...")
    engine = create_engine(db_url)
    
    diretorio_saida = os.path.dirname(arquivo_saida)

    if diretorio_saida and not os.path.exists(diretorio_saida):
        try:
            os.makedirs(diretorio_saida)
            print(f"diretório criado: {diretorio_saida}")
        except OSError as e:
            print(f"erro ao criar diretório: {e}")
            return

    engine = create_engine(db_url)
    
    try:
        df = pd.read_sql_table('movies', con=engine)
        
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        
        df['categoria'] = df['rating'].apply(classificar_filme)
        
        df_sorted = df.sort_values(by='rating', ascending=False)
        
        print(f"análise concluída. top 3 filmes do banco:")
        print(df_sorted[['title', 'rating', 'categoria']].head(3))
        
        df_sorted.to_csv(arquivo_saida, index=False)
        print(f"arquivo '{arquivo_saida}' gerado com sucesso.")
        
    except ValueError:
        print("tabela 'movies' ainda não existe ou está vazia.")