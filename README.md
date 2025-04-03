## Documentação da Extração

## Decisões de projeto:

## 1. Paginação: 
  Implementada via parâmetros offset e limit

## 2. Tratamento de erros:
- Rate limiting (código 429) com pausa automática
- 3 tentativas para cada requisição
- Timeout de 30 segundos

## 3. Controle de qualidade:
- Barra de progresso com tqdm
- Logs informativos
- Validação de estrutura dos dados

## Estrutura dos dados brutos:
- Contém todos os campos retornados pela API
- Salvo em CSV para próxima etapa
- ~50 campos por item (preço, título, vendidos, condição, etc.)

## Documentação do Modelo
## Decisões de modelagem:

## 1. Normalização:
- Separação em 4 tabelas para evitar redundância
- Relacionamentos muitos-para-muitos (produto-categoria)

## 2. Campos selecionados:
- Foco em atributos analíticos (preço, vendidos, reputação)
- Manutenção de campos originais importantes (IDs, timestamps)

## 3. Tipos de dados:
- `DECIMAL` para valores monetários
- `TIMESTAMP` para datas
- `TEXT` para campos descritivos

## Justificativas:
- Modelo otimizado para análises de:
  - Performance de produtos
  - Relação preço-vendas
  - Desempenho de categorias
- Flexível para adição de novas dimensões

## Documentação da Visualização
## Recursos do dashboard:

## 1. Filtros interativos:
- Seleção por categoria
- Faixa de preço ajustável

## 2. Visualizações:
- Histograma de distribuição de preços
- Dispersão preço vs vendidos (colorido por condição)

## 3. Métricas-chave:
- Preço médio por categoria
- Volume total de vendas

## Tecnologias utilizadas:
- *Plotly*: Para gráficos interativos
- *IPywidgets*: Para controles de filtro
- *SQLite*: Como backend de dados
