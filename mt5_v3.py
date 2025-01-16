import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import MetaTrader5 as mt5
import numpy as np
import threading
import time
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go


period_count = 0
period_time = 0

def set_period(count,time):
    global period_count
    global period_time
    period_count = count
    period_time = time

def get_period():
    global period_count
    global period_time
    return period_count,period_time

trading_bot_status = False

completed_order = 0
completed_profit = 0

count_order = 0
last_order_time = None

trigger_price = 0
def set_trigger_price(price):
    global trigger_price
    trigger_price = price

def get_trigger_price():
    global trigger_price
    return trigger_price

def set_last_order_time(time):
    global last_order_time
    last_order_time = time

def get_last_order_time():
    global last_order_time
    return last_order_time


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
root.title("MT5 Trading Bot V.3")
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
password_entry.insert(0, "Est#89HK")  # Default password

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
tk.Label(param_frame, text="Symbols").grid(row=0, column=0, sticky="w",padx=5,columnspan=2)
symbol_var = tk.StringVar(value="BTCUSDm")  # Pre-fill Symbol
symbol_dropdown = ttk.Combobox(param_frame, textvariable=symbol_var, values=["XAUUSDm","BTCUSDm"], state="disabled", width=17)
symbol_dropdown.grid(row=1, column=0, sticky="w",padx=5,columnspan=2)


tk.Label(param_frame, text="Interval").grid(row=0, column=2, sticky="w",padx=5,columnspan=2)
interval_var = tk.StringVar(value="5m") 
interval_dropdown = ttk.Combobox(param_frame, textvariable=interval_var, values=["1m", "5m", "15m", "30m","1h","4h","1d"], state="disabled", width=17)
interval_dropdown.grid(row=1, column=2, sticky="w",padx=5,columnspan=2)

tk.Label(param_frame, text="Lots").grid(row=2, column=0, sticky="w",padx=5,columnspan=2)
lot_var = tk.Entry(param_frame, width=20)
lot_var.grid(row=3, column=0, sticky="w",padx=5,columnspan=2)
lot_var.insert(0, "0.01")
lot_var.config(state="disabled")

tk.Label(param_frame, text="Trigger").grid(row=2, column=2, sticky="w",padx=5)
trigger_var = tk.Entry(param_frame, width=9)
trigger_var.grid(row=3, column=2, sticky="w",padx=5)
trigger_var.insert(0, "5")
trigger_var.config(state="disabled")

tk.Label(param_frame, text="Limit").grid(row=2, column=3, sticky="w",padx=5)
max_order_var = tk.Entry(param_frame, width=9)
max_order_var.grid(row=3, column=3, sticky="w",padx=5)
max_order_var.insert(0, "100")
max_order_var.config(state="disabled")

tk.Label(param_frame, text="Indicator").grid(row=4, column=0, sticky="w",padx=5,columnspan=4)
indicator_var = tk.StringVar(value="SUPERTREND") 
indicator_dropdown = ttk.Combobox(param_frame, textvariable=indicator_var, values=["BULLMARKET", "BOLLINGER","SUPERTREND","DONCHAIN"], state="disabled", width=40)
indicator_dropdown.grid(row=5, column=0, sticky="w",padx=5,columnspan=4)





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

time_elapsed_label = tk.Label(left_frame, text="Elapsed Time: --")
time_elapsed_label.pack(pady=0)

period_count_label = tk.Label(left_frame, text="Period count: --")
period_count_label.pack(pady=0)


# Right Frame: Status and Log

status_frame = tk.Frame(right_frame)
status_frame.pack(pady=10, padx=10, fill="x")
status_frame.columnconfigure(0, weight=1)
status_frame.columnconfigure(1, weight=1)
status_frame.columnconfigure(2, weight=1)
status_frame.columnconfigure(3, weight=1)

# Column 1: Trend
tk.Label(status_frame, text="Period Time", anchor="center").grid(row=0, column=0, padx=10, pady=0,sticky="nsew")
trend_label = tk.Label(status_frame, text="-", anchor="center", font=("Helvetica", 16))
trend_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

# Column 2: Trend2
tk.Label(status_frame, text="Current Price", anchor="center").grid(row=0, column=1, padx=10, pady=0,sticky="nsew")
current_price_label = tk.Label(status_frame, text="-", anchor="center", font=("Helvetica", 16))
current_price_label.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

# Column 2: Trend2
tk.Label(status_frame, text="Pending", anchor="center").grid(row=0, column=2, padx=10, pady=0,sticky="nsew")
process_order_label = tk.Label(status_frame, text="-", anchor="center", font=("Helvetica", 16))
process_order_label.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

# Column 2: Trend2
tk.Label(status_frame, text="Profit/Loss", anchor="center").grid(row=0, column=3, padx=10, pady=0,sticky="nsew")
trading_completed_label = tk.Label(status_frame, text="-", anchor="center", font=("Helvetica", 16))
trading_completed_label.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")

# Right Frame: Graph and Log
fig = Figure(figsize=(8, 3))
fig.subplots_adjust(left=0, right=0.95, top=1, bottom=0.08)
ax = fig.add_subplot()
# ax.yaxis.set_tick_params(labelsize=0)
ax.tick_params(axis='x', labelsize=5)
ax.tick_params(axis='y', labelsize=5)
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)



# Create a text box for logging in the right frame
log_text = tk.Text(right_frame, height=15, width=80, wrap="word")
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
    # log_available_symbols()
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
    trigger_var.config(state="normal")
    indicator_dropdown.config(state="readonly")



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
    trigger_var.config(state="disabled")
    indicator_dropdown.config(state="disabled")





# Function to start the bot
def start_bot():
    set_status(True)
    log_message("[INFO] Starting trading bot...")
    bot_thread = threading.Thread(target=run_trading_bot, daemon=True)
    bot_thread.start()
    start_bot_button.config(state="disabled")
    pause_bot_button.config(state="normal")

    symbol_dropdown.config(state="disabled")
    interval_dropdown.config(state="disabled")
    lot_var.config(state="disabled")
    max_order_var.config(state="disabled")
    trigger_var.config(state="disabled")
    indicator_dropdown.config(state="disabled")




# Function to pause the bot
def pause_bot():
    set_status(False)
    log_message("[INFO] Pausing trading bot...")
    # bot_thread = threading.Thread(target=run_trading_bot, daemon=True)
    # bot_thread.start()
    start_bot_button.config(state="normal")
    pause_bot_button.config(state="disabled")

    symbol_dropdown.config(state="readonly")
    interval_dropdown.config(state="readonly")
    lot_var.config(state="normal")
    max_order_var.config(state="normal")
    trigger_var.config(state="normal")
    indicator_dropdown.config(state="readonly")





def trading_buy(current_time):

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
        set_last_order_time(current_time)
        set_trigger_price(0)
    else:
        log_message(f"[ERROR] Buy order failed: {result}", "red")

def trading_sell(current_time):
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
        set_last_order_time(current_time)
        set_trigger_price(0)
    else:
        log_message(f"[ERROR] Sell order failed: {result}", "red")

def trading_close(position,current_time):
        symbol = symbol_var.get() 
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
            # set_last_order_time(current_time)

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
    interval = interval_var.get()
    start_time = datetime.now()
    indicator = indicator_var.get()
    
    
    while get_status():
        elapsed_time = (datetime.now() - start_time).total_seconds()
        hours, remainder = divmod(int(elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_elapsed_label.config(text=f"Elapsed Time: {hours} hour {minutes} min {seconds} sec")

        account_balace()
        if not mt5.symbol_select(symbol, True):
            log_message(f"[ERROR] Unable to select symbol {symbol}", "red")
            return
        df = get_candlestick_data(symbol, interval, 1000)
        poth_graph(symbol,df.tail(250),indicator)

        current_time = df.index[-1]
        period_count,period_time = get_period()
        trend_label.config(text=current_time.strftime("%Y-%m-%d %H:%M"))

        if(current_time != period_time):
            period_count = period_count + 1
            set_period(period_count,current_time)
        balance = df['close'].iloc[-1]
        current_price_label.config(text=f"{balance} USD")
        period_count_label.config(text=f"Period count: {period_count}")
        # log_message(f"[BOT] Time: {current_time}", "blue")

        if get_stat('profit') < 0:
            trading_completed_label.config(text=f"{get_stat('profit'):.2f} USD", fg="red")
        else:
            trading_completed_label.config(text=f"{get_stat('profit'):.2f} USD", fg="green")

        positions=mt5.positions_get(symbol=symbol)
        process_order_label.config(text=f"0 (0.00)")

        if len(positions) > 0:
            total_profit = 0

            for position in positions:
                profit = float(position.profit)
                total_profit = total_profit + profit
            if total_profit < 0:
                process_order_label.config(text=f"{len(positions)} ({total_profit:.2f} USD)", fg="red")
            else:
                process_order_label.config(text=f"{len(positions)} ({total_profit:.2f} USD)", fg="green")
        
        if indicator == "BULLMARKET":
            EMA21_curr,EMA21_prev = df['EMA21'].iloc[-1], df['EMA21'].iloc[-2]
            SMA20_curr,SMA20_prev = df['SMA20'].iloc[-1], df['SMA20'].iloc[-2]

            if len(positions) > 0:
                for position in positions:
                    if(profit < get_trigger_price()  and get_trigger_price() > 0):
                        trading_close(position,current_time)
                    elif EMA21_curr > SMA20_curr and EMA21_prev < SMA20_prev and current_time != get_last_order_time():
                        trading_close(position,current_time)
                    elif EMA21_curr < SMA20_curr and EMA21_prev > SMA20_prev  and current_time != get_last_order_time():
                        trading_close(position,current_time)
                    else:
                        lots = float(lot_var.get()) * 100
                        if profit > (get_trigger_price() + (2*lots)) and profit > (2*lots):
                            trigger_profit = get_trigger_price() + (1*lots)
                            set_trigger_price(trigger_profit)
                            log_message(f"[BOT] Trigger Profit: {trigger_profit}", "blue")
            # EMA's cross to the upside make buy order
            if EMA21_curr > SMA20_curr and EMA21_prev < SMA20_prev and current_time != get_last_order_time():
                trading_buy(current_time)
                log_message("[BMSB] Buy order executed")
            # EMA's cross to the downside make sell order
            elif EMA21_curr < SMA20_curr and EMA21_prev > SMA20_prev  and current_time != get_last_order_time():
                trading_sell(current_time)
                log_message("[BMSB] Sell order executed")

        elif indicator == "BOLLINGER":
            UpperBand_curr,UpperBand_prev = df['UpperBand'].iloc[-1], df['UpperBand'].iloc[-2]
            LowerBand_curr,LowerBand_prev = df['LowerBand'].iloc[-1], df['LowerBand'].iloc[-2]

            # close order
            log_message("[BB] close buy order executed")
            if len(positions) > 0:
                for position in positions:
                    profit = float(position.profit)

                    if(profit < get_trigger_price()  and get_trigger_price() > 0):
                        trading_close(position,current_time)
                    elif position.type == mt5.ORDER_TYPE_BUY:
                        if UpperBand_curr < df['close'].iloc[-1] and UpperBand_prev > df['close'].iloc[-2]:
                            trading_close(position,current_time)
                        else:
                            lots = float(lot_var.get()) * 100
                            if profit > (get_trigger_price() + (2*lots)) and profit > (2*lots):
                                trigger_profit = get_trigger_price() + (1*lots)
                                set_trigger_price(trigger_profit)
                                log_message(f"[BOT] Trigger Profit: {trigger_profit}", "blue")
                    elif position.type == mt5.ORDER_TYPE_SELL:
                        if LowerBand_curr > df['close'].iloc[-1] and LowerBand_prev < df['close'].iloc[-2]:
                            trading_close(position,current_time)
                        else:
                            lots = float(lot_var.get()) * 100
                            if profit > (get_trigger_price() + (2*lots)) and profit > (2*lots):
                                trigger_profit = get_trigger_price() + (1*lots)
                                set_trigger_price(trigger_profit)
                                log_message(f"[BOT] Trigger Profit: {trigger_profit}", "blue")
            
                log_message("[BB] close sell order executed")
                if len(positions) > 0:
                    for position in positions:
                        #check it is sell order
                        if position.type == mt5.ORDER_TYPE_SELL:
                            trading_close(position,current_time)


            # buy and sell order
            if UpperBand_curr > df['close'].iloc[-1] and UpperBand_prev < df['close'].iloc[-2] and current_time != get_last_order_time():
                log_message("[BB] Sell order executed")
                trading_sell(current_time)
            elif LowerBand_curr < df['close'].iloc[-1] and LowerBand_prev > df['close'].iloc[-2] and current_time != get_last_order_time():
                log_message("[BB] Buy order executed")
                trading_buy(current_time)
                        # if UpperBand_curr < df['close'].iloc[-1] and UpperBand_prev > df['close'].iloc[-2] and current_time != get_last_order_time():

        elif indicator == "SUPERTREND":
            Supertrend_curr,Supertrend_prev = df['Supertrend'].iloc[-1], df['Supertrend'].iloc[-2]

            if len(positions) > 0:
                for position in positions:
                    profit = float(position.profit)
                    if(profit < get_trigger_price()  and get_trigger_price() > 0):
                        trading_close(position,current_time)
                    elif Supertrend_curr > df['close'].iloc[-1] and Supertrend_prev < df['close'].iloc[-2] and current_time != get_last_order_time():
                        trading_close(position,current_time)
                    elif Supertrend_curr < df['close'].iloc[-1] and Supertrend_prev > df['close'].iloc[-2] and current_time != get_last_order_time():
                        trading_close(position,current_time)
                    else:
                        lots = float(lot_var.get()) * 100
                        if profit > (get_trigger_price() + (3*lots)) and profit > (3*lots):
                            trigger_profit = get_trigger_price() + (1*lots)
                            set_trigger_price(trigger_profit)
                            log_message(f"[BOT] Trigger Profit: {trigger_profit}", "blue")
                    
            
            if Supertrend_curr > df['close'].iloc[-1] and Supertrend_prev < df['close'].iloc[-2] and current_time != get_last_order_time():
                trading_sell(current_time)
            elif Supertrend_curr < df['close'].iloc[-1] and Supertrend_prev > df['close'].iloc[-2] and current_time != get_last_order_time():
                trading_buy(current_time)


        time.sleep(5)



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


    # Bull Market Support Band
    df['EMA21'] = ta.ema(df['close'], length=21)
    df['SMA20'] = ta.sma(df['close'], length=20)

    df['SMA'] = ta.sma(df['close'], length=5)
    df['EMA'] = ta.ema(df['close'], length=10)
    # Calculate RSI (Relative Strength Index)

    df['MA_short'] = ta.sma(df['close'], length=7)  # Short-term MA
    df['MA_long'] = ta.sma(df['close'], length=25)
    df['RSI'] = ta.rsi(df['close'], length=14)


    # Calculate MACD (Moving Average Convergence Divergence)
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_Histogram'] = macd['MACDh_12_26_9']
    df['MACD_Signal'] = macd['MACDs_12_26_9']

    # Calculate Bollinger Bands
    bbands = ta.bbands(df['close'], length=20, std=2)
    df['BB_Middle'] = bbands['BBM_20_2.0']  # Middle Band (Simple Moving Average)
    df['UpperBand'] = bbands['BBU_20_2.0']   # Upper Band
    df['LowerBand'] = bbands['BBL_20_2.0']   # Lower Band

    supertrend_result = ta.supertrend(high=df['high'], low=df['low'], close=df['close'], length=7, multiplier=3)
    df['Supertrend'] = supertrend_result['SUPERT_7_3.0']
    df['Supertrend_Direction'] = supertrend_result['SUPERTd_7_3.0']
    
    df['Buy_Signal'] = (df['close'] > df['SMA']) & (df['RSI'] < 30)
    df['Sell_Signal'] = (df['close'] < df['EMA']) & (df['RSI'] > 70)

    donchian = ta.donchian(df['high'], df['low'], lower_length=20, upper_length=20)
    df[['DCL', 'DCU', 'DCH']] = donchian


    # Smart Money Breakout
    df['Volume_avg'] = ta.sma(df['tick_volume'], length=20) 
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    threshold = 1.5  # Volume multiplier threshold
    df['Breakout_signal'] = (df['tick_volume'] > threshold * df['Volume_avg']) & (
        df['close'] > df['high'].shift(1) + 0.5 * df['ATR']
    )

    df = identify_swing_points(df) 
    df = detect_structure(df)
    df = identify_order_blocks(df)
    df = find_fair_value_gaps(df)

    # print(df.iloc[-1])

    df = generate_alerts(df)
    return df


def generate_alerts(df):
    # Initialize the alert column with NaN
    df['alert'] = None

    # Moving Average Crossovers
    df.loc[
        (df['MA_short'] > df['MA_long']) & (df['MA_short'].shift(1) <= df['MA_long'].shift(1)),
        'alert'
    ] = 'Buy'

    df.loc[
        (df['MA_short'] < df['MA_long']) & (df['MA_short'].shift(1) >= df['MA_long'].shift(1)),
        'alert'
    ] = 'Sell'

    # RSI Conditions
    df.loc[df['RSI'] < 30, 'alert'] = 'Buy (Oversold)'
    df.loc[df['RSI'] > 70, 'alert'] = 'Sell (Overbought)'

    return df

    # poth graph into ax
def identify_swing_points(df, lookback=5):
    df['swing_high'] = df['high'] == df['high'].rolling(lookback, center=True).max()
    df['swing_low'] = df['low'] == df['low'].rolling(lookback, center=True).min()
    return df
def detect_structure(df):
    df['trend'] = np.where(df['close'] > df['close'].shift(1), 'bullish', 'bearish')
    df['change_in_trend'] = df['trend'] != df['trend'].shift(1)
    return df
def identify_order_blocks(df, atr_multiplier=2):
    df['atr'] = df['high'] - df['low']  # Simplified ATR calculation
    df['bullish_ob'] = (df['close'] > df['open']) & (df['high'] - df['low'] > df['atr'] * atr_multiplier)
    df['bearish_ob'] = (df['close'] < df['open']) & (df['high'] - df['low'] > df['atr'] * atr_multiplier)
    return df
def find_fair_value_gaps(df):
    df['fvg_bullish'] = (df['low'] > df['high'].shift(1)) & (df['close'] > df['high'].shift(2))
    df['fvg_bearish'] = (df['high'] < df['low'].shift(1)) & (df['close'] < df['low'].shift(2))
    return df
   
def poth_graph(symbol, data, indicator):


    ax.clear()

    minPrice = data['low'].min()
    maxPrice = data['high'].max()
    # data['rsi_percent'] = minPrice + (minPrice - maxPrice) * (data['RSI']) / (100)
    ax.plot(data.index, data['close'], label="Close Price", color="blue",linewidth=1)

    # ax.boxplot(data.index,data['close'], patch_artist=True, boxprops=dict(facecolor="blue"), widths=0.5)


    # buy_signals = data[data['alert'].str.contains('Buy', na=False)]
    # sell_signals = data[data['alert'].str.contains('Sell', na=False)]
    # ax.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', label='Buy Alert', alpha=1)
    # ax.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', label='Sell Alert', alpha=1)


    # fill RSI values if > 70 and < 30 fill bg color red and green
    ax.fill_between(data.index, minPrice, maxPrice, where=(data['RSI'] > 70), color='yellow', alpha=0.1, label='Overbought')
    ax.fill_between(data.index, minPrice, maxPrice, where=(data['RSI'] < 30), color='purple', alpha=0.1, label='Oversold')
    # data['rsi_percent'] = minPrice + (maxPrice - minPrice) * (data['RSI']) / (100)
    # data.loc[:, 'rsi_percent'] = minPrice + (maxPrice - minPrice) * (data['RSI']) / 100
    # ax.plot(data.index, data['rsi_percent'], label="Close Price", color="blue",linewidth=0.1)

    # ax.scatter(data.index, data['close'],where=(data['Breakout_signal']==True), s=20, c='yellow', vmin=0, vmax=100)
    # for i in range(len(data)):
    #     if data['Breakout_signal'].iloc[i] == True:
    #         ax.scatter(data.index[i], data['close'].iloc[i], s=20, c='black')
            # ax.plot(data.index, data['Breakout_signal'], label="Breakout_signal", color="purple",linewidth=0.5,linestyle='--')
    #donchain
    ax.plot(data.index, data['DCL'], label="DCL", color="purple",linewidth=0.5,linestyle='--')
    ax.plot(data.index, data['DCU'], label="DCU", color="purple",linewidth=0.5,linestyle='--')
    ax.plot(data.index, data['DCH'], label="DCH", color="purple",linewidth=0.5,linestyle='--')

    if indicator == "BULLMARKET":
        ax.plot(data.index, data['EMA21'], label='21 EMA', color='orange',linewidth=0.5)
        ax.plot(data.index, data['SMA20'], label='20 SMA', color='orange',linewidth=0.5,linestyle='--')

        ax.fill_between(data.index, data['EMA21'], data['SMA20'], where=(data['EMA21'] > data['SMA20']), color='green', alpha=0.3, label='Uptrend')
        ax.fill_between(data.index, data['EMA21'], data['SMA20'], where=(data['EMA21'] < data['SMA20']), color='red', alpha=0.3, label='Uptrend')
    elif indicator == "BOLLINGER":
        ax.plot(data.index, data['UpperBand'], label="Upper Band", color="orange",linewidth=0.5,linestyle='--')
        ax.plot(data.index, data['LowerBand'], label="Lower Band", color="orange",linewidth=0.5,linestyle='--')
        ax.fill_between(data.index, data['LowerBand'], data['UpperBand'], color='yellow', alpha=0.3, label='Bollinger Band')
    elif indicator == "SUPERTREND":
        ax.plot(data.index, data['Supertrend'], label="Supertrend", color="grey",linewidth=0.5,linestyle='--')
        ax.fill_between(data.index, data['close'], data['Supertrend'], where=(data['close'] > data['Supertrend']), color='green', alpha=0.3, label='Uptrend')
        ax.fill_between(data.index, data['close'], data['Supertrend'], where=(data['close'] < data['Supertrend']), color='red', alpha=0.3, label='Downtrend')

        for i in range(len(data)):

            if data['Supertrend'].iloc[i]  > data['close'].iloc[i] and data['Supertrend'].iloc[i-1] < data['close'].iloc[i-1]:
                ax.scatter(data.index[i], data['close'].iloc[i], s=20, c='blue')
                ax.annotate('Sell', 
                    xy=(data.index[i], data['close'].iloc[i]), 
                    xytext=(data.index[i], minPrice-10), 
                    arrowprops=dict(ec="steelblue", arrowstyle=']-', connectionstyle="angle3"), 
                    fontsize=6, color='red')
            elif data['Supertrend'].iloc[i] < data['close'].iloc[i] and data['Supertrend'].iloc[i-1] > data['close'].iloc[i-1]:
                ax.scatter(data.index[i], data['close'].iloc[i], s=20, c='blue')
                ax.annotate('Buy', 
                    xy=(data.index[i], data['close'].iloc[i]), 
                    xytext=(data.index[i], maxPrice), 
                    arrowprops=dict(ec="steelblue", arrowstyle=']-', connectionstyle="angle3"), 
                    fontsize=6, color='green')
    
    # Plot the latest close price
    ax.axhline(y=data['close'].iloc[-1], color='blue', linestyle='--',label='Lastest Price',linewidth=0.5)

    positions=mt5.positions_get(symbol=symbol)
    for position in positions:
        if position.type == mt5.ORDER_TYPE_BUY:
            # plot point of buy order
            ax.axhline(y=position.price_open, color='green', linestyle='--',label='Buy Order',linewidth=0.5)
        elif position.type == mt5.ORDER_TYPE_SELL:
            # plot point of sell order
            ax.axhline(y=position.price_open, color='red', linestyle='--',label='Sell Order',linewidth=0.5)
    
    # Highlight swing points
    # ax.scatter(data.index[data['swing_high']], data['high'][data['swing_high']], color='blue', label='Swing High', marker='^')
    # ax.scatter(data.index[data['swing_low']], data['low'][data['swing_low']], color='orange', label='Swing Low', marker='v')

    # Highlight order blocks
    ax.scatter(data.index[data['bullish_ob']], data['low'][data['bullish_ob']], color='green', marker='o', label='Bullish OB')
    ax.scatter(data.index[data['bearish_ob']], data['high'][data['bearish_ob']], color='red', marker='o', label='Bearish OB')

    # Highlight fair value gaps
    ax.scatter(data.index[data['fvg_bullish']], data['low'][data['fvg_bullish']], color='cyan', marker='s', label='Bullish FVG')
    ax.scatter(data.index[data['fvg_bearish']], data['high'][data['fvg_bearish']], color='magenta', marker='s', label='Bearish FVG')

    
    ax.set_title(f"{symbol} Indicator")
    ax.set_xlabel("Time",fontsize=4)
    ax.set_ylabel("Price",fontsize=4)
    canvas.draw()


# Run the application
root.mainloop()
