# Divisas.lat Python SDK

The official Python SDK for interacting with the Divisas.lat API.
This SDK is built with modern Python practices in mind, featuring complete type hints, `pydantic` validation, and native `httpx` integration for blazing-fast performance.

## Requirements
- Python 3.9 or higher

## Installation

```bash
pip install divisas-lat
```

## Features
- **Strict Validation**: All responses are validated and parsed using `pydantic` models.
- **Modern Networking**: Uses `httpx` under the hood.
- **Fluent API Builder**: An intuitive, chainable interface (`client.query().for_country()`).
- **Thread-Safe Caching**: Built-in memory cache that respects rate limits effortlessly.
- **Type Hints**: Fully typed for excellent autocompletion in VS Code, PyCharm, and Jupyter Notebooks.

## Basic Usage

```python
import os
from divisas_lat import DivisasClient, Country, Currency

# It will automatically read from the environment variable DIVISAS_API_KEY if present
client = DivisasClient(api_key="your_api_key_here")

# Get today's exchange rate for Guatemala
rates = client.query().for_country(Country.GUATEMALA).get_today()

print(f"Currency: {rates.rate.currency_code}")
print(f"Buy: {rates.rate.buy} | Sell: {rates.rate.sell}")

# Perform a conversion
conversion = client.query()\
    .for_country(Country.MEXICO)\
    .with_currency(Currency.USD)\
    .convert(Currency.MXN, 100.50)

print(f"100.50 USD is {conversion.result} MXN")
```

## Context Manager (Recommended)

To ensure connections are properly pooled and closed, use the client as a context manager:

```python
with DivisasClient() as client:
    res = client.query().for_country(Country.COSTA_RICA).get_today()
```

## CLI Usage

The SDK ships with a built-in command line interface!

```bash
# Check the exchange rate
divisas today GT USD

# Convert currencies
divisas convert 100 USD to GTQ in GT
```
