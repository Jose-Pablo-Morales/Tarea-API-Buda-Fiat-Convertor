from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_rate(market_id):
    base_url = "https://www.buda.com/api/v2/markets"
    try:
        response = requests.get(f"{base_url}/{market_id}/ticker")
        response.raise_for_status()
        data = response.json()
        return data['ticker']['last_price'][0]
    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f"[Error] No se encontro una conversion para: {market_id} - {e}")
        return None

def generate_market_list(portfolio, fiat_list):
    market_id_list = []
    for market in portfolio.keys():
        for fiat in fiat_list:
            market_id_list.append(f"{market}-{fiat}")
    return market_id_list

def generate_rates(market_id_list):
    rates = {}
    for market_id in market_id_list:
        rate = get_rate(market_id)
        rates[market_id] = rate 
    return rates

def calculate_fiat_portfolio(rates, portfolio, fiat_list):
    fiat_portfolio = {}
    for fiat in fiat_list:
        total = 0
        for crypto_id, crypto_amount in portfolio.items():
            market_id = f"{crypto_id}-{fiat}"
            rate = rates.get(market_id)

            if rate is None:
                return {
                    "error": f"Conversion para '{market_id}' no se encontro."
                }, 400

            total += crypto_amount * float(rate)

        fiat_portfolio[fiat] = total
    return fiat_portfolio

@app.route('/fiat_conversion', methods=['GET'])
def fiat_conversion():
    data = request.get_json()
    
    if not data or 'portfolio' not in data or 'fiat_currency' not in data:
        return jsonify({"error": " Debe contener campos 'portfolio' y 'fiat_currency' "}), 400

    portfolio = data['portfolio']
    fiat_currency = data['fiat_currency']
    fiat_list = fiat_currency if isinstance(fiat_currency, list) else [fiat_currency]

    market_id_list = generate_market_list(portfolio, fiat_list)
    rates = generate_rates(market_id_list)

    result = calculate_fiat_portfolio(rates, portfolio, fiat_list)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
