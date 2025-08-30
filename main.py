import asyncio
import websockets
import json
import pandas as pd
import datetime


def mkcandle(p,q,T):
  return{
    "open_": p[0],
    "close_": p[-1],
    "low": min(p),
    "high": max(p),
    "volume": sum(q),
    "trades": len(p),
    "start_time": T[0],
    "end_time": T[-1]
  }

async def listen(mode,url):
    async with websockets.connect(url) as ws:
        intervals = {1:60000, 5:300000, 15:900000}
        interval = intervals.get(mode, 60000)
        first_run = True
        first_ever_run = True
        p, q, T, local_time = [], [], [], []

        while True:
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
            local_time.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            
            print(trade.get('p') , " : " , trade.get('q') , " : " , trade.get('T')//interval )

        return p, q, T, local_time


minute_data = asyncio.run(listen(1, "wss://stream.binance.com:9443/ws/btcusdt@trade"))
minute_candle = mkcandle(*minute_data[:3])

df = pd.DataFrame(list(zip(*minute_data)), columns=["price", "quantity", "timestamp", "local_time"])

df.to_excel("trades.xlsx", index=False)

with pd.ExcelWriter("trades.xlsx", mode="a", if_sheet_exists="overlay") as writer:
    pd.DataFrame([minute_candle]).to_excel(writer, sheet_name="Candles", index=False)
