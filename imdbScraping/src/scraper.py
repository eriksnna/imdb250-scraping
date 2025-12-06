import requests
from bs4 import BeautifulSoup
from models import Movie

def executar_scraping(url, limite_filmes=250):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"acessando {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        containers = soup.select('li.ipc-metadata-list-summary-item')
        
        lista_filmes = []
        
        for i, container in enumerate(containers):
            if i >= limite_filmes:
                break
                
            tag_titulo = container.select_one('h3.ipc-title__text')
            raw_title = tag_titulo.get_text(strip=True) if tag_titulo else "N/A"
            try:
                titulo = raw_title.split('. ', 1)[1]
            except IndexError:
                titulo = raw_title

            metadados = container.select('span.cli-title-metadata-item')
            ano = metadados[0].get_text(strip=True) if metadados else "N/A"

            tag_nota = container.select_one('span.ipc-rating-star')
            nota = tag_nota.get_text(strip=True).split('(')[0].strip() if tag_nota else "N/A"
            
            novo_filme = Movie(titulo, ano, nota)
            lista_filmes.append(novo_filme)
            
        return lista_filmes

    except Exception as e:
        print(f"erro no scraping: {e}")
        return []