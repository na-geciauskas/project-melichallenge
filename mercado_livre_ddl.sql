-- Modelo otimizado para análise de produtos eletrônicos

CREATE TABLE produtos (
    id VARCHAR(20) PRIMARY KEY,
    titulo TEXT NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    condicao VARCHAR(20) NOT NULL,
    vendidos INTEGER DEFAULT 0,
    data_criacao TIMESTAMP,
    permalink TEXT,
    thumbnail TEXT
);

CREATE TABLE vendedores (
    vendedor_id INTEGER PRIMARY KEY,
    nome TEXT,
    reputacao DECIMAL(3,2),
    transacoes INTEGER
);

CREATE TABLE categorias (
    categoria_id VARCHAR(20) PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE produto_categoria (
    produto_id VARCHAR(20) REFERENCES produtos(id),
    categoria_id VARCHAR(20) REFERENCES categorias(id),
    PRIMARY KEY (produto_id, categoria_id)
);
