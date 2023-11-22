# Algo Trading Platform

This project aims to provide an algorithmic trading platform that allows users to access and analyze market data, test and implement trading strategies, and interact with the MetaTrader platform. Almost all brokers allow trading using MetaTrader. My platform currently supports downloading market data and viewing it using various technical analysis indicators from the `talib` library.

## Features

- Update historical market data for all available symbols and timeframes through your broker. Currently, I am downloading data for 102 symbols, each with 9 timeframes, as I am using the demo version.

- View market data with technical analysis indicators using `talib`.

- Future Features:
  - Backtest trading strategies.
  - Execute trading strategies on live data.
  - Analyze the performance of trading strategies.

## Getting Started

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up environment variables in a `.env` file:


## Usage

To utilize the Algo Trading Platform, you'll need to follow these steps:

### 1. Broker Account

Ensure that you have an active trading account with a broker that supports the MetaTrader platform. Most brokers offer MetaTrader as a trading platform option.

### 2. MetaTrader Account

Open a MetaTrader account with your chosen broker if you don't have one already. This will be the account you use for executing trades and accessing market data.

### 3. MetaApi Account

Create an account with MetaApi, the service that bridges the gap between MetaTrader and your trading application. Visit the [MetaApi website](https://metaapi.cloud/) to sign up.

### 4. Connect MetaTrader to MetaApi

After creating your MetaApi account, you'll need to link your MetaTrader account to your MetaApi account. This connection enables your trading strategies to interact with MetaTrader.

### 5. Obtain MetaApi Token

Once your MetaTrader account is connected to MetaApi, you'll receive an authentication token. This token is used to establish secure communication between your application and MetaApi.

### 6. Set Up Environment Variables

In the root directory of the project, create a `.env` file to store your environment variables:
- `TOKEN`: MetaApi token
- `ACCOUNT_ID`: MetaTrader account ID
- `DOMAIN`: MetaApi service domain (optional, defaults to `agiliumtrade.agiliumtrade.ai`)

If you want also to use telegram bot, provide also:
- `TELEGRAM_TOKEN`: Telegram bot token
- `TELEGRAM_CHAT_ID`: Telegram chat ID


### Downloading Data

The program for updating market data is `download_market_data.py`. Run the program to download historical market data and update database for all available symbols and timeframes.

```bash
python download_data.py
```

The Algo Trading Platform utilizes a structured data storage approach to efficiently manage and organize market data. The data is stored within a dictionary structure that facilitates easy access and manipulation.

- At the top level, the data is organized by symbols. Each symbol corresponds to a financial instrument, such as a currency pair or a stock.
- For each symbol, there is a dictionary of timeframes. Timeframes represent the intervals at which market data is captured, such as 1 minute, 15 minutes, 1 hour, etc.
- Within each timeframe dictionary, the market data is stored as a Pandas DataFrame. This DataFrame contains columns such as 'time', 'open', 'high', 'low', 'close', and 'volume'.

This hierarchical structure ensures efficient retrieval and storage of market data, making it easy to perform various analyses and visualizations on historical and real-time data.

The flexibility of this data storage approach allows for seamless integration of additional symbols, timeframes, and data sources as the platform evolves.

The platform employs pickle files to save and load the structured data efficiently. The data is serialized into pickle files, allowing for seamless persistence between sessions and easy backup of historical market data.

The flexibility of this data storage approach allows for seamless integration of additional symbols, timeframes, and data sources as the platform evolves.

### Viewing data

To view market data with technical analysis indicators, follow these steps:

1. Run the `view_data.py` script using Python:

```bash
python view_data.py
```

2. The script will prompt you to enter the symbol you want to analyze. Provide the symbol of the financial instrument you are interested in (e.g., EURUSD, AAPL, etc.).

3. Next, the script will prompt you to choose a timeframe. Enter the timeframe for analysis (e.g., 1h, 15m, 4h, etc.).

4. The script provides the flexibility to choose from a comprehensive range of over 150 technical analysis indicators available through the talib library. Right now script provides a predefined set of 11 technical analysis indicators for visualization. These indicators include:
- RSI
- MACD
- Signal
- Upper Bollinger Band (BB)
- Middle Bollinger Band (BB)
- Lower Bollinger Band (BB)
- Stochastic SlowK
- Stochastic SlowD
- Average Directional Index (ADX)
- On-Balance Volume (OBV)
- Average True Range (ATR)

5. You can hard code the specific indicators you wish to visualize in the script. Select indicators that align with your trading strategy and analysis requirements.
6. Explore the chart to gain insights into market trends and potential trading opportunities based on your customized analysis.

## On-Going Development

The Algo Trading Platform is an evolving project, with new features and enhancements being actively developed. I'm dedicated to expanding the platform's capabilities, refining its user experience, and incorporating valuable feedback from the trading community.

Stay tuned for exciting updates as I continue to enhance the platform's functionalities, add more technical analysis indicators, and introduce features like backtesting and live trading capabilities.

## Contribution

I welcome contributions from traders, developers, and enthusiasts. If you have ideas, find issues, or want to add new features, please open issues or submit pull requests. Let's collaborate to make the platform even more powerful and user-friendly.

Stay tuned for updates and new features as we continue to enhance the Algo Trading Platform. Your feedback and involvement are instrumental as we evolve and expand our offerings. Happy trading!
