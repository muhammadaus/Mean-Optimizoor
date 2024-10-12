import json
from web3 import Web3

# Load the ABI from the JSON file
with open('ETHUSD_abi.json') as abi_file:
    abi = json.load(abi_file)

# Connect to an Ethereum node
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/i7akc0vyVBtMOsw8eA-IldtASnCzPpL0'))

# Address of the Chainlink Price Feed contract
address = '0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419'  # ETH/USD price feed address

# Create contract instance
contract = w3.eth.contract(address=address, abi=abi)

# Call the latestRoundData function
latest_data = contract.functions.latestRoundData().call()
price_data = latest_data[1] / 10**8  # Adjust for decimals

print(f"ETH/USD price: ${price_data}")

def calculate_ama(prices, period, fast_period=2, slow_period=30):
    er = efficiency_ratio(prices, period)
    fast_sc = 2 / (fast_period + 1)
    slow_sc = 2 / (slow_period + 1)
    sc = er * (fast_sc - slow_sc) + slow_sc
    ama = [prices[0]]
    for i in range(1, len(prices)):
        ama.append(ama[-1] + sc * (prices[i] - ama[-1]))
    return ama

def efficiency_ratio(prices, period):
    direction = abs(prices[-1] - prices[-period])
    volatility = sum(abs(prices[i] - prices[i-1]) for i in range(-1, -period, -1))
    return direction / volatility if volatility != 0 else 0

def optimize_timeframe(prices, initial_period=14, max_period=200):
    period = initial_period
    touches = 0
    while period <= max_period:
        ama = calculate_ama(prices, period)
        new_touches = sum(1 for p, a in zip(prices, ama) if abs(p - a) < 0.0001)
        if new_touches > touches:
            touches = new_touches
            optimal_period = period
        period += 1
    return optimal_period

# Assuming you have a function to fetch historical prices
def fetch_historical_prices(contract, num_prices):
    prices = []
    for i in range(num_prices):
        # Fetch the latest round data
        latest_data = contract.functions.latestRoundData().call()
        price = latest_data[1] / 10**8  # Adjust for decimals
        prices.append(price)
        # You may want to add a delay or wait for the next price update
    return prices

# Fetch historical prices (e.g., the last 100 prices)
historical_prices = fetch_historical_prices(contract, 100)

# Now use historical_prices instead of price_data
optimal_period = optimize_timeframe(historical_prices)
optimized_mean = calculate_ama(historical_prices, optimal_period)
