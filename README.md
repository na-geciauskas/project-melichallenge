# Documentação da Extração

## Decisões de projeto:

## 1. Paginação: Implementada via parâmetros offset e limit

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
