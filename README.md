# Exit Multileg Options Trading Script

## Overview
This Python script automates the process of exiting multileg options trades based on specified criteria. The code uses the Upstox API to retrieve live market data, monitor profit and loss (PNL) conditions, and execute exit orders when predefined stop-loss conditions are met.

---

## Features
* Fetches live market data for multiple option legs.
* Calculates MTM (Mark-to-Market) for each leg.
* Monitors total PNL and triggers exit orders upon stop-loss breach.
* Places market orders for both short and long legs of the strategy.
* Runs continuously until market close or exit conditions are met.

---

## Requirements

### Python Libraries
* `schedule`
* `time`
* `upstox_api`

### Upstox API Setup
To use this script, you must have an active Upstox account and API credentials:
* API Key
* API Secret
* Redirect URI

---

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/your-repo/exit-multileg-options.git
    ```
2. Install required libraries:
    ```bash
    pip install schedule upstox-api
    ```

---

## Configuration

### User Input
Update the following variables in the script before running:
```python
capital = 100000
short_avg_price = 100
long_avg_price = 50
quantities = 75
short_leg_strike_price = ""  # Enter the short leg strike price
long_leg_strike_price = ""   # Enter the long leg strike price
```

### Upstox API Credentials
Replace the placeholders with your API credentials in the `UPSTOX SETUP` section:
```python
s = Session ('your_api_key')
s.set_redirect_uri ('your_redirect_uri')
s.set_api_secret ('your_api_secret')
```
---

## Usage

### Steps to Run
1. Authenticate your session by logging into the Upstox API:
    * Generate a login URL:
        ```python
        print(s.get_login_url())
        ```
    * Login using your UCC ID and password.
    * Retrieve the code from the login response and update it in the script:
        ```python
        s.set_code('your_code_from_login_response')
        ```
2. Run the script:
    ```bash
    python exit_multileg_options.py
    ```
3. The script will:
    * Continuously fetch live market data.
    * Monitor PNL and exit positions upon stop-loss breach.

---

## Key Components

### Exit Criteria
Calculates MTM for short and long legs and evaluates total PNL:
```python
def exit():
    short_leg_live_mrkt_price = u.get_live_feed(u.get_instrument_by_symbol('NSE_FO', short_leg_strike_price), LiveFeedType.LTP)
    long_leg_live_mrkt_price = u.get_live_feed(u.get_instrument_by_symbol('NSE_FO', long_leg_strike_price), LiveFeedType.LTP)
    
    MTM_short_leg = quantities * (short_avg_price - short_leg_live_mrkt_price)
    MTM_long_leg = quantities * (-(long_avg_price - long_leg_live_mrkt_price))
    total_PNL = MTM_short_leg + MTM_long_leg

    if(total_PNL <= (-(0.018 * capital))):
        print("Stop Loss hit!")
        exit_order()
```

### Exit Orders
Places market orders to close positions:
```python
def exit_order():
    u.place_order(TransactionType.Buy, u.get_instrument_by_symbol('NSE_FO', short_leg_strike_price), quantities, OrderType.Market, ProductType.Delivery, 0.0, None, 0, DurationType.DAY, None, None, None)
    time.sleep(1.2)
    u.place_order(TransactionType.Sell, u.get_instrument_by_symbol('NSE_FO', long_leg_strike_price), quantities, OrderType.Market, ProductType.Delivery, 0.0, None, 0, DurationType.DAY, None, None, None)
    check = True
    print("Orders Executed")
```

### Continuous Monitoring
Uses the `schedule` library to monitor live data at intervals:
```python
schedule.every(0.1).seconds.do(exit)
while check == False:
    schedule.run_pending()
    time.sleep(0.1)
```

---

## Notes
* Ensure that Upstox API access is enabled for your account.
* The script currently supports NSE_FO instruments.
* Modify the code to include additional features or custom exit criteria as required.

---

## Disclaimer
This script is for educational purposes only. Use it at your own risk. Ensure compliance with trading regulations and consult with your broker before executing automated trading strategies.

