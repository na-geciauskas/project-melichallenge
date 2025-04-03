import pandas as pd
import sqlite3
from datetime import datetime

class MercadoLivreETL:
    def __init__(self, raw_data_file="raw_data.csv", db_file="mercado_livre.db"):
        self.raw_data = pd.read_csv(raw_data_file)
        self.conn = sqlite3.connect(db_file)
        
    def transform_data(self):
        """Transforma os dados brutos para o modelo relacional"""
        # Produtos
        produtos = self.raw_data[[
            'id', 'title', 'price', 'condition', 'sold_quantity',
            'date_created', 'permalink', 'thumbnail'
        ]].rename(columns={
            'title': 'titulo',
            'price': 'preco',
            'condition': 'condicao',
            'sold_quantity': 'vendidos',
            'date_created': 'data_criacao'
        })
        produtos['data_criacao'] = pd.to_datetime(produtos['data_criacao'])
        
        # Vendedores
        vendedores = pd.json_normalize(self.raw_data['seller'].dropna())
        vendedores = vendedores[[
            'id', 'nickname', 'seller_reputation.transactions.total',
            'seller_reputation.power_seller_status'
        ]].rename(columns={
            'id': 'vendedor_id',
            'nickname': 'nome',
            'seller_reputation.transactions.total': 'transacoes',
            'seller_reputation.power_seller_status': 'reputacao'
        })
        
        # Categorias
        categorias = pd.json_normalize(self.raw_data['category'].dropna())[['id', 'name']]
        categorias = categorias.rename(columns={'id': 'categoria_id', 'name': 'nome'})
        
        # Tabela de relacionamento
        produto_categoria = self.raw_data[['id', 'category.id']].dropna()
        produto_categoria = produto_categoria.rename(columns={
            'id': 'produto_id',
            'category.id': 'categoria_id'
        })
        
        return {
            'produtos': produtos,
            'vendedores': vendedores,
            'categorias': categorias,
            'produto_categoria': produto_categoria
        }
    
    def load_data(self, transformed_data):
        """Carrega os dados transformados no banco SQLite"""
        with self.conn:
            for table_name, df in transformed_data.items():
                df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        print(f"Dados carregados com sucesso em {self.conn}")
    
    def run(self):
        transformed = self.transform_data()
        self.load_data(transformed)
        self.conn.close()

if __name__ == "__main__":
    etl = MercadoLivreETL()
    etl.run()
