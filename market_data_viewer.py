import pandas as pd
import talib
import pickle
import plotly.graph_objs as go
from plotly.subplots import make_subplots

database = 'jar/data.pkl'

# Open the file in binary read mode and use pickle to load the data
with open(database, 'rb') as file:
    data = pickle.load(file)

# Choose symbol logic
symbols = [symbol for symbol in data]
print("Available symbols: ", symbols)
symbol = None
while symbol not in symbols:
    symbol = input("Write symbol you want to plot: ")

# Choose timeframe logic
time_frames = [timeframe for timeframe in data[symbol]]
print("Available timeframes for choosen symbol: ", time_frames)
time_frame = None
while time_frame not in time_frames:
    time_frame = input("Choose time frame: ")


df = data[symbol][time_frame]

# Calculate the technical indicators
df['rsi'] = talib.RSI(df['close'], timeperiod=14)
df['macd'], _, df['signal'] = talib.MACD(
    df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['upper'], df['middle'], df['lower'] = talib.BBANDS(
    df['close'], timeperiod=20)
df['slowk'], df['slowd'] = talib.STOCH(df['high'], df['low'], df['close'],
                                       fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
df['adx'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
df['obv'] = talib.OBV(df['close'], df['tickVolume'])
df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)

# Convert the 'time' column to datetime
df['time'] = pd.to_datetime(df['time'])

# Create candlestick trace
candlestick_trace = go.Candlestick(
    x=df['time'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name="Candlestick"
)

# Create subplots (rows=12, cols=1)
fig = make_subplots(rows=12, cols=1, shared_xaxes=True, vertical_spacing=0.03)

# Add candlestick trace to the first subplot
fig.add_trace(candlestick_trace, row=1, col=1)
indicator_names = [
    'RSI', 'MACD', 'Signal', 'Upper BB', 'Middle BB', 'Lower BB',
    'Stoch SlowK', 'Stoch SlowD', 'ADX', 'OBV', 'ATR'
]
column_mapping = {
    'RSI': 'rsi',
    'MACD': 'macd',
    'Signal': 'signal',
    'Upper BB': 'upper',
    'Middle BB': 'middle',
    'Lower BB': 'lower',
    'Stoch SlowK': 'slowk',
    'Stoch SlowD': 'slowd',
    'ADX': 'adx',
    'OBV': 'obv',
    'ATR': 'atr'
}
# Create subplots (rows=12, cols=1)
fig = make_subplots(rows=12, cols=1, shared_xaxes=True,
                    vertical_spacing=0.03, row_heights=[0.7] + [0.1] * 11)

# Add candlestick trace to the first subplot
fig.add_trace(candlestick_trace, row=1, col=1)

# Create traces for each technical indicator
for i, name in enumerate(indicator_names, start=2):
    column_name = column_mapping[name]  # Get the corresponding column name
    trace = go.Scatter(x=df['time'], y=df[column_name], mode='lines', name=name)
    fig.add_trace(trace, row=i, col=1)

    # Set subplot titles
    fig.update_yaxes(title_text=name, row=i, col=1)

# Set layout settings
fig.update_layout(
    title=f"Choosen symbol and timeframe: {symbol} {time_frame}",
    xaxis_rangeslider_visible=False,
    showlegend=False
)

# Show the interactive chart
fig.show()
