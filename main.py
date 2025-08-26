import asyncio
import websockets
import json

async def listen(url):
  async with websockets.connect(url) as ws:
    first_run = True
    first_ever_run = True
    p, q, T = [], [], []

    while True :
      data = await ws.recv()
      trade = json.loads(data)
      if first_run:
        if first_ever_run:
          start_time = trade.get('T')//60000
          first_ever_run = not first_ever_run
        print("waiting... " , trade.get('T'))
        if not trade.get('T')//60000 > start_time:
          continue
        start_time = trade.get('T')//60000
        first_run = not first_run
      if trade.get('T')//60000 > start_time:
        break
      p.append(trade.get('p'))
      q.append(trade.get('q'))
      T.append(trade.get('T'))
      print(trade.get('p') , " : " , trade.get('q') , " : " , trade.get('T')//60000 )
    return p , q , T
      
asyncio.run(listen("wss://stream.binance.com:9443/ws/btcusdt@trade"))
print("SUCESS!")