import tkinter as tk
import threading
import websocket
import json
import logging
import time
import random

logging.basicConfig(level=logging.INFO)

class TradeSimulatorUI:
    def __init__(self, master):
        self.master = master
        master.title("GoQuant Trade Simulator")

        # Use horizontal layout (left = input, right = output)
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=20)

        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        # --- Input Panel (Left) ---
        tk.Label(self.left_frame, text="Exchange:").pack()
        self.exchange_entry = tk.Entry(self.left_frame)
        self.exchange_entry.insert(0, "OKX")
        self.exchange_entry.pack()

        tk.Label(self.left_frame, text="Spot Asset:").pack()
        self.asset_entry = tk.Entry(self.left_frame)
        self.asset_entry.insert(0, "BTC-USDT")
        self.asset_entry.pack()

        tk.Label(self.left_frame, text="Order Type:").pack()
        self.order_type_entry = tk.Entry(self.left_frame)
        self.order_type_entry.insert(0, "market")
        self.order_type_entry.pack()

        tk.Label(self.left_frame, text="Quantity (USD):").pack()
        self.quantity_entry = tk.Entry(self.left_frame)
        self.quantity_entry.insert(0, "100")
        self.quantity_entry.pack()

        tk.Label(self.left_frame, text="Volatility:").pack()
        self.volatility_entry = tk.Entry(self.left_frame)
        self.volatility_entry.insert(0, "0.02")
        self.volatility_entry.pack()

        tk.Label(self.left_frame, text="Fee Tier:").pack()
        self.fee_tier_entry = tk.Entry(self.left_frame)
        self.fee_tier_entry.insert(0, "1")
        self.fee_tier_entry.pack()

        # Start/Stop Buttons
        self.run_button = tk.Button(self.left_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(pady=10)

        self.stop_button = tk.Button(self.left_frame, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.pack()

        # --- Output Panel (Right) ---
        tk.Label(self.right_frame, text="Output:").pack()
        self.result_text = tk.Text(self.right_frame, width=50, height=20)
        self.result_text.pack()

        # WebSocket control
        self.stop_websocket = False
        self.ws = None

    def run_simulation(self):
        # Prevent multiple threads
        if hasattr(self, "ws_thread") and self.ws_thread.is_alive():
            return

        self.stop_websocket = False
        self.ws_thread = threading.Thread(target=self.run_websocket)
        self.ws_thread.start()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Simulation started...\n")

    def stop_simulation(self):
        self.stop_websocket = True
        if self.ws:
            self.ws.close()
        self.result_text.insert(tk.END, "Simulation stopped.\n")

    def run_websocket(self):
        def on_message(ws, message):
            start_time = time.time()
            data = json.loads(message)
            self.process_order_book(data, start_time)

        def on_error(ws, error):
            logging.error(f"WebSocket Error: {error}")

        def on_close(ws, close_status_code, close_msg):
            logging.info(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")

        def on_open(ws):
            logging.info("WebSocket connection opened")

        self.ws = websocket.WebSocketApp(
            "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP",
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )
        self.ws.on_open = on_open
        self.ws.run_forever()

        while not self.stop_websocket:
            time.sleep(1)

        self.ws.close()

    def process_order_book(self, data, start_time):
        # Get user inputs
        quantity_usd = float(self.quantity_entry.get())
        volatility = float(self.volatility_entry.get())
        fee_tier = int(self.fee_tier_entry.get())

        # --- Model calculations ---
        slippage = self.calculate_slippage(quantity_usd, volatility)
        fees = self.calculate_fees(quantity_usd, fee_tier)
        impact = self.calculate_market_impact(quantity_usd, volatility)
        net_cost = slippage + fees + impact
        maker_prob = self.predict_maker_taker_prob(quantity_usd)

        latency = round((time.time() - start_time) * 1000, 2)  # in ms

        # --- Display output in GUI ---
        output = (
            f"Expected Slippage: ${slippage:.4f}\n"
            f"Expected Fees: ${fees:.4f}\n"
            f"Expected Market Impact: ${impact:.4f}\n"
            f"Net Cost: ${net_cost:.4f}\n"
            f"Maker Probability: {maker_prob:.2%}\n"
            f"Internal Latency: {latency} ms\n"
            "----------------------------------\n"
        )

        self.master.after(0, lambda: self.update_gui(output))

    def calculate_slippage(self, quantity, volatility):
        # Linear model: slippage increases with quantity and volatility
        return 0.0005 * quantity * (1 + volatility)

    def calculate_fees(self, quantity, tier):
        # Simple tiered fee model
        base_fee = 0.001
        discount = tier * 0.0001  # Tier 1 = 0.0001 off, Tier 5 = 0.0005 off
        effective_fee = max(base_fee - discount, 0.0002)
        return quantity * effective_fee

    def calculate_market_impact(self, quantity, volatility):
        # Simplified Almgren-Chriss impact model
        return 0.0003 * (quantity ** 0.5) * (1 + volatility)

    def predict_maker_taker_prob(self, quantity):
        # Logistic-like model for simplicity
        x = -0.01 * quantity + 1
        return 1 / (1 + pow(2.718, -x))  # sigmoid

    def update_gui(self, output):
        self.result_text.insert(tk.END, output)
        self.result_text.see(tk.END)  # Auto-scroll

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeSimulatorUI(root)
    root.mainloop()
