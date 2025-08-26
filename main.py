import asyncio
import websockets
import json


async def listen():
  url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

  
  async with websockets.connect(url) as wss:
    first_run = True
    first_ever_run = True
    prices = []
    qualtities = []
    timestamps = []

    while True :
      data = await wss.recv()
      trade = json.loads(data)
      if first_run:
        if first_ever_run:
          start_time = trade.get('T')//60000
          first_ever_run = False
        print("waiting... " , trade.get('T'))
        if not trade.get('T')//60000 > start_time:
          continue
        start_time = trade.get('T')//60000
        first_run = False
      if trade.get('T')//60000 > start_time:
        break
      prices.append(trade.get('p'))
      qualtities.append(trade.get('q'))
      timestamps.append(trade.get('T'))
      print(trade.get('p') , " : " , trade.get('q') , " : " , trade.get('T')//60000 )
    for price in prices:
      print(price)
      

asyncio.run(listen())