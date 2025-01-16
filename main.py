import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread, Event
from binance.client import Client
import time
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mplfinance as mpf
import queue

# Define global stop event and thread-safe queue
stop_event = Event()
update_queue = queue.Queue()
is_open_order = False
completed_order_count = 0
symbol_price = 0.0

order_buy_qty = 0.0
order_sell_qty = 0.0
order_profit = 0.0

def set_order_profit(profit):
    global order_profit
    order_profit = profit

def get_order_profit():
    global order_profit
    return order_profit

def set_order_qty(action,qty):
    global order_buy_qty
    global order_sell_qty
    if action == 'buy':
        order_buy_qty = qty
    elif action == 'sell':
        order_sell_qty = qty

def get_order_qty(action):
    global order_buy_qty
    global order_sell_qty
    if action == 'buy':
        return order_buy_qty
    elif action == 'sell':
        return order_sell_qty


def get_current_symbol_price():
    global symbol_price
    return symbol_price

def set_current_symbol_price(price):
    global symbol_price
    symbol_price = price

def get_current_order_count():
    global completed_order_count
    return completed_order_count

def increase_current_order_count():
    global completed_order_count
    completed_order_count = completed_order_count + 1

def get_current_order_status():
    global is_open_order
    return is_open_order

def set_current_order_status(status):
    global is_open_order
    is_open_order = status

def get_account_balance(client, crypto='USDT'):
    try:
        balance = client.get_asset_balance(asset=crypto)
        if balance['asset'] == crypto:
            return float(balance['free'])
    except Exception as e:
        log_text.insert(tk.END, f"Error fetching account balance: {e}\n")
    return 0.0

def get_current_price(client, symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        log_text.insert(tk.END, f"Error fetching current price: {e}\n")
        return 0.0
# Define trading bot functions
def get_candlestick_data(client, symbol, interval):
    klines = client.get_klines(symbol=symbol, interval=interval)
    df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                       'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                       'Taker buy quote asset volume', 'Ignore'])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')
    df.set_index('Open time', inplace=True)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric)
    return df

def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = calculate_ema(data['Close'], short_window)
    long_ema = calculate_ema(data['Close'], long_window)
    macd_line = short_ema - long_ema
    signal_line = calculate_ema(macd_line, signal_window)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=window).mean().fillna(0)
    avg_loss = loss.rolling(window=window).mean().fillna(0)
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def place_buy_order(client, symbol, quantity):
    try:
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        return order
    except Exception as e:
        log_text.insert(tk.END, f"Error placing buy order: {e}\n")
        return None

def place_sell_order(client, symbol, quantity):
    try:
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
        return order
    except Exception as e:
        log_text.insert(tk.END, f"Error placing sell order: {e}\n")
        return None

def update_graph(df, ax, canvas,ax2, canvas2):
    try:
        ax.clear()  # Clear previous plots
        ax2.clear()

        # Plot closing prices as a line chart
        ax.plot(df.index[-50:], df['Close'].tail(50), label="Close", linewidth=1)
         # Annotate the latest value of 'Close'
        latest_close_value = df['Close'].iloc[-1]
        latest_close_time = df.index[-1]
        ax.annotate(
            f"{latest_close_value:.2f}", 
            (latest_close_time, latest_close_value), 
            textcoords="offset points", 
            xytext=(0,5),
            ha='center', 
            color="blue", 
            fontsize=8
        )

   
        ax2.plot(df.index[-50:], df['MACD'].tail(50), label="#1", color="red", linewidth=1)
        ax2.plot(df.index[-50:], df['Signal'].tail(50), label="#2", color="green", linewidth=1)


        # Annotate the latest values of MACD and Signal
        latest_macd_value = df['MACD'].iloc[-1]
        latest_signal_value = df['Signal'].iloc[-1]
        latest_time = df.index[-1]
        ax2.annotate(
            f"{latest_macd_value:.2f}", 
            (latest_time, latest_macd_value), 
            textcoords="offset points", 
            xytext=(0,5), 
            ha='center', 
            color="red", 
            fontsize=7
        )

        ax2.annotate(
            f"{latest_signal_value:.2f}", 
            (latest_time, latest_signal_value), 
            textcoords="offset points", 
            xytext=(0,5), 
            ha='center', 
            color="green", 
            fontsize=7
        )

        ax.set_title("Price",fontsize=10)
        ax.set_xlabel("Time",fontsize=7)
        ax.set_ylabel("Price",fontsize=7)
        ax.legend(fontsize=7)  # Add legend

        ax2.set_title("Indecator",fontsize=10)
        ax2.set_xlabel("Time",fontsize=7)
        ax2.set_ylabel("Value",fontsize=7)
        ax2.legend(fontsize=7)  # Add legend

        # Redraw the canvas
        canvas.draw_idle()
        canvas2.draw_idle()
    except Exception as e:
        log_text.insert(tk.END, f"Error updating graph: {e}\n")

def run_trading(client, symbol, interval, macd_params, rsi_window, log_widget, ax, canvas,ax2, canvas2):
    short_window, long_window, signal_window = macd_params
    is_position_open = False

    position_quantity = 0.001  # Adjust as needed

    log_widget.insert(tk.END, f"Starting bot for {symbol} with interval {interval}...\n")
    log_widget.insert(tk.END, f"MACD{macd_params}, RSI({rsi_window})\n")
    log_widget.insert(tk.END, "*********************************\n","blue")


    def update_loop():
        nonlocal is_position_open
        try:
            # Fetch data
            df = get_candlestick_data(client, symbol, interval)
            df['MACD'], df['Signal'], df['Histogram'] = calculate_macd(df, short_window, long_window, signal_window)
            df['RSI'] = calculate_rsi(df)

            # Update the graph
            update_graph(df, ax, canvas,ax2, canvas2)

            # Trading logic
            macd_prev, macd_curr = df['MACD'].iloc[-2], df['MACD'].iloc[-1]
            signal_prev, signal_curr = df['Signal'].iloc[-2], df['Signal'].iloc[-1]

            if macd_prev < signal_prev and macd_curr > signal_curr and not is_position_open:
                # Buy signal
                order = place_buy_order(client, symbol, position_quantity)
                if order:
                    currentTime = datetime.now().strftime("%H:%M:%S")
                    log_widget.insert(tk.END, f"{currentTime} | {symbol}: {df['Close'].iloc[-1]} | #1: {df['MACD'].iloc[-1]:.2f} #2: {df['Signal'].iloc[-1]:.2f} #3: {df['RSI'].iloc[-1]:.2f}\n")
                    cumulative_quote_quantity = order.get('cummulativeQuoteQty')
                    set_order_qty('buy',cumulative_quote_quantity)
                    log_widget.insert(tk.END, f"Buy order done!: {cumulative_quote_quantity}\n")
                    is_position_open = True
                    set_current_order_status(True)

            elif macd_prev > signal_prev and macd_curr < signal_curr and is_position_open:
                # Sell signal
                order = place_sell_order(client, symbol, position_quantity)
                if order:
                    currentTime = datetime.now().strftime("%H:%M:%S")
                    log_widget.insert(tk.END, f"{currentTime} | {symbol}: {df['Close'].iloc[-1]} | #1: {df['MACD'].iloc[-1]:.2f} #2: {df['Signal'].iloc[-1]:.2f} #3: {df['RSI'].iloc[-1]:.2f}\n")
                    order_sell_qty = float(order.get('cummulativeQuoteQty'))
                    order_buy_qty = float(get_order_qty('buy'))
                    calculate_profit = order_sell_qty - order_buy_qty
                    log_widget.insert(tk.END, f"Sell order done!: {order_sell_qty} ")
                    if calculate_profit > 0:
                        log_widget.insert(tk.END, f" ({calculate_profit})\n","green")
                    else:
                        log_widget.insert(tk.END, f" ({calculate_profit})\n","red")
                    is_position_open = False
                    set_current_order_status(False)
                    increase_current_order_count()

        except Exception as e:
            log_widget.insert(tk.END, f"Error in trading loop: {e}\n")

        if not stop_event.is_set():
            canvas.get_tk_widget().after(60000, update_loop)

    update_loop()

def update_balance_time_profit(client, symbol, start_time, starting_balance):
    """
    Continuously updates the account balance, elapsed time, and profit/loss.

    Args:
        client: Binance API client object.
        symbol (str): The trading pair symbol (e.g., BTCUSDT).
        start_time (datetime): The start time of the bot.
        starting_balance (float): Initial USDT balance at the start of the bot.
    """
    while not stop_event.is_set():
        try:
            # Fetch current USDT balance
            current_balance = get_account_balance(client, 'USDT')
            
            # Fetch current price of the trading symbol
            current_price = get_current_price(client, symbol)
            
            # Calculate elapsed time
            elapsed_time = (datetime.now() - start_time).total_seconds()
            minutes, seconds = divmod(int(elapsed_time), 60)
            
            # Calculate profit or loss
            completed_count = get_current_order_count()
            
            if get_current_order_status():
                is_open_order = 'Ordering'
                profit = 'Waiting for order'
            else:
                is_open_order = 'No order'
                profit = f"{(current_balance - starting_balance):.2f} USDT"
            # Add updates to the queue for thread-safe GUI updates
            update_queue.put({
                "usdt_balance": f"Current USDT Balance: {current_balance:.2f}",
                "current_price": f"Current Price ({symbol}): {current_price:.2f}",
                "elapsed_time": f"Elapsed Time: {minutes} min {seconds} sec",
                "profit": f"Profit/Loss: {profit}",
                "process_order": f"Processing order: {is_open_order}",
                "trading_completed": f"Completed order: {completed_count}",
            })

        except Exception as e:
            # Add error messages to the queue
            update_queue.put({
                "usdt_balance": "Error fetching balance",
                "current_price": f"Error fetching price for {symbol}",
                "elapsed_time": "Error calculating time",
                "profit": "Error calculating profit",
                "process_order": "Error calculating process order",
                "trading_completed": "Error calculating completed order"
            })
            log_text.insert(tk.END, f"Error in update_balance_time_profit: {e}\n")

        # Wait for 1 second before updating again
        time.sleep(10)


def process_queue_updates():
    """
    Processes updates from the queue and updates the Tkinter widgets.
    """
    try:
        while not update_queue.empty():
            update = update_queue.get_nowait()
            usdt_balance_label.config(text=update["usdt_balance"])
            current_price_label.config(text=update["current_price"])
            time_elapsed_label.config(text=update["elapsed_time"])
            profit_label.config(text=update["profit"])
            process_order_label.config(text=update["process_order"])
            trading_completed_label.config(text=update["trading_completed"])
    except Exception as e:
        log_text.insert(tk.END, f"Error processing updates: {e}\n")
    # Schedule the next check for the queue
    root.after(100, process_queue_updates)

def start_bot(api_key, secret_key, symbol, interval, macd_params, rsi_window,testnet):
    
    client = Client(api_key, secret_key, testnet=testnet)
    starting_balance = get_account_balance(client, 'USDT')  # Function call
    start_time = datetime.now()
    Thread(
        target=update_balance_time_profit,
        args=(client, symbol, start_time, starting_balance),
        daemon=True
    ).start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    run_trading(client, symbol, interval, macd_params, rsi_window, log_text, ax, canvas,ax2, canvas2)
    process_queue_updates()

def launch_bot():
    api_key = api_key_entry.get()
    secret_key = secret_key_entry.get()
    symbol = symbol_var.get()
    interval = interval_var.get()
    testnet = testnet_var.get()
    try:
        short_window = int(short_window_entry.get())
        long_window = int(long_window_entry.get())
        signal_window = int(signal_window_entry.get())
        rsi_window = int(rsi_window_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "MACD and RSI parameters must be integers!")
        return

    if not api_key or not secret_key or not symbol or not interval:
        messagebox.showerror("Input Error", "Please fill all fields!")
        return

    macd_params = (short_window, long_window, signal_window)

    Thread(
        target=start_bot,
        args=(api_key, secret_key, symbol, interval, macd_params, rsi_window,testnet),
        daemon=True
    ).start()


def connect_bot():
    api_key = api_key_entry.get()
    secret_key = secret_key_entry.get()
    testnet = testnet_var.get()
    client = Client(api_key, secret_key, testnet=testnet)
    try:
        account = client.get_account()
        asset = client.get_asset_balance(asset='USDT')
        if asset['free']:
            balance = asset['free']
        else:
            balance = 0.0
        log_text.insert(tk.END, f"Connection successful!!: ",'blue')
        log_text.insert(tk.END, f"USDT balance: {balance}\n",'grey')
        # start_button enable
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
    except Exception as e:
        log_text.insert(tk.END, f"Connection failed!\n",'red')
        start_button.config(state=tk.DISABLED)

def stop_bot():
    stop_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


# Initialize tkinter window
root = tk.Tk()
root.title("SPOT Trading Bot")

icon_path = "icon.ico"
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"Error loading icon: {e}")

# Create frames
left_frame = tk.Frame(root, width=200)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

right_frame = tk.Frame(root, width=100)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Default values
default_api_key = "g5twmlsil0MggnT4VIn9oo5ivcv874ZQwf08CdvPBhPGwZVVFprlIuq7FLAjhw8U"  # Replace with your actual API Key
default_secret_key = "7Kw4xjf4LoBLsVZ8T3D3ANnrlZATPnjzkcKXvwjKBlQFaQVbEoxfZRnzYgIwb61G"  # Replace with your actual Secret Key
default_symbol = "BTCUSDT"
default_interval = "15m"
default_short_window = "12"  # Default MACD Short EMA window
default_long_window = "26"  # Default MACD Long EMA window
default_signal_window = "9"  # Default MACD Signal line window
default_rsi_window = "14"  # Default RSI calculation windowtk.Label(left_frame, text="API Key:").grid(row=0, column=0, sticky="w")

tk.Label(left_frame, text="API Key:").grid(row=0, column=0, sticky="w")
api_key_entry = tk.Entry(left_frame, width=35)
api_key_entry.insert(0, default_api_key)  # Pre-fill API Key
api_key_entry.grid(row=0, column=1, pady=5)

tk.Label(left_frame, text="Secret Key:").grid(row=1, column=0, sticky="w")
secret_key_entry = tk.Entry(left_frame, width=35, show="*")
secret_key_entry.insert(0, default_secret_key)  # Pre-fill Secret Key
secret_key_entry.grid(row=1, column=1, pady=5)


tk.Label(left_frame, text="Symbol:").grid(row=2, column=0, sticky="w")
symbol_var = tk.StringVar(value=default_symbol)  # Pre-fill Symbol
symbol_dropdown = ttk.Combobox(left_frame, textvariable=symbol_var, values=["BTCUSDT", "ETHUSDT","BNBUSDT","GALAUSDT","XRPUSDT","DOGEUSDT"], state="readonly", width=33)
symbol_dropdown.grid(row=2, column=1, pady=5)

tk.Label(left_frame, text="Interval:").grid(row=3, column=0, sticky="w")
interval_var = tk.StringVar(value=default_interval) 
interval_dropdown = ttk.Combobox(left_frame, textvariable=interval_var, values=["1m", "5m", "15m", "30m"], state="readonly", width=33)
interval_dropdown.grid(row=3, column=1, pady=5)

tk.Label(left_frame, text="Indecator #1:").grid(row=4, column=0, sticky="w")
short_window_entry = tk.Entry(left_frame, width=35)
short_window_entry.insert(0, default_short_window) 
short_window_entry.grid(row=4, column=1, pady=5)

tk.Label(left_frame, text="Indecator #2:").grid(row=5, column=0, sticky="w")
long_window_entry = tk.Entry(left_frame, width=35)
long_window_entry.insert(0, default_long_window) 
long_window_entry.grid(row=5, column=1, pady=5)

tk.Label(left_frame, text="Indecator #3:").grid(row=6, column=0, sticky="w")
signal_window_entry = tk.Entry(left_frame, width=35)
signal_window_entry.insert(0, default_signal_window)
signal_window_entry.grid(row=6, column=1, pady=5)

tk.Label(left_frame, text="Indecator #4:").grid(row=7, column=0, sticky="w")
rsi_window_entry = tk.Entry(left_frame, width=35)
rsi_window_entry.insert(0, default_rsi_window)
rsi_window_entry.grid(row=7, column=1, pady=5)

tk.Label(left_frame, text="Type:").grid(row=8, column=0, sticky="w")
radioBox = tk.Frame(left_frame)
testnet_var = tk.BooleanVar(value=True)
testnet_radio_yes = tk.Radiobutton(radioBox, text="Testnet", variable=testnet_var, value=True)
testnet_radio_yes.grid(row=0, column=0)
testnet_radio_no = tk.Radiobutton(radioBox, text="Product", variable=testnet_var, value=False)
testnet_radio_no.grid(row=0, column=1)
radioBox.grid(row=8, column=1, sticky="w")

connect_button = tk.Button(left_frame, text="Connect", command=connect_bot)
connect_button.grid(row=9, column=0, pady=10)
start_button = tk.Button(left_frame, text="Start Bot", command=launch_bot, state=tk.DISABLED)
start_button.grid(row=9, column=1, pady=10)
stop_button = tk.Button(left_frame, text="Stop Bot", command=stop_bot, state=tk.DISABLED)
stop_button.grid(row=9, column=2, pady=10)

usdt_balance_label = tk.Label(left_frame, text="Current USDT Balance: --")
usdt_balance_label.grid(row=10, column=0, columnspan=2)

current_price_label = tk.Label(left_frame, text="Current Price (--): --")
current_price_label.grid(row=11, column=0, columnspan=2)

time_elapsed_label = tk.Label(left_frame, text="Elapsed Time: --")
time_elapsed_label.grid(row=12, column=0, columnspan=2)

profit_label = tk.Label(left_frame, text="Profit/Loss: --")
profit_label.grid(row=13, column=0, columnspan=2)

process_order_label = tk.Label(left_frame, text="Processing order: --")
process_order_label.grid(row=14, column=0, columnspan=2)

trading_completed_label = tk.Label(left_frame, text="Completed order: --")
trading_completed_label.grid(row=15, column=0, columnspan=2)

# Right Frame: Graph and Log
fig = Figure(figsize=(6, 2))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

fig2 = Figure(figsize=(6, 2))
ax2 = fig2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(fig2, master=right_frame)
canvas2.get_tk_widget().pack(fill="both", expand=True)


ax.tick_params(axis='x', labelsize=7)  # Set x-axis tick font size
ax.tick_params(axis='y', labelsize=7)  # Set y-axis tick font size
ax2.tick_params(axis='x', labelsize=7)  # Set x-axis tick font size
ax2.tick_params(axis='y', labelsize=7)  # Set y-axis tick font size

log_text = tk.Text(right_frame, height=10, width=70)
log_text.config(font=("Helvetica", 8))
log_text.pack(fill="both", expand=True)
log_text.tag_config("green", foreground="green")
log_text.tag_config("red", foreground="red")
log_text.tag_config("blue", foreground="blue")
log_text.tag_config("grey", foreground="grey")

# Start the Tkinter main loop
root.mainloop()
