

# Histórico de Preços de Criptomoedas

## Descrição
Este projeto contém um script em Python que obtém e visualiza o histórico de preços de criptomoedas nos últimos 30 dias, utilizando a API da CoinGecko. O script gera gráficos de preços para seis criptomoedas (Bitcoin, Ethereum, Binance Coin, Solana, Cardano e Ripple) em USD, exibindo os dados em uma grade de subplots 3x2. Os gráficos são salvos como um arquivo PNG (`crypto_prices.png`) e, se possível, exibidos em uma janela.

## Requisitos
Para executar o script, você precisa das seguintes bibliotecas instaladas:
- Python 3.x
- Requests
- Matplotlib
- NumPy

Instale as dependências usando o pip:
```bash
pip install requests matplotlib numpy
```

## Como Usar
1. Salve o script Python (por exemplo, como `crypto_prices.py`).
2. Execute o script em um ambiente Python com as bibliotecas necessárias instaladas:
   ```bash
   python crypto_prices.py
   ```
3. O script fará requisições à API da CoinGecko e gerará um arquivo `crypto_prices.png` no diretório atual.
4. Se a exibição gráfica for suportada no seu ambiente, uma janela com os gráficos será exibida; caso contrário, verifique o arquivo PNG gerado.

## Estrutura do Código
O script realiza as seguintes etapas:
1. **Definição das Criptomoedas**:
   - Um dicionário (`cryptos`) mapeia nomes de criptomoedas para seus IDs na API CoinGecko.
2. **Obtenção de Dados**:
   - A função `get_price_history` faz requisições à API da CoinGecko para obter o histórico de preços dos últimos 30 dias, com dados diários.
   - Inclui tratamento de erros para falhas de rede, limites de requisições (HTTP 429) e respostas inválidas.
   - Implementa retentativas com espera exponencial para lidar com erros 429.
3. **Visualização**:
   - Cria uma grade de subplots 3x2 usando Matplotlib.
   - Cada subplot exibe o histórico de preços de uma criptomoeda, com cores distintas.
   - Ajusta os rótulos de data no eixo X para evitar sobreposição e melhora a legibilidade.
4. **Saída**:
   - Salva o gráfico como `crypto_prices.png` com alta resolução (DPI 300).
   - Tenta exibir o gráfico em uma janela, com fallback para o arquivo PNG em caso de falha.

## Exemplo de Saída
O script gera:
- **Arquivo**: `crypto_prices.png`, contendo uma grade de subplots com o histórico de preços de cada criptomoeda.
- **Console**: Mensagens de progresso, como:
  ```
  Tentativa 1 para obter dados de bitcoin...
  Dados obtidos para bitcoin: 31 pontos
  Tentativa 1 para obter dados de ethereum...
  ...
  Gráfico salvo como crypto_prices.png
  ```
- **Gráfico (se exibido)**: Uma janela com subplots mostrando os preços das criptomoedas em USD, com eixos rotulados e legendas.

## Personalização
Você pode modificar os seguintes aspectos do código:
- **Criptomoedas**: Edite o dicionário `cryptos` para incluir ou remover criptomoedas. IDs válidos podem ser encontrados na documentação da CoinGecko.
- **Período de Dados**: Altere o parâmetro `days` na função `get_price_history` para obter dados de períodos diferentes (e.g., 7 dias, 90 dias).
- **Estilo Gráfico**: Ajuste cores, tamanhos de fonte, ou layout dos subplots modificando os parâmetros em `plt.plot`, `plt.subplots`, ou `plt.savefig`.
- **Atraso entre Requisições**: Modifique o valor de `time.sleep(10)` para ajustar o intervalo entre chamadas à API, caso ainda enfrente erros 429.

## Limitações
- **Limite de Requisições**: A API gratuita da CoinGecko tem um limite de 10-50 requisições por minuto. O script inclui atrasos e retentativas, mas pode falhar em conexões instáveis ou se o limite for atingido.
- **Exibição Gráfica**: Em ambientes sem interface gráfica (e.g., servidores remotos), o gráfico não será exibido, mas o arquivo PNG será gerado.
- **Granularidade dos Dados**: O script usa dados diários (`interval='daily'`) para reduzir a carga na API. Para dados mais detalhados (por hora), remova o parâmetro `interval`, mas isso pode aumentar o risco de atingir o limite de requisições.

## Solução de Problemas
- **Erro 429 (Too Many Requests)**:
  - Aumente o atraso entre requisições (e.g., `time.sleep(15)`).
  - Reduza o número de criptomoedas no dicionário `cryptos`.
  - Considere usar uma chave de API paga da CoinGecko para limites mais altos.
- **Gráfico Não Exibido**:
  - Verifique o arquivo `crypto_prices.png` gerado no diretório.
  - Certifique-se de que seu ambiente suporta exibição gráfica ou remova a tentativa de exibição (`plt.show()`).
- **Falha na API**:
  - Teste a conexão com a API:
    ```bash
    curl https://api.coingecko.com/api/v3/ping
    ```
    Deve retornar: `{"gecko_says":"(V3) To the Moon!"}`.

## Licença
Este projeto é fornecido sob a licença MIT. Sinta-se à vontade para usar, modificar e distribuir conforme necessário.


