from binance import AsyncClient, BinanceSocketManager
from aiogram import Bot
from collections import deque


class Ticker:

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.price_feed: deque = deque([], maxlen=120)

    def update(self, ts: int, price: float):
        self.price_feed.append((ts, price))

    def get_change(self) -> float:
        p1, p2 = self.price_feed[0][1], self.price_feed[-1][1]
        return (p2 - p1) / p1


async def screen(bot: Bot):
    client = await AsyncClient.create()
    bsm = BinanceSocketManager(client)

    tickers: dict[str, Ticker] = {}

    async with bsm.miniticker_socket() as ms:
        while True:
            events = await ms.recv()
            alerts = []
            for e in events:
                symbol = e['s']
                if symbol[-4:] != 'USDT':
                    continue

                if ticker := tickers.get(symbol):
                    ticker.update(e['E'], e['c'])
                    change = ticker.get_change()
                    if change >= 0.02: alerts.append({'symbol': symbol, 'change': change})
                else:
                    tickers[symbol] = Ticker(symbol)
                    tickers[symbol].update(e['E'], e['c'])
