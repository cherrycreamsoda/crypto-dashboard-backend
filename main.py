import asyncio
import websockets
import json

def mkcandle(p,q,T):
  open = p[0]
  low = min(p)
  high = max(p)
  close = p[-1]
  volume = sum(q)
  count_of_trades = len(p)

  print(open)
  print(low)
  print(high)
  print(close)
  print(volume)
  print(count_of_trades)

async def listen(mode,url):
  async with websockets.connect(url) as ws:
    intervals = { 1:60000, 5:300000, 15:900000}
    interval = intervals.get(mode, 60000)
    first_run = True
    first_ever_run = True
    p, q, T = [], [], []

    while True :
      data = await ws.recv()
      trade = json.loads(data)
      if first_run:
        if first_ever_run:
          start_time = trade.get('T')//interval
          first_ever_run = not first_ever_run
        print("waiting... " , trade.get('T'))
        if not trade.get('T')//interval > start_time:
          continue
        start_time = trade.get('T')//interval
        first_run = not first_run
      if trade.get('T')//interval > start_time:
        break
      p.append(float(trade.get('p')))
      q.append(float(trade.get('q')))
      T.append(int(trade.get('T')))
      print(trade.get('p') , " : " , trade.get('q') , " : " , trade.get('T')//interval )
    return p , q , T
      
minute_data = asyncio.run(listen(1,"wss://stream.binance.com:9443/ws/btcusdt@trade"))
minute_candle = mkcandle(*minute_data)