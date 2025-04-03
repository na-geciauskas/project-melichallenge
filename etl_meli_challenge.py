import pandas as pd
import sqlite3
from datetime import datetime

class MercadoLivreETL:
    def __init__(self, raw_data_file="raw_data.csv", db_file="mercado_livre.db"):
        self.raw_data = pd.read_csv(raw_data_file)
        self.conn = sqlite3.connect(db_file)

    def save_raw_data(self, df, filename_prefix="raw_data"):
        """
        Salva os dados brutos com timestamp para versionamento
        
        Args:
            df (DataFrame): Dados a serem salvos
            filename_prefix (str): Prefixo para o nome do arquivo
            
        Returns:
            str: Caminho completo do arquivo gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"Dados brutos versionados em: {filename}")
        return filename
        
    def transform_data(self):
    """
    Transforma os dados brutos da API em um modelo relacional normalizado,
    aplicando validações básicas e tratamentos essenciais.
    
    Returns:
        dict: Dicionário com 4 DataFrames normalizados:
            - produtos: Informações principais dos produtos
            - vendedores: Dados dos sellers com reputação
            - categorias: Hierarquia de categorias
            - produto_categoria: Relacionamento muitos-para-muitos
            
    Raises:
        AssertionError: Se violações de integridade forem detectadas
    """
    
    # --- Transformação de Produtos ---
    # Seleciona e renomeia colunas relevantes mantendo a rastreabilidade
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
    
    # Conversão de tipos e validação básica
    produtos['data_criacao'] = pd.to_datetime(produtos['data_criacao'])
    assert not produtos['id'].duplicated().any(), "IDs duplicados encontrados em produtos"
    assert produtos['titulo'].notna().all(), "Títulos de produtos ausentes"

    # --- Transformação de Vendedores ---
    # Extrai e normaliza dados aninhados de sellers
    vendedores = pd.json_normalize(self.raw_data['seller'].dropna())
    
    # Seleção e mapeamento de colunas com tratamento de nulos
    vendedores = vendedores[[
        'id', 'nickname', 'seller_reputation.transactions.total',
        'seller_reputation.power_seller_status'
    ]].rename(columns={
        'id': 'vendedor_id',
        'nickname': 'nome',
        'seller_reputation.transactions.total': 'transacoes',
        'seller_reputation.power_seller_status': 'reputacao'
    })
    
    # Preenchimento de valores ausentes em reputação
    vendedores['reputacao'] = vendedores['reputacao'].fillna('Sem reputação')
    
    # --- Transformação de Categorias ---
    # Extrai hierarquia de categorias com checagem de integridade
    categorias = pd.json_normalize(self.raw_data['category'].dropna())[['id', 'name']]
    categorias = categorias.rename(columns={'id': 'categoria_id', 'name': 'nome'})
    categorias = categorias.dropna(subset=['categoria_id'])  # Remove categorias inválidas

    # --- Tabela de Relacionamento ---
    # Cria tabela de associação com verificação de chaves
    produto_categoria = self.raw_data[['id', 'category.id']].dropna()
    produto_categoria = produto_categoria.rename(columns={
        'id': 'produto_id',
        'category.id': 'categoria_id'
    })
    
    # Valida integridade referencial
    categorias_validas = categorias['categoria_id'].unique()
    pc_filtrado = produto_categoria[produto_categoria['categoria_id'].isin(categorias_validas)]
    
    if len(pc_filtrado) < len(produto_categoria):
        print(f"Aviso: {len(produto_categoria) - len(pc_filtrado)} relacionamentos com categorias inválidas removidos")
    
    return {
        'produtos': produtos,
        'vendedores': vendedores,
        'categorias': categorias,
        'produto_categoria': pc_filtrado
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
