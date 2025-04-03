# Pipeline de Dados do Mercado Livre

Este projeto implementa um pipeline completo de dados desde a extração até a visualização de produtos do Mercado Livre, com foco em dispositivos Chromecast.

## 📌 Visão Geral

O pipeline consiste em três etapas principais:
1. **Extração**: Coleta de dados da API de busca do Mercado Livre
2. **Transformação e Carga**: Modelagem dos dados em estrutura relacional e carga em banco SQLite
3. **Visualização**: Dashboard interativo para análise dos dados

## 🛠 Tecnologias Utilizadas

- Python 3.8+
- SQLite
- Pandas
- Plotly
- Jupyter Notebook
- Requests

## 📂 Estrutura do Projeto

<pre>
project-melichallenge/
├── data/
│   ├── raw_data.csv           # Dados brutos da API
│   └── mercado_livre.db       # Banco de dados SQLite
│
├── src/
│   ├── extraction_meli_challenge.py          # Código de extração (Passo 1)
│   ├── meli_challenge_ddl.sql                # DDL do modelo (Passo 2)
│   ├── etl_meli_challenge.py                 # Código ETL (Passo 2)
│   └── meli_challenge_dashboard.ipynb        # Jupyter notebook (Passo 3)
│
├── README.md                  # Documentação completa
└── requirements.txt           # Dependências do projeto
</pre>

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip instalado

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/na-geciauskas/projeto-melichallenge.git
cd projeto-melichallenge
```

2. Instale as dependências:
```bash
python src/etl.py
```
## 🚀 Execução do Pipeline

### 1. Extração de dados:
```bash
python src/extraction.py

```
### 2. Transformação e carga:
```bash
python src/etl.py
```

### 3. Visualização:
```bash
jupyter notebook src/dashboard.ipynb
```

## 🔍 Detalhes de Implementação

### Passo 1: Extração
- Extrai 500 resultados da API de busca
- Termo de busca: "chromecast" (produto com volume suficiente para análise)
- Tratamento robusto de erros e rate limiting
- Saída: arquivo CSV com dados brutos

### Passo 2: Modelagem e Carga
- Modelo relacional com 4 tabelas normalizadas
- Script SQL para criação da estrutura (DDL)
- Processo ETL para transformação e carga dos dados
- Banco de dados SQLite como destino

### Passo 3: Visualização
- Dashboard interativo com:
  - Filtros por categoria e faixa de preço
  - Histograma de distribuição de preços
  - Gráfico de dispersão preço vs vendidos
  - Métricas resumidas

## 📊 Decisões de Projeto

**Extração**:
- Paginação via parâmetros `offset` e `limit`
- Tratamento de rate limiting (pausas automáticas)
- 3 tentativas para cada requisição

**Modelagem**:
- Normalização em 4 tabelas relacionadas
- Tipos de dados apropriados para análise
- Foco em atributos analíticos relevantes

**Visualização**:
- Gráficos interativos com Plotly
- Filtros dinâmicos com IPywidgets
- Layout simples e informativo

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✉️ Contato

Para dúvidas ou sugestões, usar um dos meios de contato:
- Email: na.geciauskas@gmail.com
- LinkedIn: [seu-perfil](https://linkedin.com/in/nara-geciauskas-ramos-castillo)

