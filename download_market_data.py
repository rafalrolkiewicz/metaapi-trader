import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from datetime import datetime, timedelta, timezone
import pickle
from dotenv import load_dotenv
import pandas as pd
import message_sender as telegram

# Load environment variables from a .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Default domain for the MetaApi service
domain = os.getenv('DOMAIN') or 'agiliumtrade.agiliumtrade.ai'


class MetaApiHandler:
    """Handles MetaApi connection and trading operations."""

    def __init__(self, token, account_id):
        """Initialize the MetaApiHandler.

        Args:
            token (str): MetaApi token.
            account_id (str): MetaTrader account ID.
        """
        self.token = token
        self.account_id = account_id
        self.api = MetaApi(token, {'domain': domain})
        self.account = None

    async def connect(self):
        """Connect to MetaApi and wait for synchronization."""
        try:
            self.account = await self.api.metatrader_account_api.get_account(self.account_id)
            #  wait until account is deployed and connected to broker
            print('Deploying account')
            if self.account.state != 'DEPLOYED':
                await self.account.deploy()
            else:
                print('Account already deployed')

            # Connect to the MetaApi service and MetaTrader account
            print('Waiting for API server to connect to broker')
            if self.account.connection_status != 'CONNECTED':
                await self.account.wait_connected()

            # Connect to MetaApi API
            self.connection = self.account.get_rpc_connection()
            await self.connection.connect()

            # Wait until terminal state synchronized to the local state
            print('Waiting for SDK to synchronize to terminal state')
            await self.connection.wait_synchronized()

            print("Connected!")

        except:
            print("Connection failed")

    async def connection_status(self):
        status = self.account.connection_status
        return status

    async def server_time(self):
        try:
            server_time = await self.connection.get_server_time()
            return server_time

        except:
            print("Couldn't get server time")
            return None

    async def disconnect(self):
        if self.account:
            try:
                await self.connection.close()
                print("Disconnected!")
                exit()

            except:
                print("Couldn't disconnect!")

    async def get_candles(self, symbol, resolution, start_time, limit):
        try:
            candles = await self.account.get_historical_candles(symbol, resolution, start_time, limit)
            return candles

        except:
            print("Error, couldn't download candle history")
            return None

    async def get_candle(self, symbol, resolution):
        try:
            # there is third parameter, keep subscription
            candle = await self.connection.get_candle(symbol, resolution)
            return candle

        except:
            return None

    async def get_symbols(self):
        try:
            symbols = await self.connection.get_symbols()
            return symbols

        except:
            print("Error, couldn't download symbols")
            return None

    async def get_account_info(self):
        try:
            info = await self.connection.get_account_information()
            currency = info["currency"]
            balance = info["balance"]
            equity = info["equity"]
            margin = info["margin"]
            free_margin = info["freeMargin"]
            leverage = info["leverage"]
            return currency, balance, equity, margin, free_margin, leverage

        except:
            print("Error, couldn't get account informations")
            return None

    async def positions(self):
        try:
            positions = await self.connection.get_positions()
            return positions

        except:
            print("Error, couldn't get positions")
            return None

    async def orders(self):
        try:
            orders = await self.connection.get_orders()
            return orders

        except:
            print("Error, couldn't get orders")
            return None

    async def history_orders(self, days):
        try:
            history_orders = await self.connection.get_history_orders_by_time_range(datetime.utcnow() - timedelta(days=days), datetime.utcnow())
            return history_orders

        except:
            print("Error, couldn't get orders history")
            return None

    async def history_deals(self, days):
        try:
            history_deals = await self.connection.get_deals_by_time_range(datetime.utcnow() - timedelta(days=days), datetime.utcnow())
            return history_deals

        except:
            print("Error, couldn't get deals history")
            return None

    async def open_buy_position(self, symbol, volume):
        try:
            position = await self.connection.create_market_buy_order(symbol=symbol, volume=volume)
            # print(f"Opened position {position.id}")
            print("Position details: ", position)

        except Exception as e:
            print(f"Error opening position: {str(e)}")

    async def open_sell_position(self, symbol, volume):
        try:
            position = await self.connection.create_market_sell_order(symbol=symbol, volume=volume)
            print(f"Opened position {position.id}")
            print("Position details: ", position)

        except Exception as e:
            print(f"Error opening position: {str(e)}")

    async def close_position(self, id):
        try:
            await self.connection.close_position(id)
            print(f"Closed position {id}")

        except Exception as e:
            print(f"Error closing position: {str(e)}")

    async def close_order(self, id):
        try:
            # Close an existing order by its ID
            await self.connection.cancel_order(id)
            print(f"Closed order {id}")

        except Exception as e:
            print(f"Error closing order: {str(e)}")

    async def calculate_margin(self, symbol, buysell, volume, price):
        if buysell == "buy":
            buysell = 'ORDER_TYPE_BUY'
        elif buysell == "sell":
            buysell = 'ORDER_TYPE_SELL'

        try:
            margin = await self.connection.calculate_margin({
                'symbol': symbol,
                'type': buysell,
                'volume': volume,
                'openPrice': price
            })
            return margin

        except:
            print("Error, couldn't get calculated margin")
            return None

    async def get_symbol_price(self, symbol):
        try:
            price = await self.connection.get_symbol_price(symbol)
            return price

        except:
            print("Error, couldn't get symbol price")
            return None

    async def get_symbol_info(self, symbol):
        try:
            symbol_info = await self.connection.get_symbol_specification(symbol)
            return symbol_info

        except:
            print("Error, couldn't get symbol informations")
            return None


def data_pickle(data, file_name):
    file_name += '.pkl'
    # Open the file in binary write mode and use pickle to dump the data
    with open(file_name, 'wb') as file:
        pickle.dump(data, file)
    print("Data pickled.")


def data_unpickle(file_name):
    file_name += '.pkl'
    try:
        # Open the file in binary read mode and use pickle to load the data
        with open(file_name, 'rb') as file:
            data = pickle.load(file)
        return data

    except:
        print("Error, couldn't unpickle given file")
        return None


async def download_market_data(metaapi, symbol, resolution, to_time):
    data = data_unpickle("jar/data")

    pages = 1000
    started_at = datetime.now().timestamp()

    print(f"Downloading {symbol} {resolution}")
    start_time = datetime.now(timezone.utc)
    server_tz = timezone(timedelta(hours=2))
    to_time = to_time.replace(tzinfo=server_tz).astimezone(timezone.utc)

    candles = []
    quantity = 0
    # Intervals in minutes:
    candle_intervals = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240,
        "1d": 1440,
        "1w": 10080,
        "1mn": 43200,
    }
    candle_interval = candle_intervals[resolution]

    # Initialize the candle count
    candle_count = 0

    # Calculate the number of selected candles within the time range
    current_time = to_time

    while current_time <= start_time:
        if (current_time - to_time).total_seconds() % (candle_interval * 60) == 0:
            candle_count += 1
        current_time += timedelta(minutes=1)

    # Maximum number of candles that can be downloaded at once is 1000
    if candle_count > 1000:
        quantity = 1000
    else:
        quantity = candle_count

    # Update candles in database:
    for page in range(pages):
        # the API to retrieve historical market data is currently available for G1 only
        new_candles = await metaapi.get_candles(symbol, resolution, start_time, quantity)
        if not new_candles:
            print("Candles over")
            break

        for i in range(len(new_candles)):
            candles.insert(i, new_candles[i])

        start_time = new_candles[0]['time']

        if start_time < to_time:
            print("Reached data from database")
            break
        print("Page:", page+1, end="\r")

    if candles:
        df = pd.DataFrame(candles)

        # Convert the 'Time' column to datetime format
        df['time'] = pd.to_datetime(df['time'])

        # Sort the DataFrame based on the 'Time' column
        df = df.sort_values(by='time')

        # Drop duplicates from DataFrame
        df = df.drop_duplicates(subset=['time'], keep='first')

        df = df[df['time'] > to_time]

        historic_df = data[symbol][resolution]
        df_joined = pd.concat([historic_df, df])
        data[symbol][resolution] = df_joined
        data_pickle(data, "jar/data")

    print(f'Downloaded data. Took {(datetime.now().timestamp() - started_at)}s')


def check_last_data_entry(symbol, resolution):
    data = data_unpickle("jar/data")
    df = data[symbol][resolution]
    last = df["time"].iloc[-1].to_pydatetime()

    return last


async def update_all_data(metaapi):
    data = data_unpickle("jar/data")
    for symbol in data:
        for resolution in data[symbol]:
            to_time = check_last_data_entry(symbol, resolution)
            await download_market_data(metaapi, symbol, resolution, to_time)
    await telegram.send_message_async("Data updated")


async def main():
    # Initialize MetaApi handler
    metaapi = MetaApiHandler(TOKEN, ACCOUNT_ID)

    # Connect to MetaApi
    await metaapi.connect()

    # Update data
    await update_all_data(metaapi)

    # Available symbols
    # symbols = await metaapi.get_symbols()
    # print(symbols)

    # Symbol price and info
    # print("Symbol price: ", await metaapi.get_symbol_price("EURUSD"))
    # print("Symbol info: ", await metaapi.get_symbol_info("EURUSD"))

    # Get open positions:
    # print("Positions:", await metaapi.positions())

    # Get pending orders:
    # print("Orders:", await metaapi.orders())

    # History of orders:
    # print("History orders:", await metaapi.history_orders(90))

    # History of deals:
    # print("History deals:", await metaapi.history_deals(90))

    # Testing opening buy position:
    # await metaapi.open_buy_position("EURUSD", 1)
    # await metaapi.close_position("2573829")

    # Disconnect from MetaApi
    await metaapi.disconnect()


# Run the program
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
