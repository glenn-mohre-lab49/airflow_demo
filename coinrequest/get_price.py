import json
import requests
import datetime
from dataclasses import dataclass, asdict

@dataclass
class BTCPrice:
    currency: str
    rate: float
    price_date: datetime.datetime = datetime.datetime.now()
    API_URL: str = 'https://api.coindesk.com/v1/bpi/currentprice.json'

    def __dict__(self):
        return {
            'currency': self.currency,
            'rate': self.rate,
            'price_date': str(self.price_date)
        }

    def __repr__(self):
        return f"{self.currency}:{self.rate} @ {self.price_date}"

    @classmethod
    def get_btc_prices(cls):
        data = requests.get(cls.API_URL).json()
        prices = []
        for item in data['bpi'].values():
            prices.append(cls(**{'currency': item['code'], 'rate': item.get('rate_float')}))
        
        return [p.__dict__() for p in prices]

    @classmethod
    def process_prices(cls, prices):
        return json.dumps(prices)

    @classmethod
    def compose_price_email(cls, price_json):
        return {
            'subject': 'Price JSON',
            'body': f'Price JSON\n{price_json}'
        }

