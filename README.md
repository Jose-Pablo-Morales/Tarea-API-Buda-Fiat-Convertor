# API Fiat Convertor

Con esta API, se puede convertir un portafolio de criptomonedas a su equivalente a moneda fiat, usando los precios en tiempo real de la API publica de buda.com. 
Además se añadió la funcionalidad de convertir a varias monedas fiat en el mismo request.

Se utiliza "last_price" como multiplicador de la divisa

## Endpoint

GET https://tarea-api-buda-fiat-convertor.onrender.com/fiat_conversion

## Ejemplo de uso

```json
{
	"portfolio": {
		"BTC": 0.5,
		"ETH": 2.0,
		"USDT": 1000
	},
	"fiat_currency": ["CLP","PEN","COP"]
}
```
Si se necesita  solo la conversion de una moneda fiat, no es necesario usar corchetes como lista.

```json
{
	"portfolio": {
		"BTC": 0.5,
		"ETH": 2.0,
		"USDT": 1000
	},
	"fiat_currency": "CLP"
}
```

## Respuesta

```json
{
    "CLP": 65127072.0,
    "COP": 264655902.515,
    "PEN": 232540.245
}
```



## Funcionalidad Interna

### get_rate(market_id)

Obtiene el último precio de una criptomoneda en una moneda fiat desde la API de Buda.

### generate_market_list(portfolio, fiat_list)

Genera IDs de mercados necesarios (ej. btc-clp, eth-ars).

### generate_rates(market_id_list)

Recupera las tasas de cambio para todos los mercados especificados.

### calculate_fiat_portfolio(rates, portfolio, fiat_list)

Calcula el valor total del portafolio en cada moneda fiat.

#### Se escribieron tests para el endpoint, generate_market_list y calculate_fiat_portfolio.


