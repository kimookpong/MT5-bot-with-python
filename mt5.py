import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import MetaTrader5 as mt5
import threading
import time
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd


trading_bot_status = False
on_process_buy = False
on_process_sell = False

completed_order = 0
completed_profit = 0


def get_onprocess(type):
    global on_process_buy
    global on_process_sell
    if type == "buy":
        return on_process_buy
    elif type == "sell":
        return on_process_sell
def set_onprocess(type, value):
    global on_process_buy
    global on_process_sell
    if type == "buy":
        on_process_buy = value
    elif type == "sell":
        on_process_sell = value

def get_stat(type):
    global completed_order
    global completed_profit
    if type == "order":
        return completed_order
    elif type == "profit":
        return completed_profit
    
def set_stat(type, value):
    global completed_order
    global completed_profit
    if type == "order":
        completed_order = value
    elif type == "profit":
        completed_profit = value

def get_status():
    global trading_bot_status
    return trading_bot_status

def set_status(status):
    global trading_bot_status
    trading_bot_status = status

# Create the main window
root = tk.Tk()
root.title("MT5 Trading Bot")
# root.geometry("1000x500")

# Create frames
left_frame = tk.Frame(root, width=200)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

right_frame = tk.Frame(root, width=800)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Account number label and entry
tk.Label(left_frame, text="Account Number:").pack(pady=(5, 0))
account_entry = tk.Entry(left_frame, width=40)
account_entry.pack(pady=(0))
account_entry.insert(0, "182809343")  # Default account number

# Password label and entry
tk.Label(left_frame, text="Password:").pack(pady=(5, 0))
password_entry = tk.Entry(left_frame, show="*", width=40)
password_entry.pack(pady=(0))
password_entry.insert(0, "")  # Default password

# Server label and entry
tk.Label(left_frame, text="Server:").pack(pady=(5, 0))
server_entry = tk.Entry(left_frame, width=40)
server_entry.pack(pady=(0))
server_entry.insert(0, "Exness-MT5Trial6")  # Default server

# Connect and Disconnect buttons in the same row
button_frame = tk.Frame(left_frame)
button_frame.pack(pady=10)

connect_button = tk.Button(button_frame, text="Connect", command=lambda: connect_to_mt5())
connect_button.grid(row=0, column=0, padx=5)

disconnect_button = tk.Button(button_frame, text="Disconnect", state="disabled", command=lambda: disconnect_mt5())
disconnect_button.grid(row=0, column=1, padx=5)


param_frame = tk.Frame(left_frame)
param_frame.pack(pady=10)

# make select list of symbols
tk.Label(param_frame, text="Symbols:").grid(row=0, column=0, sticky="w",padx=5,columnspan=2)
symbol_var = tk.StringVar(value="BTCUSDm")  # Pre-fill Symbol
symbol_dropdown = ttk.Combobox(param_frame, textvariable=symbol_var, values=[], state="disabled", width=17)
symbol_dropdown.grid(row=1, column=0, sticky="w",padx=5,columnspan=2)


tk.Label(param_frame, text="Interval:").grid(row=0, column=2, sticky="w",padx=5,columnspan=2)
interval_var = tk.StringVar(value="15m") 
interval_dropdown = ttk.Combobox(param_frame, textvariable=interval_var, values=["1m", "5m", "15m", "30m","1h","4h","1d"], state="disabled", width=17)
interval_dropdown.grid(row=1, column=2, sticky="w",padx=5,columnspan=2)

tk.Label(param_frame, text="Lots:").grid(row=2, column=0, sticky="w",padx=5,columnspan=2)
lot_var = tk.Entry(param_frame, width=20)
lot_var.grid(row=3, column=0, sticky="w",padx=5,columnspan=2)
lot_var.insert(0, "0.01")
lot_var.config(state="disabled")

tk.Label(param_frame, text="Limit order:").grid(row=2, column=2, sticky="w",padx=5,columnspan=2)
max_order_var = tk.Entry(param_frame, width=20)
max_order_var.grid(row=3, column=2, sticky="w",padx=5,columnspan=2)
max_order_var.insert(0, "20")
max_order_var.config(state="disabled")

tk.Label(param_frame, text="Fast EMA:").grid(row=4, column=0, sticky="w",padx=5)
fast_ema_var = tk.Entry(param_frame, width=8)
fast_ema_var.grid(row=5, column=0, sticky="w",padx=5)
fast_ema_var.insert(0, "12")
fast_ema_var.config(state="disabled")

tk.Label(param_frame, text="Slow EMA:").grid(row=4, column=1, sticky="w",padx=5)
slow_ema_var = tk.Entry(param_frame, width=8)
slow_ema_var.grid(row=5, column=1, sticky="w",padx=5)
slow_ema_var.insert(0, "26")
slow_ema_var.config(state="disabled")

tk.Label(param_frame, text="Signal line:").grid(row=4, column=2, sticky="w",padx=5)
signal_var = tk.Entry(param_frame, width=8)
signal_var.grid(row=5, column=2, sticky="w",padx=5)
signal_var.insert(0, "9")
signal_var.config(state="disabled")

tk.Label(param_frame, text="RSI:").grid(row=4, column=3, sticky="w",padx=5)
rsi_var = tk.Entry(param_frame, width=8)
rsi_var.grid(row=5, column=3, sticky="w")
rsi_var.insert(0, "14")
rsi_var.config(state="disabled")

button_bot = tk.Frame(left_frame)
button_bot.pack(pady=10)
# Start Bot button
start_bot_button = tk.Button(button_bot, text="Start Bot", state="disabled", command=lambda: start_bot())
start_bot_button.grid(row=0, column=0, padx=5)

# Start Bot button
pause_bot_button = tk.Button(button_bot, text="Pause Bot", state="disabled", command=lambda: pause_bot())
pause_bot_button.grid(row=0, column=1, padx=5)



usdt_balance_label = tk.Label(left_frame, text="Current USDT Balance: --")
usdt_balance_label.pack(pady=0)

current_price_label = tk.Label(left_frame, text="Current Price (--): --")
current_price_label.pack(pady=0)

time_elapsed_label = tk.Label(left_frame, text="Elapsed Time: --")
time_elapsed_label.pack(pady=0)

process_order_label = tk.Label(left_frame, text="Processing order: --")
process_order_label.pack(pady=0)

process_type_label = tk.Label(left_frame, text="Order type: --")
process_type_label.pack(pady=0)

trading_completed_label = tk.Label(left_frame, text="Completed order: --")
trading_completed_label.pack(pady=0)


# Right Frame: Graph and Log
fig = Figure(figsize=(6, 2))
ax = fig.add_subplot(111)
ax.tick_params(axis='x', labelsize=7)  # Set x-axis tick font size
ax.tick_params(axis='y', labelsize=7)  # Set y-axis tick font size
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

fig2 = Figure(figsize=(6, 2))
ax2 = fig2.add_subplot(111)
ax2.tick_params(axis='x', labelsize=7)  # Set x-axis tick font size
ax2.tick_params(axis='y', labelsize=7)  # Set y-axis tick font size
canvas2 = FigureCanvasTkAgg(fig2, master=right_frame)
canvas2.get_tk_widget().pack(fill="both", expand=True)


# Create a text box for logging in the right frame
log_text = tk.Text(right_frame, height=20, width=80, wrap="word")
log_text.config(font=("Helvetica", 7), state="disabled")
log_text.pack(fill="both", expand=True)
log_text.tag_config("green", foreground="green")
log_text.tag_config("red", foreground="red")
log_text.tag_config("blue", foreground="blue")
log_text.tag_config("grey", foreground="grey")
log_text.tag_config("yellow", foreground="yellow")

# Function to log messages
def log_message(message, color="black"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text.config(state="normal")
    log_text.insert(tk.END,timestamp + " | " + message + "\n",color)
    log_text.config(state="disabled")
    log_text.see(tk.END)

def account_balace():
    # Get account balance
    account_info = mt5.account_info()
    if account_info is not None:
        balance = account_info.balance
        usdt_balance_label.config(text=f"Current USDT Balance: {balance} USD")

# Function to handle MT5 connection
def connect_to_mt5():
    account_number = account_entry.get()
    password = password_entry.get()
    server = server_entry.get()

    if not account_number or not password or not server:
        # messagebox.showwarning("Warning", "Please fill in all fields.")
        log_message("[WARNING] Please fill in all fields.")
        return

    log_message("[INFO] Initializing MT5...", "blue")
    if not mt5.initialize(login=int(account_number), password=password, server=server):
        error_message = f"[ERROR] MT5 Initialization failed: {mt5.last_error()}"
        # messagebox.showerror("Error", error_message)
        log_message(error_message, "red")
        return

    log_message("[INFO] Logging in to MT5...", "blue")
    if not mt5.login(int(account_number), password=password, server=server):
        error_message = f"[ERROR] Login failed: {mt5.last_error()}"
        # messagebox.showerror("Error", error_message)
        log_message(error_message, "red")
        mt5.shutdown()
        return

    success_message = "[SUCCESS] Successfully connected to MT5!"
    account_balace()
    # messagebox.showinfo("Success", success_message)
    log_message(success_message, "green")
    log_available_symbols()
    connect_button.config(state="disabled")
    disconnect_button.config(state="normal")
    start_bot_button.config(state="normal")

    account_entry.config(state="disabled")
    password_entry.config(state="disabled")
    server_entry.config(state="disabled")

    symbol_dropdown.config(state="readonly")
    interval_dropdown.config(state="readonly")
    lot_var.config(state="normal")
    max_order_var.config(state="normal")

    fast_ema_var.config(state="normal")
    slow_ema_var.config(state="normal")
    signal_var.config(state="normal")
    rsi_var.config(state="normal")

# Function to handle MT5 disconnection
def disconnect_mt5():
    log_message("[INFO] Shutting down MT5...", "blue")
    mt5.shutdown()
    log_message("[SUCCESS] Successfully disconnected from MT5!", "green")
    # messagebox.showinfo("Disconnected", "Successfully disconnected from MT5!")
    connect_button.config(state="normal")
    disconnect_button.config(state="disabled")
    start_bot_button.config(state="disabled")

    account_entry.config(state="normal")
    password_entry.config(state="normal")
    server_entry.config(state="normal")

    symbol_dropdown.config(state="disabled")
    interval_dropdown.config(state="disabled")
    lot_var.config(state="disabled")
    max_order_var.config(state="disabled")

    fast_ema_var.config(state="disabled")
    slow_ema_var.config(state="disabled")
    signal_var.config(state="disabled")
    rsi_var.config(state="disabled")



# Function to start the bot
def start_bot():
    set_status(True)
    log_message("[INFO] Starting trading bot...")
    bot_thread = threading.Thread(target=run_trading_bot, daemon=True)
    bot_thread.start()
    start_bot_button.config(state="disabled")
    pause_bot_button.config(state="normal")


# Function to pause the bot
def pause_bot():
    set_status(False)
    log_message("[INFO] Pausing trading bot...")
    # bot_thread = threading.Thread(target=run_trading_bot, daemon=True)
    # bot_thread.start()
    start_bot_button.config(state="normal")
    pause_bot_button.config(state="disabled")

def log_available_symbols():
    symbols = mt5.symbols_get()
    # log_message("[INFO] Available symbols:")
    for symbol in symbols:
        # log_message(f"  {symbol.name}")
        # Update symbol dropdown with available symbols
        available_symbols = [symbol.name for symbol in symbols]
        symbol_dropdown.config(values=available_symbols)

def trading_buy():

    trading_close()

    set_onprocess("buy", True)
    set_onprocess("sell", False)

    symbol = symbol_var.get()
    lot_size = float(lot_var.get())
    price = mt5.symbol_info_tick(symbol).ask 
    deviation = 10 
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "Python Buy Order",
        "type_time": mt5.ORDER_TIME_GTC, 
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        log_message(f"[BOT] Buy order executed successfully", "green")
    else:
        log_message(f"[ERROR] Buy order failed: {result}", "red")

def trading_sell():
    trading_close()
    set_onprocess("buy", False)
    set_onprocess("sell", True)

    symbol = symbol_var.get()
    lot_size = float(lot_var.get())
    price = mt5.symbol_info_tick(symbol).bid 
    deviation = 10 
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "Python Sell Order",
        "type_time": mt5.ORDER_TIME_GTC, 
        "type_filling": mt5.ORDER_FILLING_IOC,  
    }
    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        log_message(f"[BOT] Sell order executed successfully", "green")
    else:
        log_message(f"[ERROR] Sell order failed: {result}", "red")

def trading_close():
    symbol = symbol_var.get() 
    positions = mt5.positions_get(symbol=symbol) 
    if positions is None or len(positions) == 0:
        log_message(f"[INFO] No open positions to close for {symbol}.", "blue")
        return
    log_message(f"[INFO] Closing all open positions for {symbol}...", "blue")
    for position in positions:
        ticket = position.ticket
        volume = position.volume
        price = (
            mt5.symbol_info_tick(symbol).bid
            if position.type == mt5.ORDER_TYPE_BUY
            else mt5.symbol_info_tick(symbol).ask
        )
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "volume": volume,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,  # Reverse the type to close
            "price": price,
            "deviation": 10, 
            "magic": 234000,
            "comment": "Python Close Order",
        }
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            log_message(
                f"[SUCCESS] Closed position {ticket} for {symbol}. Volume: {volume}, Profit: {position.profit:.2f} USD",
                "green",
            )
            set_stat("order", get_stat("order") + 1)
            set_stat("profit", get_stat("profit") + float(position.profit))

            max_order = max_order_var.get()
            if get_stat("order") >= int(max_order):
                log_message(f"[INFO] limit order reached. Stop bot!!", "blue")
                disconnect_mt5()
                return
            
        else:
            log_message(
                f"[ERROR] Failed to close position {ticket} for {symbol}. Error: {result}",
                "red",
            )


# Trading bot logic
def run_trading_bot():
    symbol = symbol_var.get()
    symbol = symbol_var.get()
    interval = interval_var.get()
    start_time = datetime.now()
    
    
    while get_status():
        elapsed_time = (datetime.now() - start_time).total_seconds()
        hours, remainder = divmod(int(elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_elapsed_label.config(text=f"Elapsed Time: {hours} hour {minutes} min {seconds} sec")

        account_balace()
        if not mt5.symbol_select(symbol, True):
            log_message(f"[ERROR] Unable to select symbol {symbol}", "red")
            return
        df = get_candlestick_data(symbol, interval, 200)
        poth_graph(symbol,df.tail(80))
        signal_time = df.index[-1]
        macd_prev2,macd_prev, macd_curr = df['MACD'].iloc[-2], df['MACD'].iloc[-2], df['MACD'].iloc[-1]
        signal_prev2, signal_prev, signal_curr = df['Signal'].iloc[-2], df['Signal'].iloc[-2], df['Signal'].iloc[-1]

        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        balance = df['close'].iloc[-1]
        
        
        current_price_label.config(text=f"Current {symbol} price: {balance} USD")
        trading_completed_label.config(text=f"Completed order: {get_stat('order')}  (Profit: {get_stat('profit'):.2f} USD)")

        order_type = "None"
        if get_onprocess("buy"):
            order_type = "Buy"
        elif get_onprocess("sell"):
            order_type = "Sell"
        process_type_label.config(text=f"Order type: {order_type}")
        positions=mt5.positions_get(symbol=symbol)
        process_order_label.config(text=f"Processing order: 0 (Profit: 0 USD)")
        if len(positions)>0:
            total_profit = 0
            for position in positions:
                # timeStart = pd.to_datetime(position.time, unit='s')
                # volume = position.volume
                profit = float(position.profit)
                total_profit = total_profit + profit
                # if profit>0:
                #     log_message(f">>> [ORDER] {timeStart} | {volume} lots | Profit: {profit}", "green")
                # else:
                #     log_message(f">>> [ORDER] {timeStart} | {volume} lots | Profit: {profit}", "red")
            process_order_label.config(text=f"Processing order: {len(positions)} (Profit: {total_profit:.2f} USD)")

        if macd_prev < signal_prev and macd_curr > signal_curr and not get_onprocess("buy") and macd_curr > macd_prev:
            log_message(f"[BOT] Current: {current_time} | Signal time: {signal_time} | Current Price {balance}",'grey')
            trading_buy()
        elif macd_prev > signal_prev and macd_curr < signal_curr and not get_onprocess("sell") and macd_curr < macd_prev:
            log_message(f"[BOT] Current: {current_time} | Signal time: {signal_time} | Current Price {balance}",'grey')
            trading_sell()

        # Simulate bot actions with a 5-second interval
        time.sleep(10)

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    # Calculate short and long EMAs
    short_ema = data['close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['close'].ewm(span=long_window, adjust=False).mean()
    
    # Calculate MACD and Signal Line
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    
    return macd, signal

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_candlestick_data(symbol, timeframe, num_bars):
    timeframeList = {
        "1m": mt5.TIMEFRAME_M1,
        "5m": mt5.TIMEFRAME_M5,
        "15m": mt5.TIMEFRAME_M15,
        "30m": mt5.TIMEFRAME_M30,
        "1h": mt5.TIMEFRAME_H1,
        "4h": mt5.TIMEFRAME_H4,
        "1d": mt5.TIMEFRAME_D1,
    }
    rates = mt5.copy_rates_from_pos(symbol, timeframeList[timeframe], 0, num_bars)
    if rates is None:
        log_message(f"[ERROR] Unable to get candlestick data for {symbol}", "red")
        return []
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')
    df.set_index('time', inplace=True)
    df['MACD'], df['Signal'] = calculate_macd(df, short_window=int(fast_ema_var.get()), long_window=int(slow_ema_var.get()), signal_window=int(signal_var.get()))
    df['RSI'] = calculate_rsi(df['close'], window=int(rsi_var.get()))
    return df
    # poth graph into ax
    
   
def poth_graph(symbol, data):
    ax.clear()

    # ohlc_data = data[['open', 'high', 'low', 'close']]
    # mpf.plot(
    #     ohlc_data,
    #     ax=ax,
    #     type='candle',
    #     style='charles',
    #     title=f"{symbol} Price",
    #     ylabel="Price",
    #     xrotation=20,
    #     datetime_format='%H:%M'
    # )

    ax.plot(data.index, data['close'], label=symbol, color="blue",linewidth=1)
    latest_close_value = data['close'].iloc[-1]
    latest_close_time = data.index[-1]
    ax.annotate(
        f"{latest_close_value:.2f}", 
        (latest_close_time, latest_close_value), 
        textcoords="offset points", 
        xytext=(0,5),
        ha='center', 
        color="blue", 
        fontsize=8
        )
    # ax.set_title(f"{symbol} Price")
    ax.set_xlabel("Time",fontsize=7)
    ax.set_ylabel("Price",fontsize=7)
    ax.legend(fontsize=7)
    canvas.draw()

    ax2.clear()
    ax2.plot(data.index, data['MACD'], label="#1", color="brown", linewidth=1)
    ax2.plot(data.index, data['Signal'], label="#2", color="purple", linewidth=1)
    ax2.plot(data.index, data['RSI'], label="#3", color="orange", linewidth=1)
    latest_macd_value = data['MACD'].iloc[-1]
    latest_signal_value = data['Signal'].iloc[-1]
    lastest_rsi_value = data['RSI'].iloc[-1]
    latest_time = data.index[-1]
    ax2.annotate(
        f"{latest_macd_value:.2f}", 
        (latest_time, latest_macd_value), 
        textcoords="offset points", 
        xytext=(0,2), 
        ha='center', 
        color="brown", 
        fontsize=7
    )

    ax2.annotate(
        f"{latest_signal_value:.2f}", 
        (latest_time, latest_signal_value), 
        textcoords="offset points", 
        xytext=(0,2), 
        ha='center', 
        color="purple", 
        fontsize=7
    )

    ax2.annotate(
        f"{lastest_rsi_value:.2f}", 
        (latest_time, lastest_rsi_value), 
        textcoords="offset points", 
        xytext=(0,2), 
        ha='center', 
        color="orange", 
        fontsize=7
    )
    # ax2.set_title(f"{symbol} Indicator")
    ax2.set_xlabel("Time",fontsize=7)
    ax2.set_ylabel("Value",fontsize=7)
    ax2.legend(fontsize=7)
    canvas2.draw()

# Run the application
root.mainloop()
