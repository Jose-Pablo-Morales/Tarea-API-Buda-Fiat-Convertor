import unittest
from unittest.mock import patch
from app import app, generate_market_list, calculate_fiat_portfolio

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.get_rate')
    def test_fiat_conversion_endpoint(self, mock_get_rate):
        mock_get_rate.side_effect = lambda market_id: {
            'BTC-CLP': '115000000',
            'ETH-CLP': '3331326'
        }.get(market_id, '0')

        payload = {
            "portfolio": {
                "BTC": 0.5,
                "ETH": 2
            },
            "fiat_currency": ["CLP"]
        }

        response = self.client.get('/fiat_conversion', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        expected_total = 0.5 * 115000000 + 2 * 3331326  # 5,000,000 + 6,000,000
        self.assertEqual(data["CLP"], expected_total)

    def test_generate_market_list(self):
        portfolio = {"BTC": 0.5, "ETH": 2}
        fiat_list = ["CLP", "PEN"]
        market_ids = generate_market_list(portfolio, fiat_list)
        expected = ["BTC-CLP", "BTC-PEN", "ETH-CLP", "ETH-PEN"]
        self.assertEqual(set(market_ids), set(expected))

    def test_calculate_fiat_portfolio(self):
        rates = {
            "BTC-CLP": "115000000",
            "ETH-CLP": "3331326"
        }
        portfolio = {
            "BTC": 0.5,
            "ETH": 2
        }
        fiat_list = ["CLP"]
        result = calculate_fiat_portfolio(rates, portfolio, fiat_list)
        self.assertAlmostEqual(result["CLP"], 0.5 * 115000000 + 2 * 3331326)

if __name__ == '__main__':
    unittest.main()
