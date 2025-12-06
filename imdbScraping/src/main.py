import json
import scraper as scraper
import database as database
import analise as analise
from models import Series 

def carregar_config():
    with open('./config.json', 'r') as f:
        return json.load(f)

def main():
    config = carregar_config()
    print("configuração carregada.")
    
    engine = database.inicializar_banco(config['db_url'])
    
    filmes_extraidos = scraper.executar_scraping(config['url'], config['n_filmes'])
    print(f"{len(filmes_extraidos)} filmes extraídos.")
    
    filmes_extraidos.append(Series("twin peaks", "1990", 2, 30))
    filmes_extraidos.append(Series("game of thrones", "2011", 8, 73))
    
    database.salvar_catalogo(engine, filmes_extraidos)
    
    analise.gerar_relatorios(config['db_url'], config['output_csv'])
    
    print("\nfluxo finalizado com sucesso!")

if __name__ == "__main__":
    main()