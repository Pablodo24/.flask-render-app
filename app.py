import os
import requests
import pandas as pd
from flask import Flask, jsonify
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

def get_binance_data():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100"
    response = requests.get(url).json()
    df = pd.DataFrame(response, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                         'close_time', 'quote_asset_volume', 'trades', 'taker_buy_base',
                                         'taker_buy_quote', 'ignore'])
    df['close'] = df['close'].astype(float)
    return df[['close']]

@app.route('/recommendation', methods=['GET'])
def get_recommendation():
    price_data = get_binance_data()
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(price_data["close"].values.reshape(-1,1))

    predicted_price = scaler.inverse_transform([[scaled_data[-1][0] * 1.01]])[0][0]

    return jsonify({
        "predicted_price": predicted_price,
        "recommendation": "BUY" if predicted_price > price_data["close"].iloc[-1] else "SELL"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
