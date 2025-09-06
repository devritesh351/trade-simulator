import websocket
import json
import pandas as pd
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Global variables to store order book data
order_book = {
    "asks": [],
    "bids": []
}

# WebSocket callback functions
def on_message(ws, message):
    global order_book
    data = json.loads(message)
    order_book['asks'] = data['asks']
    order_book['bids'] = data['bids']
    process_order_book()

def on_error(ws, error):
    logging.error(f"Error: {error}")

def on_close(ws):
    logging.info("WebSocket closed")

def on_open(ws):
    logging.info("WebSocket connection opened")

# Function to process order book data
def process_order_book():
    expected_slippage = calculate_expected_slippage()
    expected_fees = calculate_expected_fees()
    expected_market_impact = calculate_expected_market_impact()
    net_cost = expected_slippage + expected_fees + expected_market_impact
    logging.info(f"Net Cost: {net_cost}")

def calculate_expected_slippage():
    return np.random.uniform(0, 1)  # Placeholder

def calculate_expected_fees():
    return np.random.uniform(0, 1)  # Placeholder

def calculate_expected_market_impact():
    return np.random.uniform(0, 1)  # Placeholder

# Main function to run the WebSocket client
def run_websocket():
    ws = websocket.WebSocketApp("wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP",
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    run_websocket()
