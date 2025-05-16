import requests
import matplotlib
matplotlib.use('Agg')  # Backend não interativo para salvar gráficos
import matplotlib.pyplot as plt
from datetime import datetime
import time
import numpy as np
from requests.exceptions import HTTPError

# Dicionário com nome e ID CoinGecko das criptomoedas
cryptos = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Binance Coin": "binancecoin",
    "Solana": "solana",
    "Cardano": "cardano",
    "Ripple": "ripple"
}

# Função para obter histórico de preços com retentativas
def get_price_history(crypto_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"Tentativa {attempt + 1} para obter dados de {crypto_id}...")
            url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': '30',
                'interval': 'daily'  # Dados diários para reduzir carga
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Levanta exceção para erros HTTP
            data = response.json()
            
            if 'prices' not in data or not data['prices']:
                print(f"Erro: Dados de preços não encontrados para {crypto_id}")
                return [], []
            
            prices = data['prices']
            dates = [datetime.fromtimestamp(p[0] / 1000.0).date() for p in prices]
            values = [p[1] for p in prices]
            print(f"Dados obtidos para {crypto_id}: {len(prices)} pontos")
            return dates, values
        except HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 10 * (2 ** attempt)  # Espera exponencial: 10s, 20s, 40s
                print(f"Erro 429: Limite de requisições atingido para {crypto_id}. Aguardando {wait_time} segundos...")
                time.sleep(wait_time)
            else:
                print(f"Erro HTTP ao obter dados para {crypto_id}: {e}")
                return [], []
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados para {crypto_id}: {e}")
            return [], []
    
    print(f"Falha após {max_retries} tentativas para {crypto_id}")
    return [], []

# Criar figura e subplots
fig, axes = plt.subplots(3, 2, figsize=(14, 10))
fig.suptitle('Histórico de Preço - Últimos 30 Dias (USD)', fontsize=16)

# Lista de cores para diferenciar os gráficos
colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan']

# Preencher os subplots
for ax, (name, crypto_id), color in zip(axes.flatten(), cryptos.items(), colors):
    dates, values = get_price_history(crypto_id)
    
    if not dates or not values:
        ax.text(0.5, 0.5, f"Dados indisponíveis para {name}", 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title(name)
        ax.grid(True)
    else:
        ax.plot(dates, values, label=name, color=color, linewidth=1.5)
        ax.set_title(name)
        ax.set_xlabel('Data')
        ax.set_ylabel('Preço (USD)')
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)
        ax.set_xticks(ax.get_xticks()[::5])  # Reduzir rótulos no eixo X
        ax.set_ylim(min(values) * 0.95, max(values) * 1.05)  # Ajustar eixo Y
        ax.legend()
    
    # Atraso entre requisições para evitar limite
    time.sleep(10)

# Ajustar layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Salvar o gráfico como arquivo
output_file = "crypto_prices.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Gráfico salvo como {output_file}")

# Tentar exibir o gráfico
try:
    plt.show(block=True)
except Exception as e:
    print(f"Não foi possível exibir o gráfico: {e}")
    print(f"Por favor, verifique o arquivo salvo: {output_file}")

# Fechar a figura para liberar memória
plt.close(fig)
