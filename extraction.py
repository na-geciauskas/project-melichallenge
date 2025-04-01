import requests
import pandas as pd
from tqdm import tqdm
import time
import sqlite3
from datetime import datetime

class MercadoLivreExtractor:
    def __init__(self):
        self.base_url = "https://api.mercadolibre.com/sites/MLA/search"
        self.headers = {'User-Agent': 'DataPipeline/1.0'}

    def fetch_data(self, keyword="chromecast", total_results=500, results_per_page=50):
        """
        Extrai dados da API do Mercado Livre com tratamento de erros e paginação
        
        Args:
            keyword: Termo de busca (default: "chromecast")
            total_results: Número total de resultados desejados
            results_per_page: Itens por página (máx 50)
            
        Returns:
            DataFrame com os resultados
        """
        all_results = []
        retries = 3
        
        with tqdm(total=total_results, desc="Extraindo dados") as pbar:
            offset = 0
            while len(all_results) < total_results:
                try:
                    params = {
                        'q': keyword,
                        'limit': results_per_page,
                        'offset': offset
                    }
                    
                    response = requests.get(
                        self.base_url,
                        params=params,
                        headers=self.headers,
                        timeout=30
                    )
                    
                    # Tratamento de erros
                    if response.status_code == 429:
                        wait_time = int(response.headers.get('Retry-After', 10))
                        print(f"Rate limit atingido. Aguardando {wait_time} segundos...")
                        time.sleep(wait_time)
                        continue
                        
                    response.raise_for_status()
                    
                    data = response.json()
                    current_results = data.get('results', [])
                    
                    if not current_results:
                        break
                        
                    all_results.extend(current_results)
                    offset += results_per_page
                    pbar.update(len(current_results))
                    
                    # Respeitar rate limit
                    time.sleep(1)
                    
                except requests.exceptions.RequestException as e:
                    if retries > 0:
                        retries -= 1
                        time.sleep(5)
                        continue
                    raise Exception(f"Falha na requisição após 3 tentativas: {e}")
                
        return pd.DataFrame(all_results[:total_results])

    def save_raw_data(self, df, filename="raw_data.csv"):
        """Salva os dados brutos em CSV"""
        df.to_csv(filename, index=False)
        print(f"Dados brutos salvos em {filename}")

if __name__ == "__main__":
    extractor = MercadoLivreExtractor()
    
    # Escolhi "chromecast" por ser um produto com:
    # - Volume suficiente de resultados (>500)
    # - Diversidade de atributos para análise
    # - Preços variados para visualização interessante
    
    try:
        df = extractor.fetch_data()
        extractor.save_raw_data(df)
        
        print("\n✅ Extração concluída com sucesso!")
        print(f"Total de itens extraídos: {len(df)}")
        print(f"Colunas disponíveis: {list(df.columns)}")
        
    except Exception as e:
        print(f"\n❌ Erro na extração: {e}")
