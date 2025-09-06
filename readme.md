#  Trade Simulator

A real-time, high-performance crypto trade simulator built using Python. This project connects to a live Level 2 (L2) orderbook WebSocket from OKX to estimate transaction costs, including slippage, fees, market impact, and latency.

---

## Objective

Build a trade simulation tool that calculates key trading metrics in real time using live L2 market data.

---

## Core Features

## UI Components

* **Left Panel (Inputs)**

  * Exchange (OKX)
  * Spot Asset (e.g., BTC-USDT)
  * Order Type (Market)
  * Quantity (in USD)
  * Volatility
  * Fee Tier

* **Right Panel (Outputs)**

  * Expected Slippage
  * Expected Fees
  * Expected Market Impact
  * Net Cost
  * Maker/Taker Ratio
  * Internal Latency

---

##  WebSocket Streaming

* **Endpoint**: `wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP`
* **Streamed Data**: Full L2 orderbook (bids and asks)
* **Data Processing**: Runs in a separate thread for real-time performance

---

## Model Implementations

## Slippage Estimation

* Based on top-level bid/ask spread
* Modulated by volatility input
* Simulates regression output without full training data

## Fee Estimation

* Rule-based model
* Adjusts based on provided fee tier (e.g., Tier 1, Tier 2, etc.)

## Market Impact (Almgren-Chriss Inspired)

* Based on order size and market volatility
* Uses square-root law for temporary impact

## Maker/Taker Ratio Prediction

* Logistic regression-inspired calculation
* Considers bid/ask dominance and recent spread tightening

##  Internal Latency

* Measured using `time.perf_counter()` before and after each tick's processing

---

##  Getting Started

### 🔧 Prerequisites

```bash
pip install websocket-client numpy scikit-learn
```

## Running the App

```bash
python trade_simulator_ui.py
```

Make sure you are connected to a VPN that allows access to OKX.

---

##  Project Structure

```
trade_simulator/
├── trade_simulator_ui.py         # Orderbook processing, threading
├── models.py            # Slippage, fees, market impact models
├── trade_simulator.py  # Real-time WebSocket listener
└── README.md            # This file

---

