import json
import time
import matplotlib.pyplot as plt
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

def fetch_historical_prices(contract, num_days=90, interval_hours=24):
    prices = []
    total_intervals = num_days * 24 // interval_hours  # Total number of intervals to fetch

    for i in range(total_intervals):
        # Fetch the latest round data
        latest_data = contract.functions.latestRoundData().call()
        price = latest_data[1] / 10**8  # Adjust for decimals
        prices.append(price)
        
        # Print the fetched price for debugging
        print(f"Fetched price {i + 1}/{total_intervals}: {price}")

        # Wait for the specified interval (in seconds)
        time.sleep(interval_hours * 3600)  # Convert hours to seconds

    return prices

# Fetch historical prices for the last 90 days
historical_prices = fetch_historical_prices(contract, num_days=90, interval_hours=24)

# Plotting the historical prices
plt.figure(figsize=(12, 6))
plt.plot(historical_prices, label='ETH/USD Price', color='blue')
plt.title('Historical ETH/USD Prices Over the Last 90 Days')
plt.xlabel('Time (Days)')
plt.ylabel('Price (USD)')
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# Now use historical_prices for further analysis
optimal_period = optimize_timeframe(historical_prices)
optimized_mean = calculate_ama(historical_prices, optimal_period)

# Print the results
print(f"Optimal Period: {optimal_period}")
print(f"Optimized Mean: {optimized_mean}")
