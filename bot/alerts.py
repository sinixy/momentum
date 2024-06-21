from bot import bot
from config import RECEIVER_ID


async def send_alerts(alerts: list[dict]):
    text = ''
    for alert in alerts:
        symbol = alert['symbol']
        change_prc = alert['change'] * 100
        text += f'{symbol} - {change_prc :.2f}\n'
    await bot.send_message(RECEIVER_ID, text)