# 🤖 MT5 Autobot v4.3 (ภาษาไทย)# 🤖 MT5 Autobot v4.3# MT5 Autobot v4.2 🤖💰# MT5 Trading Bot v4.1

บอทเทรดอัตโนมัติสำหรับ MetaTrader 5 (MT5) พร้อม UI ทันสมัย กลยุทธ์ให้เลือกหลายแบบ และระบบจัดการความเสี่ยงครบถ้วน**MT5 Automated Trading Bot with Advanced Technical Indicators\*\***Automated Trading Bot for MetaTrader 5\*\* with Advanced Technical Analysis and Risk Management🤖 Advanced MetaTrader 5 Automated Trading Bot with Supertrend Strategy and Real-time GUI Dashboard

![Python](https://img.shields.io/badge/python-3.8%2B-blue)A professional automated trading system for MetaTrader 5 (MT5) with multiple technical indicators, risk management features, and real-time monitoring dashboard.Created by: **kimookpong** ![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)

![MetaTrader5](https://img.shields.io/badge/MetaTrader-5-green)

![License](https://img.shields.io/badge/license-MIT-orange)![Python](https://img.shields.io/badge/python-3.8+-blue.svg)Email: kimookpong@gmail.com ![License](https://img.shields.io/badge/license-MIT-green.svg)

---![MT5](https://img.shields.io/badge/MetaTrader-5-green.svg)

## สารบัญ![License](https://img.shields.io/badge/license-MIT-orange.svg)Version: **4.2**![MetaTrader5](https://img.shields.io/badge/platform-MT5-orange.svg)

- คุณสมบัติเด่น

- ความต้องการของระบบ---![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)## 📋 Overview

- วิธีติดตั้ง

- การตั้งค่า## 📋 Table of Contents![License](https://img.shields.io/badge/license-MIT-green.svg)

- วิธีใช้งาน

- กลยุทธ์การเทรด- [Features](#-features)![MetaTrader5](https://img.shields.io/badge/platform-MT5-orange.svg)This project is a sophisticated automated trading bot designed for MetaTrader 5 platform. It features a modern GUI interface with real-time chart visualization, technical indicator analysis, and automated trading execution based on Supertrend strategy.

- อินดิเคเตอร์

- การจัดการความเสี่ยง- [Screenshots](#-screenshots)

- การสร้างไฟล์ .exe

- การแก้ไขปัญหา- [Installation](#-installation)---### 🎯 Key Features

- ใบอนุญาตและข้อจำกัดความรับผิดชอบ

- [Configuration](#-configuration)

---

# 🤖 MT5 Autobot v4.3

## คุณสมบัติเด่น

- กลยุทธ์ให้เลือก: BULLMARKET, BOLLINGER, SUPERTREND, DONCHAINA professional automated trading bot for MetaTrader 5 with a modern UI, multiple strategies, and strong risk management.

- กราฟแบบเรียลไทม์ เปิด/ปิดอินดิเคเตอร์ได้ทันที (SuperTrend, Bollinger, EMA/SMA, Donchian, RSI, MACD)

- UI สมัยใหม่ด้วย Tkinter แบ่งเป็น 3 ส่วน: ตั้งค่า • กราฟ • Log![Python](https://img.shields.io/badge/python-3.8%2B-blue)

- แสดง P/L และจำนวนออเดอร์แบบเรียลไทม์![MetaTrader5](https://img.shields.io/badge/MetaTrader-5-green)

- Log ภาษาไทย พร้อมวัน-เวลาแบบพุทธศักราช![License](https://img.shields.io/badge/license-MIT-orange)

- ระบบป้องกันความเสี่ยง: Cooldown + Trailing Profit

- ไอคอนโปรแกรมและ Taskbar บน Windows (autobot.ico)---

---## 📚 Table of Contents

- Features

## ความต้องการของระบบ- Requirements

- Windows 10/11 (64-bit)- Installation

- ติดตั้งและล็อกอิน MetaTrader 5 แล้ว- Configuration

- Python 3.8 ขึ้นไป- Usage

- Strategies

แพ็กเกจ Python (ดูรายละเอียดใน `requirements.txt`):- Indicators

- MetaTrader5, pandas, pandas-ta, mplfinance, matplotlib- Risk Management

- Build Executable

---- Troubleshooting

- License & Disclaimer

## วิธีติดตั้ง

````powershell---

# 1) โคลนโปรเจกต์

git clone https://github.com/kimookpong/MT5-bot-with-python.git## ✨ Features

cd MT5-bot-with-python- Multiple strategies: BULLMARKET, BOLLINGER, SUPERTREND, DONCHAIN

- Real-time chart with toggleable indicators (SuperTrend, Bollinger, EMA/SMA, Donchian, RSI, MACD)

# 2) สร้าง Virtual Environment (แนะนำ)- Modern Tkinter UI: 3-column layout (Controls • Chart • Log)

python -m venv .venv- Live P/L and positions dashboard

.\.venv\Scripts\Activate.ps1- Thai language logs with Buddhist calendar timestamps

- Advanced risk control: cooldown + trailing profit

# 3) ติดตั้ง dependencies- Windows taskbar icon and custom app icon (autobot.ico)

pip install -r requirements.txt

---

# 4) รันโปรแกรม

python mt5_v4.py## 🧩 Requirements

```- Windows 10/11 (64-bit)

- MetaTrader 5 installed and logged in

---- Python 3.8+



## การตั้งค่าPython packages (see requirements.txt):

- กรอก Account / Password / Server ใน UI แล้วกดเชื่อมต่อ- MetaTrader5, pandas, pandas-ta, mplfinance, matplotlib

- ปรับพารามิเตอร์ใน UI ได้ดังนี้:

  - Symbol: เริ่มต้นเป็น XAUUSDm---

  - Interval: 1m, 5m, 15m, 30m, 1h, 4h, 1d (เริ่มต้น 5m)

  - Lot Size: เริ่มต้น 0.01## �️ Installation

  - Trigger Price: ระยะ (ดอลลาร์) สำหรับ Trailing Profit (เริ่มต้น 3)```powershell

  - Max Orders: สูงสุดของออเดอร์ค้าง (เริ่มต้น 100)# 1) Clone

  - Indicator: เริ่มต้นเป็น SUPERTRENDgit clone https://github.com/kimookpong/MT5-bot-with-python.git

cd MT5-bot-with-python

ค่าคงที่เพิ่มเติม (แก้ได้ใน `mt5_v4.py`):

```python# 2) (Recommended) Create venv

COOLDOWN_SECONDS = 20            # เวลาหน่วงป้องกันเข้าออกไวเกินpython -m venv .venv

MINIMUM_TRIGGER_LENGTH = 5       # ขั้นขั้นต่ำของกำไรเพื่ออัปเดต Trailing (ถ้าใช้แบบ fix).\.venv\Scripts\Activate.ps1

````

# 3) Install deps

---pip install -r requirements.txt

## วิธีใช้งาน# 4) Run

1. กด 🔌 Connect และรอข้อความ "✅ เชื่อมต่อสำเร็จ!"python mt5_v4.py

2. ปรับค่าที่ต้องการในพาเนล Parameters```

3. กด 🚀 Start เพื่อเริ่มบอท

4. ติดตามกราฟ, Active Orders, และผลกำไร/ขาดทุนแบบเรียลไทม์---

5. กด ⏸️ Pause เพื่อหยุดชั่วคราวได้ทุกเมื่อ

## ⚙️ Configuration

Log จะแสดงสีและเวลาตามพ.ศ. เพื่ออ่านง่าย- Account, Password, Server: fill in the UI then Connect

- Parameters in UI:

--- - Symbol: XAUUSDm (default)

- Interval: 1m, 5m, 15m, 30m, 1h, 4h, 1d (default 5m)

## กลยุทธ์การเทรด - Lot Size: default 0.01

- BULLMARKET: ใช้ EMA เร็ว/ช้า ตัดกัน + ตัวกรองเทรนด์ - Trigger Price: trailing profit step in USD (default 3)

- BOLLINGER: เทรดตามการแตะแถบและการเบรกเอาท์/รีเวอร์ชัน - Max Orders: default 100

- SUPERTREND: ตามเทรนด์ด้วยแถบ ATR - Indicator: SUPERTREND (default)

- DONCHAIN: เข้าเมื่อราคาเบรกกรอบช่องทาง

Advanced constants (in `mt5_v4.py`):

สัญญาณออก (Exit) พิจารณาจากสัญญาณกลับทิศและการจัดการความเสี่ยงด้านล่าง```python

COOLDOWN_SECONDS = 20

---MINIMUM_TRIGGER_LENGTH = 5

````

## อินดิเคเตอร์

- SuperTrend (period 10, multiplier 3.0)---

- Bollinger Bands (period 20, std 2.0)

- EMA/SMA (เช่น EMA 9/21, EMA 200, SMA 50)## � Usage

- Donchian Channels1) Click 🔌 Connect (wait for success log)

- RSI (14) และ MACD (12,26,9)2) Adjust parameters if needed

3) Click 🚀 Start to begin trading

สามารถเปิด/ปิดอินดิเคเตอร์เหนือกราฟ และกราฟจะรีเฟรชให้อัตโนมัติ4) Monitor chart, Active Orders, and P/L

5) Click ⏸️ Pause to stop

---

Logs are color-coded and timestamped in Thai calendar.

## การจัดการความเสี่ยง

- Cooldown: ป้องกันเข้าออเดอร์ซ้ำซ้อนในช่วงเวลาใกล้กัน (เริ่มต้น 20 วินาที)---

```python

def is_on_cooldown():## 📈 Strategies

    if get_last_order_time() is None:- BULLMARKET: EMA fast/slow crossover with trend filter

        return False- BOLLINGER: Band touches and mean reversion/breakout

    return (datetime.now() - get_last_order_time()).total_seconds() < COOLDOWN_SECONDS- SUPERTREND: Trend-following with ATR-based bands

```- DONCHAIN: Channel breakout entries

- Trailing Profit: ล็อกกำไรแบบไดนามิก โดยดูจาก Trigger Price ใน UI

  - เมื่อกำไรปัจจุบัน - กำไรที่ล็อกไว้ > Trigger → อัปเดตจุดล็อกกำไรExit rules depend on opposite signals and risk controls below.

  - ถ้ากำไรลดลงต่ำกว่าจุดล็อก → ปิดออเดอร์อัตโนมัติและรีเซ็ต

---

ตัวอย่าง:

- ตั้ง Trigger = 3 ดอลลาร์ → ล็อกกำไรที่ 3, จากนั้น 6, 9, ...## � Indicators

- หากกำไรจาก 6 ลดลงมาเหลือ 5 → ระบบจะปิดออเดอร์ให้อัตโนมัติ- SuperTrend (period 10, multiplier 3.0)

- Bollinger Bands (period 20, std 2.0)

---- EMA/SMA (e.g., EMA 9/21, EMA 200, SMA 50)

- Donchian Channels

## การสร้างไฟล์ .exe- RSI (14) and MACD (12,26,9)

```powershell

pip install pyinstallerToggle indicators above the chart; the view refreshes automatically.

pyinstaller --onefile --windowed --icon=autobot.ico --add-data "autobot.ico;." --name MT5_Autobot_v4.3 mt5_v4.py

```---

ไฟล์จะถูกสร้างที่ `dist\MT5_Autobot_v4.3.exe`

## 🛡️ Risk Management

---- Cooldown: prevents immediate re-entry for 20 seconds

```python

## การแก้ไขปัญหาdef is_on_cooldown():

- เชื่อมต่อไม่ได้: ตรวจสอบบัญชี, รหัสผ่าน, server, เปิด MT5 แล้วหรือไม่, อินเทอร์เน็ต      if get_last_order_time() is None:

- ไม่ส่งออเดอร์: ตลาดปิด, สัญลักษณ์ไม่ถูกต้อง, lot ไม่เหมาะสม            return False

- เข้าออกไวเกิน: เพิ่มค่า COOLDOWN_SECONDS      return (datetime.now() - get_last_order_time()).total_seconds() < COOLDOWN_SECONDS

- กราฟไม่อัปเดต: ตรวจสอบการเชื่อมต่อ, ลองสลับเปิด/ปิดอินดิเคเตอร์```

- Trailing Profit: dynamic protection based on Trigger Price

---   - When profit - locked_profit > Trigger → update lock

   - If profit < locked_profit → force close and reset

## ใบอนุญาต (License)

MIT License — ดูรายละเอียดในไฟล์ของโปรเจกต์Example:

- Trigger = $3 → lock at $3, then $6, $9, ...

## ข้อจำกัดความรับผิดชอบ (Disclaimer)- If profit drops below last lock (e.g., from $6 to $5), position auto-closes

ซอฟต์แวร์นี้จัดทำเพื่อการศึกษาเท่านั้น การเทรดมีความเสี่ยงสูง ควรทดสอบในบัญชีเดโมก่อน ผู้พัฒนาไม่รับผิดชอบความเสียหายใดๆ ที่อาจเกิดขึ้น

---

---

## 📦 Build Executable

พัฒนาโดย kimookpong — v4.3```powershell

pip install pyinstaller
pyinstaller --onefile --windowed --icon=autobot.ico --add-data "autobot.ico;." --name MT5_Autobot_v4.3 mt5_v4.py
````

Output: `dist\MT5_Autobot_v4.3.exe`

---

## 🔧 Troubleshooting

- Cannot connect: check credentials, server, MT5 running, internet
- No orders: market closed, symbol invalid, lot too small/large
- Rapid entries: increase COOLDOWN_SECONDS
- Chart not updating: ensure connection, toggle indicators to refresh

---

## 📄 License

MIT License — see file header in this repo

## ⚠️ Disclaimer

For educational use only. Trading involves risk. Test on demo first. The author is not responsible for losses.

---

Made with ❤️ by kimookpong — v4.3

Entry: $2,000

Profit reaches $3 → Lock profit at $3matplotlib#### Exit Signals

Profit reaches $6 → Lock profit at $6

Profit drops to $5 → Auto-close (locked at $6)tkinter

Result: Protected $5 profit instead of riding down

`````- **Position Closing**: Based on Supertrend direction reversal



### Position Management- **Stop Loss**: Automatic based on Supertrend levels

- Maximum concurrent positions configurable

- Automatic position closure on strategy exit signals### Hardware (แนะนำ)- **Take Profit**: Dynamic adjustment with trend

- Real-time P/L tracking per position

- **CPU:** Intel i5 / AMD Ryzen 5 หรือสูงกว่า

---

- **RAM:** 4 GB ขึ้นไป## 🔧 Configuration

## 💻 Usage

- **Storage:** 500 MB ว่าง

### Step 1: Connect to MT5

1. Launch MT5 Autobot- **Internet:** เชื่อมต่อคงที่### Symbol Settings

2. Enter your account credentials

3. Click **🔌 Connect**

4. Wait for "✅ เชื่อมต่อสำเร็จ!" message

---```python

### Step 2: Configure Parameters

1. Select **Symbol** (e.g., XAUUSDm, BTCUSDm)# Default symbol (can be changed in GUI)

2. Choose **Interval** (1m, 5m, 15m, etc.)

3. Set **Lot Size** (recommended: 0.01 for testing)## 🚀 การติดตั้ง (Installation)symbol = "XAUUSD"

4. Set **Trigger Price** for trailing profit

5. Choose **Indicator** strategy



### Step 3: Start Trading### วิธีที่ 1: ใช้ไฟล์ .exe (แนะนำ) ⭐# Lot size options

1. Click **🚀 Start** button

2. Monitor chart and trading loglot_sizes = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]

3. Watch for entry/exit signals

4. Track P/L in real-time1. ดาวน์โหลดไฟล์ `MT5_Autobot_v4.2.exe` จากโฟลเดอร์ `dist/````



### Step 4: Monitor & Adjust

- Check **Trading Log** for all actions

- Monitor **Active Orders** in dashboard2. Double-click ไฟล์ `.exe` เพื่อเปิดโปรแกรม### Indicator Parameters

- Adjust indicators using toggle controls

- Pause bot anytime with **⏸️ Pause**



---3. เสร็จแล้ว! ไม่ต้องติดตั้งอะไรเพิ่ม```python



## 📦 Building Executable# Supertrend settings (optimized for 5M)



### Create Standalone .exe File### วิธีที่ 2: รันจาก Source Codesupertrend_length = 10



**Step 1: Install PyInstaller**supertrend_multiplier = 2.5

```bash

pip install pyinstaller#### 1. Clone Repository

`````

``````bash# Bollinger Bands

**Step 2: Build Executable**

```bashgit clone https://github.com/kimookpong/MT5-bot-with-python.gitbb_length = 20

pyinstaller --onefile --windowed --icon=autobot.ico --add-data "autobot.ico;." --name MT5_Autobot_v4.3 mt5_v4.py

```cd MT5-bot-with-pythonbb_std = 2



**Step 3: Locate Executable**`````

``````

Output: dist\MT5_Autobot_v4.3.exe# MACD

````````

#### 2. สร้าง Virtual Environmentmacd_fast = 12

### Build Options

- `--onefile`: Single executable file````bashmacd_slow = 26

- `--windowed`: No console window (GUI only)

- `--icon`: Custom application iconpython -m venv .venvmacd_signal = 9

- `--add-data`: Include icon file in build

- `--name`: Executable name.venv\Scripts\activate



---```# RSI



## 🔧 Troubleshootingrsi_length = 14



### Connection Issues#### 3. ติดตั้ง Dependencies```



**Problem**: "❌ เชื่อมต่อล้มเหลว"```bash

- ✅ Verify MT5 is running

- ✅ Check account credentialspip install -r requirements.txt## 📁 Project Structure

- ✅ Confirm server name is correct

- ✅ Ensure MT5 allows algorithmic trading````



**Problem**: "❌ เข้าระบบล้มเหลว"```````

- ✅ Double-check password

- ✅ Verify account is active#### 4. รันโปรแกรมMT5-bot-with-python/

- ✅ Check internet connection

```bash├── mt5_v4.py              # Main application file

### Trading Issues

python mt5_v4.py├── mt5_v3.py              # Previous version

**Problem**: Orders not executing

- ✅ Check symbol is available```├── mt5_v2.py              # Legacy version

- ✅ Verify market is open

- ✅ Ensure sufficient balance├── mt5.py                 # Original version

- ✅ Check lot size is valid for symbol

#### 5. Build เป็น .exe (Optional)├── future.py              # Development features

**Problem**: Rapid entry/exit cycles

- ✅ Cooldown system should prevent this (20 seconds)```bash├── icon.ico               # Application icon

- ✅ Check logs for cooldown messages

- ✅ Increase COOLDOWN_SECONDS if neededpyinstaller --onefile --windowed --icon=icon.ico \├── main.py                # Alternative entry point



### Chart Issues  --name "MT5_Autobot_v4.2" \├── README.md              # This file



**Problem**: Chart not updating  --hidden-import=MetaTrader5 \├── requirements.txt       # Python dependencies

- ✅ Check MT5 connection

- ✅ Verify symbol has data  --hidden-import=pandas_ta \├── build/                 # PyInstaller build files

- ✅ Toggle indicators on/off to refresh

  --hidden-import=mplfinance \├── dist/                  # Compiled executables

**Problem**: Indicators not showing

- ✅ Check indicator toggle switches  --hidden-import=matplotlib \└── .venv/                 # Virtual environment

- ✅ Ensure sufficient data (need 200+ candles for some indicators)

- ✅ Verify pandas_ta is installed correctly  --hidden-import=matplotlib.backends.backend_tkagg \```



---  --hidden-import=plotly \



## 📞 Contact  --hidden-import=tkinter \## 🔨 Building Executable



**Developer**: Kimookpong    --add-data "icon.ico;." \

**Email**: kimookpong@gmail.com

**GitHub**: [kimookpong](https://github.com/kimookpong)    --noconsole \To create a standalone executable:

**Version**: 4.3

  mt5_v4.py

---

``````bash

## 📄 License

# Install PyInstaller

This project is licensed under the MIT License.

---pip install pyinstaller

````````

MIT License

Copyright (c) 2024-2025 Kimookpong## 📖 วิธีใช้งาน (How to Use)# Build executable

Permission is hereby granted, free of charge, to any person obtaining a copy.venv\Scripts\pyinstaller.exe --onefile --windowed --icon=icon.ico \

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights### 1️⃣ เปิดโปรแกรม --hidden-import=MetaTrader5 \

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is --hidden-import=pandas_ta \

furnished to do so, subject to the following conditions:

- ดับเบิลคลิก `MT5_Autobot_v4.2.exe` --hidden-import=mplfinance \

The above copyright notice and this permission notice shall be included in all

copies or substantial portions of the Software.- โปรแกรมจะเปิดเป็นหน้าต่างขนาดเต็มจอ --hidden-import=matplotlib \

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR --hidden-import=plotly \

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,

FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE### 2️⃣ เชื่อมต่อ MT5 --name "MT5_Trading_Bot_v4_1" mt5_v4.py

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,```````

OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

SOFTWARE.**กรอกข้อมูลใน Connection Section:**

```

The executable will be created in the `dist/` directory.

---

```

## ⚠️ Disclaimer

Account: [หมายเลขบัญชี MT5]## ⚠️ Risk Disclaimer

**IMPORTANT**: This software is for educational and research purposes only.

Password: [รหัสผ่าน]

- ⚠️ Trading involves substantial risk of loss

- ⚠️ Past performance does not guarantee future resultsServer: [ชื่อ Server เช่น Exness-MT5Real17]**IMPORTANT**: This software is for educational and research purposes only.

- ⚠️ Use at your own risk

- ⚠️ Test thoroughly on demo accounts before live trading```

- ⚠️ The developer is not responsible for any financial losses

- ⚠️ Never risk more than you can afford to lose- **Trading Risk**: Forex and CFD trading involves substantial risk of loss

**Recommended Practice**:**กด 🔌 Connect**- **No Guarantee**: Past performance does not guarantee future results

1. Start with demo account

2. Test strategies thoroughly- **Use at Your Own Risk**: Always test strategies on demo accounts first

3. Understand all parameters

4. Start with minimum lot sizesหลังเชื่อมต่อสำเร็จจะเห็น:- **Capital Risk**: Never risk more than you can afford to lose

5. Monitor closely during initial live trading

6. Never risk more than you can afford to lose````

---✅ [SUCCESS] Successfully connected to MT5!## 🤝 Contributing

## 🔄 Version History💰 Balance: $XXX.XX USD

### v4.3 (Current)```Contributions are welcome! Please feel free to submit pull requests or open issues for:

- ✨ Added Trailing Profit system with configurable triggers

- 🛡️ Implemented 20-second cooldown to prevent rapid trading

- 🎨 Enhanced UI with modern light theme

- 📊 Added real-time indicator toggle controls### 3️⃣ ตั้งค่า Parameters- Bug fixes

- 🔧 Fixed rapid close/reopen cycle issues

- 🎯 Improved position management logic- Feature enhancements

- 🪟 Added Windows taskbar icon support

- 🇹🇭 Full Thai language interface with Buddhist calendar**Symbol:** เลือกสินทรัพย์- Strategy improvements

### v4.2- `XAUUSDm` - ทองคำ (แนะนำ)- Documentation updates

- Previous version with basic features

- `BTCUSDm` - Bitcoin

---

## 📄 License

## 🙏 Acknowledgments

**Interval:** เลือก Timeframe

- **MetaTrader 5** - Trading platform

- **pandas-ta** - Technical analysis library- `1m`, `5m` ⭐ (แนะนำ), `15m`, `30m`, `1h`, `4h`, `1d`This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

- **mplfinance** - Financial charting

- **matplotlib** - Plotting library

---**Lot Size:** ขนาดออเดอร์## 👨‍💻 Author

## 🌟 Star History- เริ่มต้นที่ `0.01` (แนะนำสำหรับบัญชีใหม่)

If you find this project helpful, please consider giving it a ⭐ on GitHub!- ปรับตามความเสี่ยงที่รับได้**Kimookpong**

[![Star History Chart](https://api.star-history.com/svg?repos=kimookpong/MT5-bot-with-python&type=Date)](https://star-history.com/#kimookpong/MT5-bot-with-python&Date)

---**Max Orders:** จำนวนออเดอร์สูงสุด- GitHub: [@kimookpong](https://github.com/kimookpong)

**Happy Trading! 🚀📈💰**- ค่าเริ่มต้น: `100`

- บอทจะหยุดเมื่อทำครบตามจำนวน## 🙏 Acknowledgments

**Indicator:** เลือกกลยุทธ์- MetaTrader 5 team for the excellent trading platform API

- **SUPERTREND** ⭐ (แนะนำสำหรับมือใหม่)- pandas-ta library for technical analysis indicators

- BULLMARKET- matplotlib and mplfinance for chart visualization

- BOLLINGER- Python community for the amazing ecosystem

- DONCHAIN

## 📞 Support

### 4️⃣ เริ่มการเทรด

If you encounter any issues or have questions:

1. กด **🚀 Start** เพื่อเริ่มบอท

1. Check the [Issues](https://github.com/kimookpong/MT5-bot-with-python/issues) section

1. ดู Trading Dashboard:2. Create a new issue with detailed description

   - **Current Period** - เวลาปัจจุบัน3. Provide error logs and system information

   - **Market Price** - ราคาตลาด

   - **Active Orders** - ออเดอร์ที่เปิดอยู่ + กำไร/ขาดทุน---

   - **Total P/L** - กำไร/ขาดทุนรวม

⭐ **Star this repository if you find it helpful!**

3. ดู Trading Log:

   - ข้อความสีเขียว 🟢 = สำเร็จ/กำไร**Happy Trading! 🚀📈**

   - ข้อความสีแดง 🔴 = ข้อผิดพลาด/ขาดทุน
   - ข้อความสีน้ำเงิน 🔵 = ข้อมูล
   - ข้อความสีเหลือง 🟡 = คำเตือน

### 5️⃣ หยุดการเทรด

- กด **⏸️ Pause** เพื่อหยุดบอทชั่วคราว
- สามารถปรับพารามิเตอร์ได้ในขณะหยุด
- กด **🚀 Start** อีกครั้งเพื่อทำงานต่อ

### 6️⃣ ตัดการเชื่อมต่อ

- กด **🔌 Disconnect** เมื่อต้องการปิดโปรแกรม
- ออเดอร์ที่เปิดอยู่จะยังคงอยู่ใน MT5

---

## 🎯 กลยุทธ์การเทรด (Trading Strategies)

### 🌟 SUPERTREND Strategy (แนะนำ)

#### Entry Conditions (เงื่อนไขเข้าออเดอร์)

**BUY Signal:**

1. ✅ Supertrend เปลี่ยนเป็น Bullish (เขียว)
2. ✅ RSI อยู่ระหว่าง **40-60** (โซนที่เหมาะสม)
3. ✅ RSI กำลังเพิ่มขึ้น (มี momentum)

**SELL Signal:**

1. ✅ Supertrend เปลี่ยนเป็น Bearish (แดง)
2. ✅ RSI อยู่ระหว่าง **40-60**
3. ✅ RSI กำลังลดลง (มี momentum)

#### Exit Conditions (เงื่อนไขปิดออเดอร์)

**1. Hard Stop-Loss (-2%)**

````

ถ้าราคาเคลื่อนที่ติดลบ > -2% → ปิดทันที

```

**2. Signal-Based Exit**
```

BUY: ปิดเมื่อ Supertrend เปลี่ยนเป็น Bearish
SELL: ปิดเมื่อ Supertrend เปลี่ยนเป็น Bullish

```

**3. Dynamic Trailing Stop (4 Tiers)**
```

Tier 4 (1.5-3x lot): ล็อคกำไร 60%, min 1x lot
Tier 3 (3-4x lot): ล็อคกำไร 70%, min 2x lot
Tier 2 (4-5x lot): ล็อคกำไร 80%, min 4x lot
Tier 1 (>5x lot): ปิดออเดอร์ทันที

```

**4. RSI Extreme Exit**
```

BUY: ปิดเมื่อ RSI > 80 (Overbought)
SELL: ปิดเมื่อ RSI < 20 (Oversold)

```

#### ตัวอย่างการทำงาน

**Lot = 0.01 (lot_value = $1)**

```

กำไร $2.00 → Tier 4 active → ล็อคที่ $1.20 (60%)
กำไร $3.50 → Tier 3 active → ล็อคที่ $2.45 (70%)
กำไร $4.50 → Tier 2 active → ล็อคที่ $3.60 (80%)
กำไร $6.00 → Tier 1 active → ปิดทันที!

```

### 📈 BULLMARKET Strategy

**Entry:**
- BUY: EMA21 crosses above SMA20 + RSI < 70
- SELL: EMA21 crosses below SMA20 + RSI > 30

**Exit:**
- Opposite crossover
- Trailing stop profit

### 📊 BOLLINGER Strategy

**Entry:**
- BUY: Price breaks below lower band + RSI < 70
- SELL: Price breaks above upper band + RSI > 30

**Exit:**
- Price reaches opposite band
- Trailing stop profit

### 📦 DONCHAIN Strategy

**Entry:**
- BUY: Price breaks above upper channel + RSI < 70
- SELL: Price breaks below lower channel + RSI > 30

**Exit:**
- Price breaks opposite channel
- Trailing stop profit

---

## ⚙️ การตั้งค่าพารามิเตอร์ (Parameters)

### Lot Size Calculator

| บัญชี | Lot Size | Risk per Trade | Max Drawdown |
|-------|----------|----------------|--------------|
| $100  | 0.01     | ~$2            | ~$10         |
| $500  | 0.05     | ~$10           | ~$50         |
| $1000 | 0.10     | ~$20           | ~$100        |
| $5000 | 0.50     | ~$100          | ~$500        |

**สูตรคำนวณ:**
```

Lot Size = (Account Balance × Risk %) / (Stop Loss in USD × 100)

````

### Recommended Settings

#### Conservative (ปลอดภัย)

```yaml
Symbol: XAUUSDm
Interval: 5m
Lot Size: 0.01
Max Orders: 50
Indicator: SUPERTREND
```

#### Moderate (กลางๆ)

```yaml
Symbol: XAUUSDm
Interval: 5m
Lot Size: 0.02-0.05
Max Orders: 100
Indicator: SUPERTREND
```

#### Aggressive (เสี่ยงสูง)

```yaml
Symbol: XAUUSDm
Interval: 5m
Lot Size: 0.10+
Max Orders: 200
Indicator: SUPERTREND
```

---

## 📊 ตัวอย่าง Log Messages

### Entry Signals

```
✓ [ST] BUY ENTRY - Supertrend bullish + RSI optimal at 52.3
✓ [ST] SELL ENTRY - Supertrend bearish + RSI optimal at 48.7
```

### Trailing Stop Updates

```
💎 [ST] Tier 2 activated: Trailing stop updated to 3.60 USD (70% of 5.14 USD)
💰 [ST] Tier 3 activated: Trailing stop updated to 2.45 USD (60% of 4.08 USD)
```

### Exit Signals

```
🛑 [ST] Trailing stop triggered at 3.45 USD (was protected at 3.60 USD)
[ST] Hard stop-loss triggered at -2.15% | Loss: -2.30 USD
[ST] BUY closed on bearish signal | P/L: 1.85 USD
```

---

## ❓ คำถามที่พบบ่อย (FAQ)

### Q: โปรแกรมต้องการ Internet ตลอดเวลาไหม?

**A:** ใช่ ต้องเชื่อมต่ออินเทอร์เน็ตเพื่อเชื่อมต่อกับ MT5 และรับข้อมูลราคาแบบ Real-time

### Q: สามารถรันหลาย Symbol พร้อมกันได้ไหม?

**A:** ปัจจุบันรันได้ทีละ Symbol เท่านั้น หากต้องการรันหลาย Symbol ต้องเปิดโปรแกรมหลายหน้าต่าง

### Q: บอทจะเทรดต่อถ้าปิดโปรแกรมไหม?

**A:** ไม่ เมื่อปิดโปรแกรมบอทจะหยุดทำงาน แต่ออเดอร์ที่เปิดอยู่ยังคงอยู่ใน MT5

### Q: รองรับบัญชี Demo ไหม?

**A:** รองรับทั้งบัญชี Demo และ Real

### Q: Lot Size ขั้นต่ำคือเท่าไหร่?

**A:** ขึ้นอยู่กับ Broker แต่ปกติคือ 0.01 lot

### Q: สามารถใช้กับคู่เงินอื่นได้ไหม?

**A:** ตอนนี้รองรับเฉพาะ XAUUSDm และ BTCUSDm แต่สามารถแก้ไข code เพื่อเพิ่ม Symbol ได้

### Q: ทำไมบางครั้งไม่มีการเทรด?

**A:** เพราะเงื่อนไขการเข้าออเดอร์ค่อนข้างเข้มงวด (RSI 40-60 + momentum) เพื่อลดสัญญาณเท็จ

---

## 🔧 การแก้ไขปัญหา (Troubleshooting)

### ปัญหา: เชื่อมต่อ MT5 ไม่ได้

**สาเหตุ:**

- MT5 ไม่ได้เปิด
- ข้อมูล Account/Password/Server ผิด
- MT5 ไม่อนุญาตให้ Algo Trading

**วิธีแก้:**

1. เปิด MT5 ก่อนรันโปรแกรม
2. ตรวจสอบข้อมูลให้ถูกต้อง
3. ใน MT5: Tools → Options → Expert Advisors → ✅ Allow Algo Trading

### ปัญหา: ไม่มีการเทรด

**สาเหตุ:**

- เงื่อนไขการเข้าออเดอร์ไม่เป็นจริง
- Symbol ไม่มีใน Market Watch
- Max Orders ครบแล้ว

**วิธีแก้:**

1. ตรวจสอบ Trading Log
2. เพิ่ม Symbol ใน Market Watch ของ MT5
3. เพิ่มค่า Max Orders

### ปัญหา: โปรแกรมช้า/ค้าง

**สาเหตุ:**

- RAM ไม่เพียงพอ
- Internet connection ไม่เสถียร
- เปิด Indicator เยอะเกินไป

**วิธีแก้:**

1. ปิดโปรแกรมอื่นที่ไม่จำเป็น
2. ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
3. ปิด RSI/MACD Chart ถ้าไม่ได้ใช้

### ปัญหา: Order ไม่ผ่าน

**สาเหตุ:**

- Margin ไม่พอ
- Symbol ปิดตลาด
- Broker ไม่อนุญาต

**วิธีแก้:**

1. เช็ค Free Margin ใน MT5
2. ตรวจสอบเวลาทำการของตลาด
3. ติดต่อ Broker

---

## 📈 Performance Tips

### เพิ่มประสิทธิภาพการเทรด

1. **เริ่มต้นด้วย Demo Account**

   - ทดสอบกลยุทธ์ก่อนใช้เงินจริง
   - ปรับ Lot Size ให้เหมาะสม

2. **ใช้ SUPERTREND Strategy**

   - มีระบบจัดการความเสี่ยงดีที่สุด
   - Win rate สูงกว่ากลยุทธ์อื่น

3. **เลือก Timeframe ที่เหมาะสม**

   - 5m ⭐ (แนะนำ) - สมดุลระหว่างโอกาสและความเสี่ยง
   - 15m - สัญญาณน้อยแต่แม่นยำกว่า

4. **ติดตาม Trading Log**

   - วิเคราะห์ pattern ของการเทรด
   - ปรับกลยุทธ์ตามผลลัพธ์

5. **จัดการ Risk**
   - อย่าใช้ Lot Size สูงเกินไป
   - ตั้ง Max Orders ให้เหมาะสมกับเงินทุน

---

## 📸 Screenshots

### Main Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  🔗 Connection    │  📊 Trading Chart    │  📝 Trading Log  │
│  ⚙️ Parameters    │  📈 Live Price       │  🟢 Success      │
│  🤖 Bot Control   │  💹 Indicators       │  🔴 Error        │
│  💰 Account Info  │  📉 Chart Controls   │  🔵 Info         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Changelog

### Version 4.2 (Current)

- ✨ เพิ่มระบบ Dynamic Trailing Stop แบบ 4 Tiers
- 🛡️ Hard Stop-Loss ที่ -2%
- 🎯 RSI Extreme Exit
- 💎 Entry Filters ด้วย RSI 40-60 + Momentum
- 📊 ปรับปรุง UI และ Trading Log
- 🚀 เพิ่มประสิทธิภาพการทำงาน

### Version 4.1

- เพิ่ม Connection Profile Management
- ปรับปรุง Chart Indicators
- เพิ่ม Contact Information

### Version 4.0

- เพิ่ม SUPERTREND Strategy
- ปรับปรุง RSI Filtering
- เพิ่ม Chart Controls

---

## 🤝 Support & Contact

### ติดต่อผู้พัฒนา

- **Email:** kimookpong@gmail.com
- **GitHub:** [kimookpong/MT5-bot-with-python](https://github.com/kimookpong/MT5-bot-with-python)

### การสนับสนุนโปรเจค

ถ้าคุณชอบโปรเจคนี้ สามารถสนับสนุนได้โดย:

- ⭐ Star บน GitHub
- 🐛 Report bugs ผ่าน Issues
- 💡 แนะนำฟีเจอร์ใหม่
- 🔀 Submit Pull Requests

---

## ⚠️ คำเตือน (Disclaimer)

```
⚠️ การเทรดมีความเสี่ยง
- โปรแกรมนี้สร้างขึ้นเพื่อการศึกษาและทดสอบ
- ไม่รับประกันผลกำไรหรือความสำเร็จ
- ผู้ใช้ต้องรับผิดชอบความเสี่ยงเอง
- ควรเริ่มต้นด้วยบัญชี Demo ก่อนใช้เงินจริง
- ผู้พัฒนาไม่รับผิดชอบต่อความสูญเสียใดๆ
```

---

## 📜 License

MIT License

Copyright (c) 2025 kimookpong

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🎉 Happy Trading!

**Remember:**

- 📚 เรียนรู้อย่างต่อเนื่อง
- 💰 จัดการเงินทุนอย่างรอบคอบ
- 🎯 มีแผนการเทรดที่ชัดเจน
- 😌 อย่าโลภ ควบคุมอารมณ์

---

_Last Updated: 2025-10-16_
_Version: 4.2_
_Created by: kimookpong_
