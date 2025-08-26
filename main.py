import asyncio
import websockets
import json

async def listen():
  url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
  
  async with websockets.connect(url) as wss:

    while True:
      data = await wss.recv()
      # print(data)
      trade = json.loads(data)
      print(trade.get('p') , " : " , trade.get('q') , " : " , trade.get('T') )

asyncio.run(listen())