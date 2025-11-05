import requests
import pandas as pd
import time
import ta

# === CONFIG ===
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"   # ⚠️ paste your bot token here
CHAT_ID = "-1002913169228"
PAIRS = ["BTCUSDT", "DOGSUSDT", "ETHUSDT"]  # you can add more
INTERVAL = 300  # 300 seconds = 5 minutes

# === FUNCTIONS ===
def get_price_data(symbol, limit=200):
    url = f"https://public.coindcx.com/market_data/candles?pair={symbol}&interval=5m&limit={limit}"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    return df

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.get(url, params=payload)
    except:
        print("Telegram send error")

def supertrend(df, multiplier=3, period=7):
    atr = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=period).average_true_range()
    hl2 = (df['high'] + df['low']) / 2
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)
    direction = [1]
    for i in range(1, len(df)):
        if df['close'][i] > upperband[i-1]:
            direction.append(1)
        elif df['close'][i] < lowerband[i-1]:
            direction.append(-1)
        else:
            direction.append(direction[i-1])
    df['supertrend'] = direction
    return df

def analyze(df):
    df = supertrend(df)
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], 14).rsi()
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Combined logic
    if last['supertrend'] == 1 and last
