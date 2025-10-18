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
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from tkinter import font
import sys
import os


period_count = 0
period_time = 0
version = "4.3"

# Cooldown (seconds) to prevent immediate re-entry after an order action
COOLDOWN_SECONDS = 20
MINIMUM_TRIGGER_LENGTH = 5 

# Buy/Sell signals for chart markers
buy_signals = []
sell_signals = []

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

trigger_profit = 0
def set_trigger_profit(price):
    global trigger_profit
    trigger_profit = price

def get_trigger_profit():
    global trigger_profit
    return trigger_profit

def set_last_order_time(time):
    global last_order_time
    last_order_time = time

def get_last_order_time():
    global last_order_time
    return last_order_time


def is_on_cooldown():
    """Return True if last_order_time is within COOLDOWN_SECONDS from now."""
    if get_last_order_time() is None:
        return False
    try:
        return (datetime.now() - get_last_order_time()).total_seconds() < COOLDOWN_SECONDS
    except Exception:
        return False


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

# Create the main window - Full screen
root = tk.Tk()
root.title(f"MT5 Autobot V.{version}")
root.state('zoomed')  # Full screen on Windows
root.configure(bg='#f7fafc')  # Light gray-white background

# Set window icon (for title bar and taskbar)
try:
    root.iconbitmap('autobot.ico')
except Exception:
    pass  # If icon file not found, continue without it

# Set taskbar icon for Windows (requires ctypes for AppUserModelID)
try:
    if sys.platform == 'win32':
        import ctypes
        # Set AppUserModelID to show custom icon on taskbar
        myappid = 'kimookpong.mt5autobot.trading.4.2'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass  # If fails, continue without custom taskbar grouping

# Configure modern light theme with custom colors
style = ttk.Style()
style.theme_use('clam')

# Modern light color palette
PRIMARY_BG = '#f7fafc'      # Light gray-white background
SECONDARY_BG = '#ffffff'    # Pure white for panels
ACCENT_BG = '#f1f5f9'       # Light blue-gray for cards
TEXT_PRIMARY = '#1a202c'    # Dark text
TEXT_SECONDARY = '#4a5568'  # Medium gray text
ACCENT_BLUE = '#3182ce'     # Rich blue
SUCCESS_GREEN = '#38a169'   # Rich green
ERROR_RED = '#e53e3e'       # Rich red
WARNING_ORANGE = '#dd6b20'  # Rich orange

# Configure custom modern styles
style.configure('Title.TLabel', 
                font=('Segoe UI', 14, 'bold'), 
                background=PRIMARY_BG, 
                foreground=TEXT_PRIMARY)

style.configure('Header.TLabel', 
                font=('Segoe UI', 10, 'bold'), 
                background=SECONDARY_BG, 
                foreground=TEXT_PRIMARY,
                relief='flat',
                borderwidth=0)

style.configure('Info.TLabel', 
                font=('Segoe UI', 9), 
                background=SECONDARY_BG, 
                foreground=TEXT_SECONDARY)

style.configure('Status.TLabel', 
                font=('Segoe UI', 10, 'bold'), 
                background='#ffffff', 
                foreground='#1e293b',
                anchor='center')

# Compact interactive button styles
style.configure('Connect.TButton', 
                font=('Segoe UI', 8, 'bold'), 
                padding=(12, 6),
                focuscolor='none',
                borderwidth=0,
                relief='flat',
                background='#3182ce',
                foreground='white')

style.map('Connect.TButton',
          background=[('active', '#2c5aa0'),
                     ('pressed', '#2a4d8a'),
                     ('disabled', '#4a5568')],
          relief=[('active', 'flat'),
                 ('pressed', 'flat')])

style.configure('Start.TButton', 
                font=('Segoe UI', 8, 'bold'), 
                padding=(12, 6),
                focuscolor='none',
                borderwidth=0,
                relief='flat',
                background='#38a169',
                foreground='white')

style.map('Start.TButton',
          background=[('active', '#2f855a'),
                     ('pressed', '#276749'),
                     ('disabled', '#4a5568')],
          relief=[('active', 'flat'),
                 ('pressed', 'flat')])

style.configure('Stop.TButton', 
                font=('Segoe UI', 8, 'bold'), 
                padding=(12, 6),
                focuscolor='none',
                borderwidth=0,
                relief='flat',
                background='#e53e3e',
                foreground='white')

style.map('Stop.TButton',
          background=[('active', '#c53030'),
                     ('pressed', '#9c2626'),
                     ('disabled', '#4a5568')],
          relief=[('active', 'flat'),
                 ('pressed', 'flat')])

# Modern frame styles
style.configure('Modern.TFrame', 
                background=SECONDARY_BG, 
                relief='flat', 
                borderwidth=1)

style.configure('Card.TFrame',
                background=ACCENT_BG,
                relief='flat',
                borderwidth=1)

# Enhanced Entry styles
style.configure('Modern.TEntry',
                fieldbackground='#ffffff',
                foreground=TEXT_PRIMARY,
                borderwidth=1,
                relief='solid',
                insertcolor=TEXT_PRIMARY,
                lightcolor='#e2e8f0',
                darkcolor='#e2e8f0')

style.map('Modern.TEntry',
          fieldbackground=[('focus', '#f1f5f9'),
                          ('active', '#f1f5f9')],
          lightcolor=[('focus', ACCENT_BLUE),
                     ('active', ACCENT_BLUE)],
          darkcolor=[('focus', ACCENT_BLUE),
                    ('active', ACCENT_BLUE)])

# Enhanced Combobox styles  
style.configure('Modern.TCombobox',
                fieldbackground='#ffffff',
                foreground=TEXT_PRIMARY,
                borderwidth=1,
                relief='solid',
                arrowcolor=TEXT_SECONDARY,
                lightcolor='#e2e8f0',
                darkcolor='#e2e8f0')

style.map('Modern.TCombobox',
          fieldbackground=[('focus', '#f1f5f9'),
                          ('active', '#f1f5f9')],
          lightcolor=[('focus', ACCENT_BLUE),
                     ('active', ACCENT_BLUE)],
          darkcolor=[('focus', ACCENT_BLUE),
                    ('active', ACCENT_BLUE)])

# Enhanced Profit/Loss styles
style.configure('Profit.TLabel', 
                font=('Segoe UI', 10, 'bold'), 
                foreground=SUCCESS_GREEN, 
                background='#ffffff', 
                anchor='center')

style.configure('Loss.TLabel', 
                font=('Segoe UI', 10, 'bold'), 
                foreground=ERROR_RED, 
                background='#ffffff', 
                anchor='center')

# Modern LabelFrame styles with subtle borders
style.configure('Modern.TLabelframe', 
                background=SECONDARY_BG,
                borderwidth=1,
                relief='solid',
                lightcolor='#e2e8f0',
                darkcolor='#e2e8f0')

style.configure('Modern.TLabelframe.Label', 
                font=('Segoe UI', 9, 'bold'),
                background=SECONDARY_BG, 
                foreground=ACCENT_BLUE)

# Premium card style with modern aesthetics
style.configure('Card.TLabelframe',
                background='#ffffff',
                borderwidth=2,
                relief='raised',
                lightcolor='#e2e8f0',
                darkcolor='#cbd5e0')

style.configure('Card.TLabelframe.Label',
                font=('Segoe UI', 9, 'bold'),
                background='#ffffff',
                foreground='#2563eb',
                padding=(8, 4))

# Modern Checkbutton styles for indicator controls
style.configure('Modern.TCheckbutton',
                font=('Segoe UI', 8),
                background=SECONDARY_BG,
                foreground=TEXT_PRIMARY,
                focuscolor='none',
                relief='flat',
                borderwidth=0)

style.map('Modern.TCheckbutton',
          background=[('active', ACCENT_BG),
                     ('selected', ACCENT_BG)],
          foreground=[('active', ACCENT_BLUE),
                     ('selected', ACCENT_BLUE)])

account = 194634703
password = ""
server = "Exness-MT5Real17"

# Configure root grid for 3-column layout
root.columnconfigure(0, weight=0, minsize=280)  # Left panel - controls
root.columnconfigure(1, weight=1)  # Center panel - chart (expandable)
root.columnconfigure(2, weight=0, minsize=300)  # Right panel - trading log
root.rowconfigure(0, weight=1)

# Create main frames with 3-column layout
left_frame = ttk.Frame(root, style='Modern.TFrame', padding="10")
left_frame.grid(row=0, column=0, padx=(8, 4), pady=8, sticky="nsew")

center_frame = ttk.Frame(root, style='Modern.TFrame', padding="8")
center_frame.grid(row=0, column=1, padx=4, pady=8, sticky="nsew")

right_frame = ttk.Frame(root, style='Modern.TFrame', padding="10")
right_frame.grid(row=0, column=2, padx=(4, 8), pady=8, sticky="nsew")

# Connection Settings Section - Compact
connection_frame = ttk.LabelFrame(left_frame, text="🔗 Connection", style='Modern.TLabelframe', padding="10")
connection_frame.pack(fill="x", pady=(0, 10))

# Account number
ttk.Label(connection_frame, text="Account:", style='Info.TLabel').grid(row=0, column=0, sticky="w", pady=(0, 3))
account_entry = ttk.Entry(connection_frame, width=28, font=('Segoe UI', 8), style='Modern.TEntry')
account_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 6))
account_entry.insert(0, account)

# Password 
ttk.Label(connection_frame, text="Password:", style='Info.TLabel').grid(row=2, column=0, sticky="w", pady=(0, 3))
password_entry = ttk.Entry(connection_frame, show="*", width=28, font=('Segoe UI', 8), style='Modern.TEntry')
password_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 6))
password_entry.insert(0, password)

# Server
ttk.Label(connection_frame, text="Server:", style='Info.TLabel').grid(row=4, column=0, sticky="w", pady=(0, 3))
server_entry = ttk.Entry(connection_frame, width=28, font=('Segoe UI', 8), style='Modern.TEntry')
server_entry.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 8))
server_entry.insert(0, server)

# Connection buttons
button_frame = ttk.Frame(connection_frame)
button_frame.grid(row=6, column=0, columnspan=2, pady=(2, 0))

connect_button = ttk.Button(button_frame, text="🔌 Connect", style='Connect.TButton', command=lambda: connect_to_mt5())
connect_button.pack(side='left', padx=(0, 8))

disconnect_button = ttk.Button(button_frame, text="🔌 Disconnect", style='Stop.TButton', state="disabled", command=lambda: disconnect_mt5())
disconnect_button.pack(side='left')

# Configure column weights for responsive design
connection_frame.columnconfigure(0, weight=1)


# Trading Parameters Section - Compact
param_frame = ttk.LabelFrame(left_frame, text="⚙️ Parameters", style='Modern.TLabelframe', padding="10")
param_frame.pack(fill="x", pady=(0, 10))

# Symbol and Interval in compact grid
ttk.Label(param_frame, text="Symbol:", style='Info.TLabel').grid(row=0, column=0, sticky="w", pady=(0, 3))
symbol_var = tk.StringVar(value="XAUUSDm")
symbol_dropdown = ttk.Combobox(param_frame, textvariable=symbol_var, 
                              values=["XAUUSDm", "BTCUSDm"], state="disabled", 
                              width=12, font=('Segoe UI', 8), style='Modern.TCombobox')
symbol_dropdown.grid(row=1, column=0, sticky="ew", pady=(0, 6), padx=(0, 4))

ttk.Label(param_frame, text="Interval:", style='Info.TLabel').grid(row=0, column=1, sticky="w", pady=(0, 3))
interval_var = tk.StringVar(value="5m")
interval_dropdown = ttk.Combobox(param_frame, textvariable=interval_var, 
                                values=["1m", "5m", "15m", "30m", "1h", "4h", "1d"], 
                                state="disabled", width=12, font=('Segoe UI', 8), style='Modern.TCombobox')
interval_dropdown.grid(row=1, column=1, sticky="ew", pady=(0, 6), padx=(4, 0))

# Risk Management in compact grid
ttk.Label(param_frame, text="Lot Size:", style='Info.TLabel').grid(row=2, column=0, sticky="w", pady=(0, 3))
lot_var = ttk.Entry(param_frame, width=12, font=('Segoe UI', 8), style='Modern.TEntry')
lot_var.grid(row=3, column=0, sticky="ew", pady=(0, 6), padx=(0, 4))
lot_var.insert(0, "0.01")
lot_var.config(state="disabled")

ttk.Label(param_frame, text="Trigger Price:", style='Info.TLabel').grid(row=2, column=1, sticky="w", pady=(0, 3))
trigger_var = ttk.Entry(param_frame, width=12, font=('Segoe UI', 8), style='Modern.TEntry')
trigger_var.grid(row=3, column=1, sticky="ew", pady=(0, 6), padx=(4, 0))
trigger_var.insert(0, 3)
trigger_var.config(state="disabled")

# Max Orders and Indicator in compact layout
ttk.Label(param_frame, text="Max Orders:", style='Info.TLabel').grid(row=4, column=0, sticky="w", pady=(0, 3))
max_order_var = ttk.Entry(param_frame, width=12, font=('Segoe UI', 8), style='Modern.TEntry')
max_order_var.grid(row=5, column=0, sticky="ew", pady=(0, 6), padx=(0, 4))
max_order_var.insert(0, "100")
max_order_var.config(state="disabled")

ttk.Label(param_frame, text="Indicator:", style='Info.TLabel').grid(row=4, column=1, sticky="w", pady=(0, 3))
indicator_var = tk.StringVar(value="SUPERTREND")
indicator_dropdown = ttk.Combobox(param_frame, textvariable=indicator_var, 
                                 values=["BULLMARKET", "BOLLINGER", "SUPERTREND", "DONCHAIN"], 
                                 state="disabled", width=12, font=('Segoe UI', 8), style='Modern.TCombobox')
indicator_dropdown.grid(row=5, column=1, sticky="ew", pady=(0, 6), padx=(4, 0))

# Configure column weights
param_frame.columnconfigure(0, weight=1)
param_frame.columnconfigure(1, weight=1)





# Bot Control Section - Compact
bot_control_frame = ttk.LabelFrame(left_frame, text="🤖 Control", style='Modern.TLabelframe', padding="8")
bot_control_frame.pack(fill="x", pady=(0, 8))

button_bot = ttk.Frame(bot_control_frame)
button_bot.pack(fill="x")

start_bot_button = ttk.Button(button_bot, text="🚀 Start", style='Start.TButton', state="disabled", command=lambda: start_bot())
start_bot_button.pack(side='left', padx=(0, 4), fill="x", expand=True)

pause_bot_button = ttk.Button(button_bot, text="⏸️ Pause", style='Stop.TButton', state="disabled", command=lambda: pause_bot())
pause_bot_button.pack(side='right', fill="x", expand=True)

# Account Information Section - Ultra Compact
info_frame = ttk.LabelFrame(left_frame, text="💰 Info", style='Modern.TLabelframe', padding="8")
info_frame.pack(fill="x")

# Balance info super compact
usdt_balance_label = ttk.Label(info_frame, text="Balance: --", 
                              style='Info.TLabel', font=('Arial', 8, 'bold'))
usdt_balance_label.pack(anchor="w", pady=(0, 2))

# Time and Period in one line each
time_elapsed_label = ttk.Label(info_frame, text="Runtime: --", 
                              style='Info.TLabel', font=('Arial', 7))
time_elapsed_label.pack(anchor="w", pady=(0, 2))

period_count_label = ttk.Label(info_frame, text="Periods: --", 
                              style='Info.TLabel', font=('Arial', 7))
period_count_label.pack(anchor="w")

# Contact Information Section - Ultra Compact
contact_frame = ttk.LabelFrame(left_frame, text="📞 Contact", style='Modern.TLabelframe', padding="6")
contact_frame.pack(fill="x", pady=(8, 0))

# Creator info
creator_label = ttk.Label(contact_frame, text="Created by: kimookpong", 
                         style='Info.TLabel', font=('Arial', 7, 'bold'))
creator_label.pack(anchor="w", pady=(0, 1))

# Version info
version_label = ttk.Label(contact_frame, text=f"Current version: {version}", 
                         style='Info.TLabel', font=('Arial', 7))
version_label.pack(anchor="w", pady=(0, 1))

# Email info
email_label = ttk.Label(contact_frame, text="Email: kimookpong@gmail.com", 
                       style='Info.TLabel', font=('Arial', 7))
email_label.pack(anchor="w")


# Center Frame: Trading Dashboard with Chart
dashboard_title = ttk.Label(center_frame, text="📈 Trading Dashboard", 
                           font=('Segoe UI', 14, 'bold'), style='Title.TLabel')
dashboard_title.pack(pady=(0, 8))

# Enhanced Trading Status Dashboard
status_frame = ttk.Frame(center_frame, style='Modern.TFrame')
status_frame.pack(fill="x", padx=8, pady=(0, 16))

# Configure grid columns with improved spacing
for i in range(4):
    status_frame.columnconfigure(i, weight=1, minsize=160)

# Modern Period Card with enhanced styling
period_card = ttk.LabelFrame(status_frame, text="Current Period", style='Card.TLabelframe', padding="10")
period_card.grid(row=0, column=0, padx=(0, 6), pady=0, sticky="ew")

period_icon = ttk.Label(period_card, text="📅", font=('Segoe UI', 18), background='white')
period_icon.pack(pady=(0, 6))
trend_label = ttk.Label(period_card, text="--:--", style='Status.TLabel', font=('Segoe UI', 11, 'bold'))
trend_label.pack()

# Enhanced Price Card with dynamic styling
price_card = ttk.LabelFrame(status_frame, text="Market Price", style='Card.TLabelframe', padding="10")
price_card.grid(row=0, column=1, padx=6, pady=0, sticky="ew")

price_icon = ttk.Label(price_card, text="💰", font=('Segoe UI', 18), background='white')
price_icon.pack(pady=(0, 6))
current_price_label = ttk.Label(price_card, text="0.00 USD", style='Status.TLabel', font=('Segoe UI', 11, 'bold'))
current_price_label.pack()

# Professional Orders Card
pending_card = ttk.LabelFrame(status_frame, text="Active Orders", style='Card.TLabelframe', padding="10")
pending_card.grid(row=0, column=2, padx=6, pady=0, sticky="ew")

orders_icon = ttk.Label(pending_card, text="📋", font=('Segoe UI', 18), background='white')
orders_icon.pack(pady=(0, 6))
process_order_label = ttk.Label(pending_card, text="0 (0.00)", style='Status.TLabel', font=('Segoe UI', 11, 'bold'))
process_order_label.pack()

# Premium P/L Card with trend indicators
profit_card = ttk.LabelFrame(status_frame, text="Total P/L", style='Card.TLabelframe', padding="10")
profit_card.grid(row=0, column=3, padx=6, pady=0, sticky="ew")

pnl_icon = ttk.Label(profit_card, text="📈", font=('Segoe UI', 18), background='white')
pnl_icon.pack(pady=(0, 6))
trading_completed_label = ttk.Label(profit_card, text="0.00 USD", style='Status.TLabel', font=('Segoe UI', 11, 'bold'))
trading_completed_label.pack()

# Chart Section in Center Frame - Full size
chart_frame = ttk.LabelFrame(center_frame, text="Price Chart", style='Card.TLabelframe', padding="8")
chart_frame.pack(fill="both", expand=True)

# Indicator Controls Section - Above the chart
indicator_controls_frame = ttk.Frame(chart_frame, style='Modern.TFrame')
indicator_controls_frame.pack(fill="x", padx=5, pady=(0, 8))

# Create checkbox variables for each indicator
show_supertrend = tk.BooleanVar(value=True)
show_bollinger = tk.BooleanVar(value=True)  
show_ema_sma = tk.BooleanVar(value=True)
show_donchian = tk.BooleanVar(value=True)
show_rsi = tk.BooleanVar(value=False)
show_macd = tk.BooleanVar(value=False)

# Title for indicator controls
# ttk.Label(indicator_controls_frame, text="📊 Chart Indicators:", 
#          font=('Segoe UI', 9, 'bold'), style='Header.TLabel').pack(side="left", padx=(5, 15))

# Create checkboxes in a horizontal layout
checkbox_frame = ttk.Frame(indicator_controls_frame, style='Modern.TFrame')
checkbox_frame.pack(side="left", fill="x", expand=True)

# Row 1: Primary indicators
row1_frame = ttk.Frame(checkbox_frame, style='Modern.TFrame')
row1_frame.pack(fill="x", pady=(0, 3))

ttk.Checkbutton(row1_frame, text="🔄 Supertrend", variable=show_supertrend,
               style='Modern.TCheckbutton').pack(side="left", padx=(0, 15))
ttk.Checkbutton(row1_frame, text="📈 Bollinger Bands", variable=show_bollinger,
               style='Modern.TCheckbutton').pack(side="left", padx=(0, 15))
ttk.Checkbutton(row1_frame, text="📊 EMA/SMA", variable=show_ema_sma,
               style='Modern.TCheckbutton').pack(side="left", padx=(0, 15))

# Row 2: Secondary indicators  
row2_frame = ttk.Frame(checkbox_frame, style='Modern.TFrame')
row2_frame.pack(fill="x")

ttk.Checkbutton(row2_frame, text="📦 Donchian", variable=show_donchian,
               style='Modern.TCheckbutton').pack(side="left", padx=(0, 15))
ttk.Checkbutton(row2_frame, text="⚡ RSI", variable=show_rsi,
               style='Modern.TCheckbutton').pack(side="left", padx=(0, 15))
ttk.Checkbutton(row2_frame, text="📶 MACD", variable=show_macd,
               style='Modern.TCheckbutton').pack(side="left")

# Add callback to refresh chart when indicators are toggled
def refresh_chart():
    """Refresh chart when indicator checkboxes are changed"""
    try:
        symbol = symbol_var.get()
        interval = interval_var.get()
        indicator = indicator_var.get()
        
        # Only refresh if we have connection and valid data
        if symbol and interval and mt5.initialized():
            df = get_candlestick_data(symbol, interval, 1000)
            if len(df) > 0:
                poth_graph(symbol, df.tail(125), indicator)
                # Force canvas update
                canvas.draw_idle()
    except Exception as e:
        # Only log error if we're actually trading (to avoid spam during startup)
        if hasattr(mt5, 'initialized') and mt5.initialized():
            log_message(f"❌ รีเฟรชกราฟล้มเหลว", "red")

# Bind checkbox variables to refresh function
show_supertrend.trace_add('write', lambda *args: refresh_chart())
show_bollinger.trace_add('write', lambda *args: refresh_chart())
show_ema_sma.trace_add('write', lambda *args: refresh_chart())
show_donchian.trace_add('write', lambda *args: refresh_chart())
show_rsi.trace_add('write', lambda *args: refresh_chart())
show_macd.trace_add('write', lambda *args: refresh_chart())

# Configure matplotlib for full screen display - Single chart approach
fig = Figure(figsize=(12, 6), facecolor='#f7fafc', dpi=100)
fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.15)

# Create main axis
ax = fig.add_subplot()
ax.set_facecolor('#ffffff')  # Clean white background
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#e2e8f0')
ax.tick_params(axis='x', labelsize=8, colors='#4a5568', pad=2)  # Better spacing
ax.tick_params(axis='y', labelsize=8, colors='#4a5568', pad=2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#e2e8f0')
ax.spines['left'].set_color('#e2e8f0')

# Initialize subplot variables for backward compatibility
ax_price = ax
ax_rsi = None
ax_macd = None

canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Right Frame: Trading Log Section
log_frame = ttk.LabelFrame(right_frame, text="📝 Trading Log", style='Card.TLabelframe', padding="8")
log_frame.pack(fill="both", expand=True)

# Create scrollable text area
log_scroll_frame = ttk.Frame(log_frame)
log_scroll_frame.pack(fill="both", expand=True)

# Text widget with modern light theme
log_text = tk.Text(log_scroll_frame, height=25, wrap="word", 
                   font=("Consolas", 8), bg='#ffffff', fg='#1a202c',
                   selectbackground='#4299e1', selectforeground='white',
                   borderwidth=0, relief='flat', insertbackground='#1a202c')

scrollbar = ttk.Scrollbar(log_scroll_frame, orient="vertical", command=log_text.yview)
log_text.configure(yscrollcommand=scrollbar.set)

log_text.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

log_text.config(state="disabled")

# Configure modern color tags for different log levels
log_text.tag_config("green", foreground="#48bb78", font=("Consolas", 8, "bold"))
log_text.tag_config("red", foreground="#f56565", font=("Consolas", 8, "bold")) 
log_text.tag_config("blue", foreground="#4299e1", font=("Consolas", 8, "bold"))
log_text.tag_config("grey", foreground="#a0aec0", font=("Consolas", 8))
log_text.tag_config("yellow", foreground="#ed8936", font=("Consolas", 8, "bold"))

# Function to log messages
def log_message(message, color="black"):
    now = datetime.now()
    # Convert to Thai Buddhist year (add 543 years) and get last 2 digits
    thai_year = str(now.year + 543)[-2:]
    timestamp = now.strftime(f"%d/%m/{thai_year} %H:%M")
    log_text.config(state="normal")
    log_text.insert(tk.END,timestamp + " " + message + "\n",color)
    log_text.config(state="disabled")
    log_text.see(tk.END)

def account_balace():
    # Get account balance
    account_info = mt5.account_info()
    if account_info is not None:
        balance = account_info.balance
        usdt_balance_label.config(text=f"Balance: ${balance:,.2f} USD")

# Function to handle MT5 connection
def connect_to_mt5():
    account_number = account_entry.get()
    password = password_entry.get()
    server = server_entry.get()

    if not account_number or not password or not server:
        # messagebox.showwarning("Warning", "Please fill in all fields.")
        log_message("⚠️ กรุณากรอกข้อมูลให้ครบ")
        return

    log_message("🔄 กำลังเชื่อมต่อ MT5...", "blue")
    if not mt5.initialize(login=int(account_number), password=password, server=server):
        error_message = f"❌ เชื่อมต่อล้มเหลว: {mt5.last_error()}"
        # messagebox.showerror("Error", error_message)
        log_message(error_message, "red")
        return

    log_message("🔐 กำลังเข้าสู่ระบบ...", "blue")
    if not mt5.login(int(account_number), password=password, server=server):
        error_message = f"❌ เข้าระบบล้มเหลว: {mt5.last_error()}"
        # messagebox.showerror("Error", error_message)
        log_message(error_message, "red")
        mt5.shutdown()
        return

    success_message = "✅ เชื่อมต่อสำเร็จ!"
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
    log_message("🔌 กำลังตัดการเชื่อมต่อ...", "blue")
    mt5.shutdown()
    log_message("✅ ตัดการเชื่อมต่อสำเร็จ!", "green")
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
    log_message("🚀 เริ่มบอท...", "green")
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
    log_message("⏸️ หยุดบอทชั่วคราว", "yellow")
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
    if (get_last_order_time() == current_time):
        return
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
        # Use wall-clock time for cooldown guards
        set_last_order_time(current_time)
        set_trigger_profit(0)
    else:
        log_message(f"❌ คำสั่ง BUY ล้มเหลว: {result}", "red")

def trading_sell(current_time):
    if (get_last_order_time() == current_time):
        return
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
        # Use wall-clock time for cooldown guards
        set_last_order_time(current_time)
        set_trigger_profit(0)
    else:
        log_message(f"❌ คำสั่ง SELL ล้มเหลว: {result}", "red")

def trading_close(position,current_time):
        if (get_last_order_time() == current_time):
            return
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
            log_message(f"💰 ปิดออเดอร์ P/L: {position.profit:.2f} USD", "green" if position.profit >=0 else "red")
            set_stat("order", get_stat("order") + 1)
            set_stat("profit", get_stat("profit") + float(position.profit))
            # รีเซ็ต trigger_profit เมื่อปิดออเดอร์
            set_trigger_profit(0)
            # ป้องกันการเปิดออเดอร์ใหม่ในช่วงเวลาเดียวกัน
    
            max_order = max_order_var.get()
            if get_stat("order") >= int(max_order):
                log_message(f"🛑 ถึงจำนวนออเดอร์สูงสุด หยุดบอท!", "blue")
                disconnect_mt5()
                return
            
        else:
            log_message(
                f"❌ ปิดออเดอร์ล้มเหลว {ticket}: {result}",
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
        time_elapsed_label.config(text=f"Runtime: {hours:02d}h {minutes:02d}m {seconds:02d}s")

        account_balace()
        if not mt5.symbol_select(symbol, True):
            log_message(f"❌ ไม่พบสัญลักษณ์ {symbol}", "red")
            return
        df = get_candlestick_data(symbol, interval, 1000)
        # Show only half of the data (125 candles) for better visibility
        poth_graph(symbol,df.tail(125),indicator)

        current_time = df.index[-1]
        period_count,period_time = get_period()
        trend_label.config(text=current_time.strftime("%Y-%m-%d %H:%M"))

        if(current_time != period_time):
            period_count = period_count + 1
            set_period(period_count,current_time)
        balance = df['close'].iloc[-1]
        current_price_label.config(text=f"{balance} USD")
        period_count_label.config(text=f"Periods: {period_count}")
        # log_message(f"[BOT] Time: {current_time}", "blue")

        if get_stat('profit') < 0:
            trading_completed_label.configure(text=f"{get_stat('profit'):.2f} USD", style='Loss.TLabel')
        else:
            trading_completed_label.configure(text=f"{get_stat('profit'):.2f} USD", style='Profit.TLabel')

        positions=mt5.positions_get(symbol=symbol)
        process_order_label.config(text=f"0 (0.00)")

        if len(positions) > 0:
            total_profit = 0

            for position in positions:
                profit = float(position.profit)
                total_profit = total_profit + profit

                trigger_length = profit - float(trigger_var.get())
                
                # 🎯 TRAILING PROFIT SYSTEM
                # อัพเดท trigger_profit เมื่อกำไรเพิ่มขึ้นเกิน trigger_var
                if trigger_length > get_trigger_profit():
                    set_trigger_profit(trigger_length)
                    log_message(f"📊 อัพเดท Trailing: {trigger_length:.2f} USD", "blue")
                
                # 🛑 บังคับปิดเมื่อกำไรลดลงต่ำกว่า trigger_profit
                elif trigger_length < get_trigger_profit() and get_trigger_profit() > 0:
                    trading_close(position, current_time)
                    log_message(f"[TP] 💰 Trailing Profit: ปิดที่ {profit:.2f} (จาก {get_trigger_profit():.2f})", "green")
                    set_trigger_profit(0)  # รีเซ็ต trigger
                    continue
                    
            if total_profit < 0:
                process_order_label.configure(text=f"{len(positions)} ({total_profit:.2f} USD)", style='Loss.TLabel')
            else:
                process_order_label.configure(text=f"{len(positions)} ({total_profit:.2f} USD)", style='Profit.TLabel')
        else:
            # รีเซ็ต trigger_profit เมื่อไม่มี position
            if get_trigger_profit() > 0:
                set_trigger_profit(0)
        
        if indicator == "BULLMARKET":
            # ดึงข้อมูลที่จำเป็น
            close_price = df['close'].iloc[-1]
            ema_fast = df['EMA_Fast'].iloc[-1]
            ema_slow = df['EMA_Slow'].iloc[-1]
            ema_trend = df['EMA_Trend'].iloc[-1]

            # --- EXIT LOGIC ---
            # ตรวจสอบเฉพาะ Position ฝั่ง BUY
            if len(positions) > 0:
                for position in positions:
                    if position.type == mt5.ORDER_TYPE_BUY:
                        # ✅ STOP LOSS: ปิดทันทีถ้าราคาปิด "ต่ำกว่า" เส้นล่างของ Band (EMA_Slow)
                        # การใช้ราคาปิดช่วยกรอง Noise ของไส้เทียนที่ทะลุลงไปชั่วคราว
                        if df['close'].iloc[-1] < ema_slow:
                            trading_close(position, current_time)
                            log_message(f"[BM] 🛑 SL: ราคาหลุดแนวรับ | P/L: {position.profit:.2f}", "red")
            
            # --- ENTRY LOGIC ---
            # เข้าออเดอร์ BUY เมื่อไม่มี Position และเงื่อนไขทั้งหมดเป็นจริง
            elif len(positions) == 0:
                
                # --- BUY CONDITIONS ---
                # 1. อยู่ในแนวโน้มกระทิง (ราคาอยู่เหนือเส้น EMA 100)
                is_in_bull_trend = close_price > ema_trend
                
                # 2. ราคาย่อตัวเข้ามาใน "โซนซื้อ" (ระหว่าง EMA 21 และ 55)
                # เราจะรอให้แท่งเทียน "ปิด" ในโซนนี้เพื่อยืนยันการย่อตัว
                is_in_buy_zone = df['close'].iloc[-1] <= ema_fast and df['close'].iloc[-1] >= ema_slow
                
                # 3. RSI ไม่ควร Overbought เกินไป (ผ่อนปรนเป็น < 75)
                rsi_curr = df['RSI'].iloc[-1]
                is_rsi_ok = rsi_curr < 75

                if is_in_bull_trend and is_in_buy_zone and is_rsi_ok and not is_on_cooldown():
                    # ตั้ง Stop Loss ไว้ใต้เส้น EMA_Slow เล็กน้อยเพื่อเป็น Buffer
                    # สำหรับ XAU/BTC การตั้ง SL ตาม % อาจจะดีกว่า
                    # ตัวอย่าง: ตั้ง SL ต่ำกว่าเส้น EMA_Slow ไป 0.15%
                    stop_loss_price = ema_slow * 0.9985 
                    
                    trading_buy(current_time, sl=stop_loss_price)
                    log_message(f"[BM] ✅ BUY: ย่อตัวในโซนซื้อ", "green")

        elif indicator == "BOLLINGER":
            # ดึงข้อมูลที่จำเป็น
            close_curr, close_prev = df['close'].iloc[-1], df['close'].iloc[-2]
            lower_band_curr, lower_band_prev = df['BB_Lower'].iloc[-1], df['BB_Lower'].iloc[-2]
            middle_band_curr = df['BB_Middle'].iloc[-1]
            upper_band_curr, upper_band_prev = df['BB_Upper'].iloc[-1], df['BB_Upper'].iloc[-2]
            rsi_curr, rsi_prev = df['RSI'].iloc[-1], df['RSI'].iloc[-2]

            # --- EXIT LOGIC ---
            if len(positions) > 0:
                for position in positions:
                    is_buy = position.type == mt5.ORDER_TYPE_BUY
                    is_sell = position.type == mt5.ORDER_TYPE_SELL

                    # ✅ TAKE PROFIT: ปิดทำกำไรเมื่อราคาแตะเส้นกลาง (Middle Band)
                    if is_buy and close_curr >= middle_band_curr:
                        trading_close(position, current_time)
                        log_message(f"[BB] ✅ TP BUY ที่เส้นกลาง | P/L: {position.profit:.2f}", "green")
                        continue
                    elif is_sell and close_curr <= middle_band_curr:
                        trading_close(position, current_time)
                        log_message(f"[BB] ✅ TP SELL ที่เส้นกลาง | P/L: {position.profit:.2f}", "green")
                        continue

                    # ✅ STOP LOSS: (Optional but recommended) ปิดเมื่อราคากลับไปทะลุกรอบเดิมอีกครั้ง
                    if is_buy and close_curr < lower_band_curr:
                        trading_close(position, current_time)
                        log_message(f"[BB] 🛑 SL BUY: หลุดกรอบล่าง | P/L: {position.profit:.2f}", "red")
                        continue
                    elif is_sell and close_curr > upper_band_curr:
                        trading_close(position, current_time)
                        log_message(f"[BB] 🛑 SL SELL: หลุดกรอบบน | P/L: {position.profit:.2f}", "red")
                        continue
            
            # --- ENTRY LOGIC ---
            elif len(positions) == 0:
                # --- BUY CONDITIONS ---
                # 1. แท่งก่อนหน้า "ปิดนอก" กรอบล่าง
                # 2. แท่งปัจจุบัน "ปิดกลับเข้ามาใน" กรอบล่าง
                # 3. RSI ยืนยันการกลับตัว (ข้าม 30 ขึ้นมา)
                was_outside_lower = close_prev < lower_band_prev
                is_inside_lower = close_curr > lower_band_curr
                is_rsi_buy_confirm = rsi_prev < 30 and rsi_curr > 30

                if was_outside_lower and is_inside_lower and is_rsi_buy_confirm and not is_on_cooldown():
                    sl_price = df['low'].iloc[-2] # SL ที่ low ของแท่งที่ทะลุออกไป
                    trading_buy(current_time, sl=sl_price)
                    log_message(f"[BB] ✅ BUY: กลับเข้ากรอบล่าง RSI>30", "blue")

                # --- SELL CONDITIONS ---
                # 1. แท่งก่อนหน้า "ปิดนอก" กรอบบน
                # 2. แท่งปัจจุบัน "ปิดกลับเข้ามาใน" กรอบบน
                # 3. RSI ยืนยันการกลับตัว (ตัด 70 ลงมา)
                was_outside_upper = close_prev > upper_band_prev
                is_inside_upper = close_curr < upper_band_curr
                is_rsi_sell_confirm = rsi_prev > 70 and rsi_curr < 70
                
                if was_outside_upper and is_inside_upper and is_rsi_sell_confirm and not is_on_cooldown():
                    sl_price = df['high'].iloc[-2] # SL ที่ high ของแท่งที่ทะลุออกไป
                    trading_sell(current_time, sl=sl_price)
                    log_message(f"[BB] 🔻 SELL: กลับเข้ากรอบบน RSI<70", "red")

        elif indicator == "SUPERTREND":
            # Enhanced Supertrend Strategy - Optimized for Risk Management & Maximum Profit
            # Using Supertrend with RSI confirmation and dynamic trailing stop
            
            close_price = df['close'].iloc[-1]
            supertrend_val = df['Supertrend'].iloc[-1]
            supertrend_dir = df['Supertrend_Direction'].iloc[-1]
            supertrend_dir_prev = df['Supertrend_Direction'].iloc[-2]
            rsi_curr = df['RSI'].iloc[-1]
            
            # Close existing positions with enhanced profit protection
            if len(positions) > 0:
                for position in positions:
                    is_buy = position.type == mt5.ORDER_TYPE_BUY
                    is_sell = position.type == mt5.ORDER_TYPE_SELL

                    # ปิด Buy ถ้า Supertrend พลิกเป็นลง
                    if is_buy and supertrend_dir == -1:
                        trading_close(position, current_time)
                   
                        continue # ไปยัง position ถัดไป

                    # ปิด Sell ถ้า Supertrend พลิกเป็นขึ้น
                    elif is_sell and supertrend_dir == 1:
                        trading_close(position, current_time)
                  
                        continue # ไปยัง position ถัดไป
                    
                    # ✅ EXIT 2: Trailing Stop Loss โดยใช้เส้น Supertrend (หัวใจของกลยุทธ์)
                    # เราจะใช้เส้น Supertrend ของ "แท่งก่อนหน้า" เป็น SL เพื่อให้ราคามีพื้นที่หายใจ
                    trailing_stop_price = df['Supertrend'].iloc[-2]

                    if is_buy and close_price < trailing_stop_price:
                        trading_close(position, current_time)
                        log_message(f"[ST] 🛑 SL BUY: ราคาต่ำกว่า ST | P/L: {position.profit:.2f}", "red")
                        continue

                    elif is_sell and close_price > trailing_stop_price:
                        trading_close(position, current_time)
                        log_message(f"[ST] 🛑 SL SELL: ราคาสูงกว่า ST | P/L: {position.profit:.2f}", "red")
                        continue

            # เข้าออเดอร์เมื่อไม่มี Position ค้างอยู่เท่านั้น
            elif len(positions) == 0:
                
                # --- BUY CONDITIONS ---
                # 1. Supertrend เพิ่งพลิกเป็นขาขึ้น
                # 2. RSI > 50 เพื่อยืนยัน Momentum ฝั่งขึ้น
                is_bullish_flip = supertrend_dir == 1 and supertrend_dir_prev == -1
                
                if is_bullish_flip and rsi_curr > 50 and not is_on_cooldown():
                    # ไม่จำเป็นต้องมี SL ในคำสั่ง เพราะ logic ด้านบนจะจัดการให้
                    trading_buy(current_time)
                    log_message(f"[ST] ✅ BUY: ST พลิกขึ้น RSI {rsi_curr:.1f}", "green")
                    # บันทึกจุด Buy สำหรับแสดงบนกราฟ (ใช้ index จาก dataframe)
                    global buy_signals
                    buy_signals.append({'time': df.index[-1], 'price': close_price})
                    # อาจจะตั้ง SL เริ่มต้นที่เส้น Supertrend ปัจจุบันเพื่อความปลอดภัย
                    # mt5.modify_position(ticket, sl=supertrend_val)

                # --- SELL CONDITIONS ---
                # 1. Supertrend เพิ่งพลิกเป็นขาลง
                # 2. RSI < 50 เพื่อยืนยัน Momentum ฝั่งลง
                is_bearish_flip = supertrend_dir == -1 and supertrend_dir_prev == 1
                
                if is_bearish_flip and rsi_curr < 50 and not is_on_cooldown():
                    trading_sell(current_time)
                    log_message(f"[ST] 🔻 SELL: ST พลิกลง RSI {rsi_curr:.1f}", "red")
                    # บันทึกจุด Sell สำหรับแสดงบนกราฟ (ใช้ index จาก dataframe)
                    global sell_signals
                    sell_signals.append({'time': df.index[-1], 'price': close_price})
                    # mt5.modify_position(ticket, sl=supertrend_val)                    
                    
        elif indicator == "DONCHAIN":
            # Donchian Channels Strategy (DCL=Lower, DCU=Upper, DCH=Highest)
            close_curr = df['close'].iloc[-1]
            close_prev = df['close'].iloc[-2]
            dcl_curr = df['DC_Lower'].iloc[-1]
            dcu_curr = df['DC_Upper'].iloc[-1]
            dcm_curr = df['DC_Middle'].iloc[-1] # เส้นกลาง
            rsi_curr = df['RSI'].iloc[-1]

            # --- EXIT LOGIC ---
            # ตรวจสอบตำแหน่งที่เปิดอยู่เพื่อปิด
            if len(positions) > 0:
                for position in positions:
                    is_buy = position.type == mt5.ORDER_TYPE_BUY
                    is_sell = position.type == mt5.ORDER_TYPE_SELL
                    
                    # ✅ EXIT 1: Stop and Reverse (SAR) - ปิดเมื่อราคาทะลุช่องตรงข้าม (ทำหน้าที่เป็น SL)
                    if is_buy and close_curr < dcl_curr:
                        trading_close(position, current_time)
                        log_message(f"[DC] 🔄 ปิด BUY: หลุดช่องล่าง | P/L: {position.profit:.2f}", "yellow")
                        continue

                    elif is_sell and close_curr > dcu_curr:
                        trading_close(position, current_time)
                        log_message(f"[DC] 🔄 ปิด SELL: หลุดช่องบน | P/L: {position.profit:.2f}", "yellow")
                        continue

                    # ✅ EXIT 2 (Optional): Take Profit / Trailing Stop ที่เส้นกลาง
                    # หากมีกำไรและราคาย่อกลับมาที่เส้นกลาง ให้พิจารณาปิดทำกำไร
                    if position.profit > 0:
                        if is_buy and close_curr < dcm_curr:
                            trading_close(position, current_time)
                            log_message(f"[DC] ✅ TP BUY: เส้นกลาง | P/L: {position.profit:.2f}", "blue")
                            continue
                        
                        elif is_sell and close_curr > dcm_curr:
                            trading_close(position, current_time)
                            log_message(f"[DC] ✅ TP SELL: เส้นกลาง | P/L: {position.profit:.2f}", "blue")
                            continue

            # --- ENTRY LOGIC ---
            # เข้าออเดอร์เมื่อไม่มี Position ค้างอยู่
            elif len(positions) == 0:
                
                # --- BUY CONDITIONS ---
                # 1. ราคาเพิ่งทะลุช่องบน (Breakout)
                # 2. RSI > 60 เพื่อยืนยัน Momentum ที่แข็งแกร่ง
                is_buy_breakout = close_curr > dcu_curr and close_prev <= dcu_curr
                
                if is_buy_breakout and rsi_curr > 60 and not is_on_cooldown():
                    trading_buy(current_time)
                    log_message(f"[DC] ✅ BUY: Breakout ช่องบน RSI {rsi_curr:.1f}", "green")

                # --- SELL CONDITIONS ---
                # 1. ราคาเพิ่งทะลุช่องล่าง (Breakdown)
                # 2. RSI < 40 เพื่อยืนยัน Momentum ที่แข็งแกร่ง
                is_sell_breakout = close_curr < dcl_curr and close_prev >= dcl_curr
                
                if is_sell_breakout and rsi_curr < 40 and not is_on_cooldown():
                    trading_sell(current_time)
                    log_message(f"[DC] 🔻 SELL: Breakdown ช่องล่าง RSI {rsi_curr:.1f}", "red")
         
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
        log_message(f"❌ ไม่สามารถดึงข้อมูล {symbol}", "red")
        return []
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')
    df.set_index('time', inplace=True)


    # Bull Market Support Band
    df['EMA_Fast'] = ta.ema(df['close'], length=21)     # เส้นบนของ Band
    df['EMA_Slow'] = ta.ema(df['close'], length=55)     # เส้นล่างของ Band
    df['EMA_Trend'] = ta.ema(df['close'], length=100)   # เส้นกรองแนวโน้มกระทิง (เร็วขึ้น)


    df['SMA'] = ta.sma(df['close'], length=5)
    df['EMA'] = ta.ema(df['close'], length=10)
    # Calculate RSI (Relative Strength Index)
    df['RSI'] = ta.rsi(df['close'], length=14)
    
    # Calculate MACD (Moving Average Convergence Divergence)
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_Histogram'] = macd['MACDh_12_26_9']
    df['MACD_Signal'] = macd['MACDs_12_26_9']
    
    # Handle NaN values - use pandas method parameter correctly
    df['RSI'] = df['RSI'].ffill().fillna(50)  # Fill with 50 if still NaN
    df['MACD'] = df['MACD'].ffill().fillna(0)
    df['MACD_Histogram'] = df['MACD_Histogram'].ffill().fillna(0)
    df['MACD_Signal'] = df['MACD_Signal'].ffill().fillna(0)

    # Calculate Bollinger Bands
    bbands = ta.bbands(df['close'], length=20, std=2.0)
    df['BB_Lower'] = bbands['BBL_20_2.0_2.0']
    df['BB_Middle'] = bbands['BBM_20_2.0_2.0']
    df['BB_Upper'] = bbands['BBU_20_2.0_2.0']

    # Calculate Supertrend - Optimized for 5m timeframe
    # Using length=12 and multiplier=3 for better sensitivity on 5min charts
    supertrend_result = ta.supertrend(high=df['high'], low=df['low'], close=df['close'], 
                                     length=12, multiplier=3.0)
    df['Supertrend'] = supertrend_result['SUPERT_12_3.0']
    df['Supertrend_Direction'] = supertrend_result['SUPERTd_12_3.0']
    
    df['Buy_Signal'] = (df['close'] > df['SMA']) & (df['RSI'] < 30)
    df['Sell_Signal'] = (df['close'] < df['EMA']) & (df['RSI'] > 70)

    donchian = ta.donchian(df['high'], df['low'], lower_length=25, upper_length=25)
    df[['DCL', 'DCU', 'DCH']] = donchian
    return df
    # poth graph into ax
    
   
def poth_graph(symbol, data, indicator):
    global ax, ax_price, ax_rsi, ax_macd
    
    # Clear figure and create dynamic subplots based on selected indicators
    fig.clear()
    
    # Determine how many subplots we need
    show_rsi_subplot = show_rsi.get()
    show_macd_subplot = show_macd.get()
    
    subplot_count = 1  # Price chart is always shown
    if show_rsi_subplot:
        subplot_count += 1
    if show_macd_subplot:
        subplot_count += 1
    
    # Create subplots with proper height ratios using GridSpec
    fig.subplots_adjust(left=0.05, right=0.96, top=0.95, bottom=0.12)
    
    if show_rsi_subplot and show_macd_subplot:
        # 3 subplots: Price (60%), RSI (20%), MACD (20%)
        gs = fig.add_gridspec(3, 1, height_ratios=[3, 1, 1], hspace=0.4)
        ax_price = fig.add_subplot(gs[0])
        ax_rsi = fig.add_subplot(gs[1])
        ax_macd = fig.add_subplot(gs[2])
    elif show_rsi_subplot:
        # 2 subplots: Price (70%), RSI (30%)
        gs = fig.add_gridspec(2, 1, height_ratios=[7, 3], hspace=0.35)
        ax_price = fig.add_subplot(gs[0])
        ax_rsi = fig.add_subplot(gs[1])
        ax_macd = None
    elif show_macd_subplot:
        # 2 subplots: Price (70%), MACD (30%)
        gs = fig.add_gridspec(2, 1, height_ratios=[7, 3], hspace=0.35)
        ax_price = fig.add_subplot(gs[0])
        ax_rsi = None
        ax_macd = fig.add_subplot(gs[1])
    else:
        # Only price chart
        ax_price = fig.add_subplot(1, 1, 1)
        ax_rsi = None
        ax_macd = None
    
    # For backward compatibility
    ax = ax_price
    
    # Style price chart
    ax_price.set_facecolor('#ffffff')
    ax_price.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#e2e8f0')
    ax_price.tick_params(axis='x', labelsize=8, colors='#4a5568', labelbottom=(not show_rsi_subplot and not show_macd_subplot))
    ax_price.tick_params(axis='y', labelsize=8, colors='#4a5568', pad=2)
    ax_price.spines['top'].set_visible(False)
    ax_price.spines['right'].set_visible(False)
    ax_price.spines['bottom'].set_color('#e2e8f0')
    ax_price.spines['left'].set_color('#e2e8f0')
    ax_price.set_ylabel('Price Chart', fontsize=10, color='#4a5568', weight='bold')
    
    # Create custom light theme style with larger fonts and better visibility
    mpf_style = mpf.make_mpf_style(
        base_mpf_style='yahoo',
        facecolor='#ffffff',
        figcolor='#f7fafc', 
        gridcolor='#e2e8f0',
        gridstyle='-',
        rc={'font.size': 9, 'axes.edgecolor': '#e2e8f0', 'axes.linewidth': 1.2}
    )
   
    # Initialize ap list for price chart addplots based on checkbox selections
    ap = []
    
    # Add Donchian Channels if enabled
    if show_donchian.get():
        ap.extend([
            mpf.make_addplot(data['DCL'], ax=ax_price, color='grey', linestyle='--', width=0.5, alpha=0.7),
            mpf.make_addplot(data['DCU'], ax=ax_price, color='grey', linestyle='--', width=0.5, alpha=0.7),
            mpf.make_addplot(data['DCH'], ax=ax_price, color='grey', linestyle='--', width=0.5, alpha=0.7),
        ])
    
    # Add EMA/SMA indicators if enabled
    if show_ema_sma.get():
        ap.extend([
            mpf.make_addplot(data['EMA'], ax=ax_price, color='#9333ea', linestyle='-', width=0.8, alpha=0.8),
            mpf.make_addplot(data['SMA'], ax=ax_price, color='#f59e0b', linestyle='-', width=0.8, alpha=0.8),
        ])
 
    # Add strategy-specific indicators based on selected trading strategy
    if indicator == "BULLMARKET":
        # Bull Market Support Band indicators
        if show_ema_sma.get():
            ap.extend([
                mpf.make_addplot(data['EMA_Slow'], ax=ax_price, color='#f97316', linestyle='-', width=1, alpha=0.8),
                mpf.make_addplot(data['EMA_Fast'], ax=ax_price, color='#ea580c', linestyle='-', width=1, alpha=0.8),
                mpf.make_addplot(data['EMA_Trend'], ax=ax_price, color='#fb923c', linestyle='--', width=0.8, alpha=0.6),
            ])
            
    elif indicator == "BOLLINGER":
        # Bollinger Bands indicators
        if show_bollinger.get():
            ap.extend([
                mpf.make_addplot(data['BB_Upper'], ax=ax_price, color='#f97316', linestyle='-', width=1, alpha=0.8),
                mpf.make_addplot(data['BB_Lower'], ax=ax_price, color='#f97316', linestyle='-', width=1, alpha=0.8),
                mpf.make_addplot(data['BB_Middle'], ax=ax_price, color='#fb923c', linestyle='--', width=0.8, alpha=0.6),
            ])
            
    elif indicator == "SUPERTREND":
        # Supertrend indicators
        if show_supertrend.get():
            # Create colored Supertrend based on direction
            supertrend_bullish = data['Supertrend'].where(data['Supertrend_Direction'] == 1)
            supertrend_bearish = data['Supertrend'].where(data['Supertrend_Direction'] == -1)
            
            ap.extend([
                # Bullish Supertrend (Green) - Thicker and more visible
                mpf.make_addplot(supertrend_bullish, ax=ax_price, color='#00cc00', width=1.5, alpha=0.9),
                # Bearish Supertrend (Red) - Thicker and more visible  
                mpf.make_addplot(supertrend_bearish, ax=ax_price, color='#cc0000', width=1.5, alpha=0.9),
            ])
            
            # Add Buy/Sell signal markers
            global buy_signals, sell_signals
            
            # Create arrays for buy/sell signals - show last 50 signals
            if len(buy_signals) > 0:
                buy_times = [s['time'] for s in buy_signals[-50:]]
                buy_prices = [s['price'] for s in buy_signals[-50:]]
                # Create series with NaN for non-signal points
                buy_marker = pd.Series(index=data.index, dtype=float)
                for time, price in zip(buy_times, buy_prices):
                    # Find closest matching index
                    if time in data.index:
                        buy_marker.loc[time] = price
                    else:
                        # Try to find nearest time
                        try:
                            nearest_idx = data.index.get_indexer([time], method='nearest')[0]
                            if nearest_idx >= 0:
                                buy_marker.iloc[nearest_idx] = price
                        except:
                            pass
                
                if buy_marker.notna().any():
                    ap.append(mpf.make_addplot(buy_marker, ax=ax_price, type='scatter', 
                                               marker='^', markersize=200, color='lime', edgecolors='darkgreen', linewidths=2))
            
            if len(sell_signals) > 0:
                sell_times = [s['time'] for s in sell_signals[-50:]]
                sell_prices = [s['price'] for s in sell_signals[-50:]]
                sell_marker = pd.Series(index=data.index, dtype=float)
                for time, price in zip(sell_times, sell_prices):
                    if time in data.index:
                        sell_marker.loc[time] = price
                    else:
                        try:
                            nearest_idx = data.index.get_indexer([time], method='nearest')[0]
                            if nearest_idx >= 0:
                                sell_marker.iloc[nearest_idx] = price
                        except:
                            pass
                
                if sell_marker.notna().any():
                    ap.append(mpf.make_addplot(sell_marker, ax=ax_price, type='scatter', 
                                               marker='v', markersize=200, color='red', edgecolors='darkred', linewidths=2))
            
    elif indicator == "DONCHAIN":
        # Enhanced Donchian Channels visualization - More prominent when selected
        if show_donchian.get():
            ap.extend([
                # Lower Channel (Support) - Blue
                mpf.make_addplot(data['DCL'], ax=ax_price, color='#3182ce', linestyle='-', width=1.5, alpha=0.9),
                # Upper Channel (Resistance) - Orange  
                mpf.make_addplot(data['DCU'], ax=ax_price, color='#dd6b20', linestyle='-', width=1.5, alpha=0.9),
                # Highest Channel (Extreme) - Purple
                mpf.make_addplot(data['DCH'], ax=ax_price, color='#805ad5', linestyle='-', width=1.5, alpha=0.9),
            ])
    
    # If no indicators are selected, show a clean chart
    if not ap:
        ap = None
    
    # Enhanced plot with better candle visibility on main price chart
    mpf.plot(
        data,
        ax=ax_price,
        addplot=ap if ap else None,
        type='candle',
        style=mpf_style,
        xrotation=0,  # Don't rotate x-axis labels on main chart
        datetime_format='%H:%M',
        # Larger candle bodies for better visibility
        volume=False,
        show_nontrading=False
    )
    
    # Draw RSI subplot if enabled and exists
    if show_rsi_subplot and ax_rsi is not None:
        try:
            ax_rsi.clear()  # Clear previous data
            ax_rsi.set_facecolor('#ffffff')
            ax_rsi.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#e2e8f0')
            ax_rsi.spines['top'].set_visible(False)
            ax_rsi.spines['right'].set_visible(False)
            ax_rsi.spines['bottom'].set_color('#e2e8f0')
            ax_rsi.spines['left'].set_color('#e2e8f0')
            
            
            # Ensure we have valid RSI data
            if data['RSI'].notna().any():
                # Plot RSI line with better styling
                valid_rsi = data['RSI'].dropna()
                ax_rsi.plot(valid_rsi.index, valid_rsi.values, color='#8b5cf6', linewidth=1, alpha=0.9, label='RSI')
                
                # Fill overbought zone (RSI > 70) - only where data exists
                ax_rsi.fill_between(data.index, 70, 100, color='#fee2e2', alpha=0.3, label='Overbought')
                
                # Fill oversold zone (RSI < 30) - only where data exists  
                ax_rsi.fill_between(data.index, 0, 30, color='#dcfce7', alpha=0.3, label='Oversold')
                
                # Conditional fills only where RSI has values
                valid_mask = data['RSI'].notna()
                if valid_mask.any():
                    ax_rsi.fill_between(data.index[valid_mask], data['RSI'][valid_mask], 70, 
                                       where=(data['RSI'][valid_mask] > 70), color='#ef4444', alpha=0.4, interpolate=True)
                    ax_rsi.fill_between(data.index[valid_mask], data['RSI'][valid_mask], 30, 
                                       where=(data['RSI'][valid_mask] < 30), color='#22c55e', alpha=0.4, interpolate=True)
            else:
                # Plot a default line if no RSI data
                ax_rsi.plot(data.index, [50] * len(data), color='#8b5cf6', linewidth=0.8, alpha=0.5, linestyle='--', label='RSI (No Data)')
                print("Warning: No valid RSI data found")
            
            # Reference lines
            ax_rsi.axhline(y=70, color='#ef4444', linestyle='--', alpha=0.8, linewidth=1.2)
            ax_rsi.axhline(y=30, color='#22c55e', linestyle='--', alpha=0.8, linewidth=1.2)
            ax_rsi.axhline(y=50, color='#6b7280', linestyle='-', alpha=0.6, linewidth=1)
            
            ax_rsi.set_ylabel('RSI', fontsize=10, color='#4a5568', weight='bold')
            ax_rsi.set_ylim(0, 100)
            ax_rsi.set_yticks([0, 30, 50, 70, 100])
            # Hide x-axis labels if MACD is also shown (MACD will show them)
            if show_macd_subplot:
                ax_rsi.tick_params(axis='x', labelsize=8, colors='#4a5568', labelbottom=False)
            else:
                ax_rsi.tick_params(axis='x', labelsize=8, colors='#4a5568', labelbottom=True)
                ax_rsi.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            
            ax_rsi.tick_params(axis='y', labelsize=8, colors='#4a5568')
            
            # Add RSI value text with NaN checking
            if not data['RSI'].isna().iloc[-1]:
                current_rsi = data['RSI'].iloc[-1]
                rsi_color = '#ef4444' if current_rsi > 70 else '#22c55e' if current_rsi < 30 else '#8b5cf6'
                ax_rsi.text(0.02, 0.92, f'RSI: {current_rsi:.1f}', transform=ax_rsi.transAxes, 
                           fontsize=9, weight='bold', color=rsi_color, 
                           bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9, edgecolor=rsi_color))
            else:
                ax_rsi.text(0.02, 0.92, 'RSI: No Data', transform=ax_rsi.transAxes, 
                           fontsize=9, weight='bold', color='#6b7280', 
                           bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9, edgecolor='#6b7280'))
            
            # Add level labels
            ax_rsi.text(0.98, 0.85, '70', transform=ax_rsi.transAxes, fontsize=7, 
                       color='#ef4444', weight='bold', ha='right')
            ax_rsi.text(0.98, 0.15, '30', transform=ax_rsi.transAxes, fontsize=7, 
                       color='#22c55e', weight='bold', ha='right')
        except Exception as e:
            print(f"RSI plotting error: {e}")
    
    # Draw MACD subplot if enabled and exists
    if show_macd_subplot and ax_macd is not None:
        try:
            ax_macd.clear()  # Clear previous data
            ax_macd.set_facecolor('#ffffff')
            ax_macd.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#e2e8f0')
            ax_macd.spines['top'].set_visible(False)
            ax_macd.spines['right'].set_visible(False)
            ax_macd.spines['bottom'].set_color('#e2e8f0')
            ax_macd.spines['left'].set_color('#e2e8f0')
            
            # Ensure we have valid MACD data
            if data['MACD'].notna().any() and data['MACD_Signal'].notna().any():
                # Plot MACD lines with better visibility - only valid data
                valid_macd = data['MACD'].dropna()
                valid_signal = data['MACD_Signal'].dropna()
                
                if not valid_macd.empty:
                    ax_macd.plot(valid_macd.index, valid_macd.values, color='#0ea5e9', linewidth=1, alpha=0.9, label='MACD')
                if not valid_signal.empty:
                    ax_macd.plot(valid_signal.index, valid_signal.values, color='#f97316', linewidth=1, alpha=0.9, label='Signal')

                # MACD Histogram with NaN checking
                if data['MACD_Histogram'].notna().any():
                    valid_hist = data['MACD_Histogram'].dropna()
                    positive_mask = valid_hist >= 0
                    negative_mask = valid_hist < 0
                    
                    # Calculate bar width based on time interval
                    if len(data.index) > 1:
                        time_delta = data.index[1] - data.index[0]
                        bar_width = time_delta.total_seconds() / (24 * 3600) * 0.8  # 80% of time interval
                    else:
                        bar_width = 0.6
                    
                    if positive_mask.any():
                        ax_macd.bar(valid_hist.index[positive_mask], valid_hist.values[positive_mask], 
                                   color='#22c55e', alpha=0.6, width=bar_width, label='Positive Hist')
                    if negative_mask.any():
                        ax_macd.bar(valid_hist.index[negative_mask], valid_hist.values[negative_mask], 
                                   color='#ef4444', alpha=0.6, width=bar_width, label='Negative Hist')
            else:
                # Plot default lines if no MACD data
                ax_macd.plot(data.index, [0] * len(data), color='#0ea5e9', linewidth=1, alpha=0.5, linestyle='--', label='MACD (No Data)')
                ax_macd.plot(data.index, [0] * len(data), color='#f97316', linewidth=1, alpha=0.5, linestyle='--', label='Signal (No Data)')
                print("Warning: No valid MACD data found")
            
            # Zero line
            ax_macd.axhline(y=0, color='#6b7280', linestyle='-', alpha=0.8, linewidth=1.2)
            
            ax_macd.set_ylabel('MACD', fontsize=10, color='#4a5568', weight='bold')
            ax_macd.tick_params(axis='x', labelsize=8, colors='#4a5568', rotation=0)
            ax_macd.tick_params(axis='y', labelsize=8, colors='#4a5568')
            
            # Format x-axis labels
            ax_macd.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            
            # Add MACD and Signal value text with NaN checking
            if (not data['MACD'].isna().iloc[-1] and 
                not data['MACD_Signal'].isna().iloc[-1] and 
                not data['MACD_Histogram'].isna().iloc[-1]):
                
                current_macd = data['MACD'].iloc[-1]
                current_signal = data['MACD_Signal'].iloc[-1]
                current_hist = data['MACD_Histogram'].iloc[-1]
                
                # Determine trend color
                macd_color = '#22c55e' if current_macd > current_signal else '#ef4444'
                
                # Value display with multiple lines
                value_text = f'MACD: {current_macd:.3f}\nSignal: {current_signal:.3f}\nHist: {current_hist:.3f}'
                ax_macd.text(0.02, 0.92, value_text, transform=ax_macd.transAxes, 
                            fontsize=8, weight='bold', color=macd_color,
                            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9, edgecolor=macd_color),
                            verticalalignment='top')
            else:
                # Show "No Data" message
                ax_macd.text(0.02, 0.92, 'MACD: No Data\nSignal: No Data\nHist: No Data', 
                            transform=ax_macd.transAxes, 
                            fontsize=8, weight='bold', color='#6b7280',
                            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9, edgecolor='#6b7280'),
                            verticalalignment='top')
            
            # Add legend for better understanding
            ax_macd.legend(loc='upper right', fontsize=7, framealpha=0.9)
        except Exception as e:
            print(f"MACD plotting error: {e}")
    


        
    # Current price line - More prominent
    ax_price.axhline(y=data['close'].iloc[-1], color='#2563eb', linestyle='-', 
               label='Latest Price', linewidth=1, alpha=0.8)
    
    # Position lines - More visible
    positions=mt5.positions_get(symbol=symbol)
    for position in positions:
        if position.type == mt5.ORDER_TYPE_BUY:
            ax_price.axhline(y=position.price_open, color='#00cc00', linestyle='-', 
                      label='Buy Order', linewidth=1, alpha=0.8)
        elif position.type == mt5.ORDER_TYPE_SELL:
            ax_price.axhline(y=position.price_open, color='#cc0000', linestyle='-', 
                      label='Sell Order', linewidth=1, alpha=0.8)
    
    # Add indicator status text in top-right corner of price chart
    active_indicators = []
    if show_supertrend.get():
        active_indicators.append("ST")
    if show_bollinger.get():
        active_indicators.append("BB")
    if show_ema_sma.get():
        active_indicators.append("EMA/SMA")
    if show_donchian.get():
        active_indicators.append("DC")
    if show_rsi.get():
        active_indicators.append("RSI")
    if show_macd.get():
        active_indicators.append("MACD")
    
    if active_indicators:
        indicator_text = "[CHART] " + " | ".join(active_indicators)
        ax_price.text(0.99, 0.97, indicator_text, transform=ax_price.transAxes, 
               fontsize=8, weight='bold', color='#4a5568',
               ha='right', va='top', 
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='#e2e8f0'))
    
    # Refresh canvas
    canvas.draw()
    canvas.flush_events()



# Configure final window settings
root.protocol("WM_DELETE_WINDOW", lambda: (mt5.shutdown() if 'mt5' in globals() else None, root.destroy()))

# Set minimum window size and make resizable for 3-column layout
root.minsize(1200, 700)
root.resizable(True, True)

# Configure proper resizing behavior for 3-column layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=0)  # Left panel fixed
root.grid_columnconfigure(1, weight=1)  # Center panel expandable
root.grid_columnconfigure(2, weight=0)  # Right panel fixed

# Window is already set to full screen with root.state('zoomed')
# No need for manual geometry configuration since we're using full screen

# Add welcome log message
log_message(f"🎯 ยินดีต้อนรับสู่ MT5 Autobot V.{version}!", "blue")
log_message("⚡ พร้อมเทรดอัตโนมัติ", "green")

# Run the application
root.mainloop()
