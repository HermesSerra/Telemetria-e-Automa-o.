# Projeto de Comunicação Modbus TCP - Hermes Renato Serra

## Descrição

Este projeto implementa a comunicação com um servidor Modbus TCP para captura, conversão, validação e apresentação de dados dos sensores conforme solicitado no edital. A solução está organizada em três etapas principais:

1. Captura de Dados Brutos  
2. Conversão e Apresentação dos Dados  
3. Validação dos Dados e Geração de JSON

## Estrutura dos Arquivos

- `captura_dados.py`: Código responsável pela conexão Modbus TCP e leitura dos registros brutos.  
- `conversao_dados.py`: Processa os dados brutos aplicando as conversões necessárias e organiza por categoria.  
- `validacao_json.py`: Valida os dados convertidos, verifica integridade e gera o JSON final formatado.  
- `dashboard_modbus.py`: Visualização dos dados em dashboard com gráficos interativos.

## Como Executar

1. Garanta que o servidor Modbus TCP esteja ativo na máquina local na porta 502.  
2. Execute o script `captura_dados.py` para coletar os dados brutos.  
3. Rode `conversao_dados.py` para converter e organizar os dados.  
4. Utilize `validacao_json.py` para validar e gerar o pacote JSON.  
5. (Opcional) Execute `dashboard_modbus.py` para visualizar os dados em gráficos interativos.

## Detalhes Técnicos

- Comunicação Modbus TCP em `localhost:502`  
- Leitura dos Holding Registers de 40001 a 40020 e Coils de 00001 a 00010  
- Conversões aplicadas:  
  - Temperaturas: valores lidos divididos por 10 (°C)  
  - Pressões: divididos por 100 (bar)  
  - Tensões: divididos por 10 (V)  
  - Correntes: divididos por 10 (A)  
- Validações:  
  - Temperaturas entre -50 e 150 °C  
  - Pressões entre 0 e 50 bar  
  - Tensões entre 100 e 300 V  
  - Correntes entre 0 e 100 A  
  - Vazões entre 0 e 1000 L/min  
  - Níveis entre 0 e 100 %

## Dashboard Interativo

Além dos scripts principais para captura, conversão e validação, desenvolvi um dashboard interativo usando a biblioteca Dash (Python) para facilitar a visualização dos dados Modbus.

### Características do Dashboard

- Lê os dados validados do arquivo JSON `dados_modbus.json`  
- Apresenta gráficos de barras para as categorias:  
  - Temperaturas (°C)  
  - Pressões (bar)  
  - Vazões (L/min)  
  - Níveis (%)  
  - Tensões (V)  
  - Correntes (A)  
- O dashboard abre automaticamente no navegador padrão ao executar o script `dashboard_modbus.py`  
- Facilita a análise visual e rápida dos dados coletados e processados

### Como usar

Execute no terminal:

```bash
python dashboard_modbus.py
