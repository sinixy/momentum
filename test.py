from binance import AsyncClient, DepthCacheManager, BinanceSocketManager
import asyncio

from config import BINANCE_API_KEY, BINANCE_API_SECRET

async def main():

    # initialise the client
    client = await AsyncClient.create()
    info = await client.futures_exchange_info()
    pairs = [i for i in info['symbols'] if i['symbol'][-4:] == 'USDT']

    # initialise websocket factory manager
    bsm = BinanceSocketManager(client)

    async with bsm.miniticker_socket() as ms:
        while True:
            tickers = await ms.recv()
            for t in tickers:
                if t['s'] == 'BTCUSDT': print(t['c'])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())