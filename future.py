import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
import MetaTrader5 as mt5
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import threading

# Initialize MetaTrader 5 connection
account_number = "182809343"
password = "Est#89HK"
server = "Exness-MT5Trial6"

if not mt5.initialize(login=int(account_number), password=password, server=server):
    print("initialize() failed")
    mt5.shutdown()
if not mt5.login(int(account_number), password=password, server=server):
    print("login() failed")
    mt5.shutdown()

# Dash app setup
app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='candlestick-chart'),
    dcc.Interval(
        id='interval-component',
        interval=5000,  # Update every 5 seconds
        n_intervals=0
    ),
    html.Div(id='signal-indicator')
])

# Data fetching and processing
def fetch_data():
    rates = mt5.copy_rates_from_pos('BTCUSDm', mt5.TIMEFRAME_M5, 0, 500)
    if rates is None:
        return pd.DataFrame()
    df = pd.DataFrame(rates)

    # Calculate indicators
    df['RSI'] = ta.rsi(df['close'], length=12)
    df['EMA'] = ta.ema(df['close'], length=150)

    # Add EMASignal
    EMAsignal = [0] * len(df)
    backcandles = 15
    for row in range(backcandles, len(df)):
        upt = 1
        dnt = 1
        for i in range(row - backcandles, row + 1):
            if max(df.open[i], df.close[i]) >= df.EMA[i]:
                dnt = 0
            if min(df.open[i], df.close[i]) <= df.EMA[i]:
                upt = 0
        if upt and dnt:
            EMAsignal[row] = 3
        elif upt:
            EMAsignal[row] = 2
        elif dnt:
            EMAsignal[row] = 1
    df['EMASignal'] = EMAsignal

    # Add isPivot and pointpos
    def isPivot(candle, window):
        if candle - window < 0 or candle + window >= len(df):
            return 0
        pivotHigh = 1
        pivotLow = 2
        for i in range(candle - window, candle + window + 1):
            if df.iloc[candle].low > df.iloc[i].low:
                pivotLow = 0
            if df.iloc[candle].high < df.iloc[i].high:
                pivotHigh = 0
        if pivotHigh and pivotLow:
            return 3
        elif pivotHigh:
            return pivotHigh
        elif pivotLow:
            return pivotLow
        else:
            return 0

    def pointpos(row):
        if row['isPivot'] == 2:
            return row['low'] - 1e-3
        elif row['isPivot'] == 1:
            return row['high'] + 1e-3
        else:
            return np.nan

    df['isPivot'] = df.index.map(lambda x: isPivot(x, window=5))
    df['pointpos'] = df.apply(pointpos, axis=1)

    return df

# Function to check buy or sell signal based on current data
def get_signal(df):
    latest_data = df.iloc[-1]

    # Buy condition based on RSI and EMA
    if latest_data['RSI'] < 30 and latest_data['close'] > latest_data['EMA']:
        return "Buy Signal (RSI < 30, Price above EMA)"

    # Sell condition based on RSI and EMA
    elif latest_data['RSI'] > 70 and latest_data['close'] < latest_data['EMA']:
        return "Sell Signal (RSI > 70, Price below EMA)"
    
    # Neutral condition
    else:
        return "No Clear Signal"

# Callback to update the chart
@app.callback(
    [Output('candlestick-chart', 'figure'),
     Output('signal-indicator', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_chart(n):
    df = fetch_data()

    if df.empty:
        return go.Figure(), "No data available"

    # Convert the Unix timestamp to a datetime format for better x-axis representation
    df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')

    # Select a range for visualization
    dfpl = df.tail(200)

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=dfpl['time'],  # Use 'time' as the x-axis
        open=dfpl['open'],
        high=dfpl['high'],
        low=dfpl['low'],
        close=dfpl['close']
    )])

    # Add the EMA line
    fig.add_trace(go.Scatter(
        x=dfpl['time'],
        y=dfpl['EMA'],
        mode='lines',
        name='EMA (150)',
        line=dict(color='orange', width=1)
    ))

    # Add buy and sell signals
    buy_signals = dfpl[(dfpl['isPivot'] == 2) & (dfpl['EMASignal'] == 2)]
    sell_signals = dfpl[(dfpl['isPivot'] == 1) & (dfpl['EMASignal'] == 1)]
    close_signals = dfpl[((dfpl['isPivot'] == 1) & (dfpl['EMASignal'] == 2)) | ((dfpl['isPivot'] == 2) & (dfpl['EMASignal'] == 1))]

    fig.add_scatter(x=close_signals['time'], y=close_signals['close'], mode="markers",
                    marker=dict(size=10, color="blue", symbol="x"),
                    name="Close Signal")

    fig.add_scatter(x=buy_signals['time'], y=buy_signals['low'], mode="markers",
                    marker=dict(size=10, color="green", symbol="triangle-up"),
                    name="Buy Signal")

    fig.add_scatter(x=sell_signals['time'], y=sell_signals['high'], mode="markers",
                    marker=dict(size=10, color="red", symbol="triangle-down"),
                    name="Sell Signal")

    fig.update_layout(
        title="BTC/USD Candlestick Chart",
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            title="Time",  # Label the x-axis as Time
            tickformat="%H:%M:%S",  # Format the time to show hour, minute, and second
            tickangle=45  # Rotate time labels for better readability
        )
    )

    # Add current price annotation
    fig.add_annotation(
        x=df['time'].iloc[-1],
        y=df['close'].iloc[-1],
        text=f"Current Price: {df['close'].iloc[-1]}",
        showarrow=True,
        arrowhead=1
    )

    # Get the latest buy/sell signal based on the logic
    signal = get_signal(df)

    return fig, signal


# Run the app
if __name__ == '__main__':
    threading.Thread(target=app.run_server, kwargs={"debug": True, "use_reloader": False}).start()
