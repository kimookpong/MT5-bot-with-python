# MT5 Autobot v4.2 🤖💰# MT5 Trading Bot v4.1

**Automated Trading Bot for MetaTrader 5** with Advanced Technical Analysis and Risk Management🤖 Advanced MetaTrader 5 Automated Trading Bot with Supertrend Strategy and Real-time GUI Dashboard

Created by: **kimookpong** ![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)

Email: kimookpong@gmail.com ![License](https://img.shields.io/badge/license-MIT-green.svg)

Version: **4.2**![MetaTrader5](https://img.shields.io/badge/platform-MT5-orange.svg)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)## 📋 Overview

![License](https://img.shields.io/badge/license-MIT-green.svg)

![MetaTrader5](https://img.shields.io/badge/platform-MT5-orange.svg)This project is a sophisticated automated trading bot designed for MetaTrader 5 platform. It features a modern GUI interface with real-time chart visualization, technical indicator analysis, and automated trading execution based on Supertrend strategy.

---### 🎯 Key Features

## 📋 สารบัญ (Table of Contents)- **🎨 Modern GUI Interface**: Light theme design with intuitive 3-column layout

- **📊 Real-time Chart Visualization**: Interactive candlestick charts with technical indicators

- [ภาพรวม](#-ภาพรวม-overview)- **🔄 Supertrend Strategy**: Optimized for 5-minute timeframe trading

- [คุณสมบัติเด่น](#-คุณสมบัติเด่น-features)- **📈 Technical Indicators**: Supertrend, Bollinger Bands, MACD, RSI

- [ความต้องการของระบบ](#-ความต้องการของระบบ-requirements)- **🛡️ Risk Management**: Built-in stop-loss and take-profit mechanisms

- [การติดตั้ง](#-การติดตั้ง-installation)- **📱 Full-screen Mode**: Default full-screen startup for better visibility

- [วิธีใช้งาน](#-วิธีใช้งาน-how-to-use)- **💰 Live Trading Log**: Real-time position tracking and profit/loss monitoring

- [กลยุทธ์การเทรด](#-กลยุทธการเทรด-trading-strategies)- **🔧 Customizable Parameters**: Adjustable lot sizes, periods, and indicator settings

- [ระบบจัดการความเสี่ยง](#-ระบบจดการความเสยง-risk-management)

- [การตั้งค่าพารามิเตอร์](#-การตงคาพารามเตอร-parameters)## 🚀 Quick Start

- [คำถามที่พบบ่อย](#-คำถามทพบบอย-faq)

- [การแก้ไขปัญหา](#-การแกไขปญหา-troubleshooting)### Prerequisites

---- Windows OS (recommended)

- MetaTrader 5 platform installed and configured

## 🌟 ภาพรวม (Overview)- Python 3.8 or higher

- Active trading account with MetaTrader 5

MT5 Autobot v4.2 คือโปรแกรมเทรดอัตโนมัติสำหรับ MetaTrader 5 ที่มาพร้อมกับ:

- 🎯 4 กลยุทธ์การเทรดที่ทรงพลัง### 📦 Installation

- 📊 เครื่องมือวิเคราะห์ทางเทคนิคครบครัน

- 🛡️ ระบบจัดการความเสี่ยงขั้นสูง1. **Clone the repository**

- 💎 การจัดการกำไรแบบ Dynamic Trailing Stop

- 🎨 UI ที่สวยงามและใช้งานง่าย ```bash

  git clone https://github.com/kimookpong/MT5-bot-with-python.git

--- cd MT5-bot-with-python

````

## ✨ คุณสมบัติเด่น (Features)

2. **Create virtual environment**

### 🎯 Trading Strategies (4 กลยุทธ์)

```bash

1. **BULLMARKET** - Bull Market Support Band   python -m venv .venv

- ใช้ EMA21 และ SMA20 crossover   .venv\Scripts\activate

- เหมาะสำหรับตลาดขาขึ้น   ```



2. **BOLLINGER** - Bollinger Bands Strategy3. **Install dependencies**

- เทรดตาม Bollinger Bands breakout   ```bash

- ดีสำหรับตลาดที่มี volatility   pip install -r requirements.txt

````

3. **SUPERTREND** - Advanced Supertrend Strategy ⭐ (แนะนำ)

   - ใช้ Supertrend Indicator + RSI confirmation### 🔧 Dependencies

   - ระบบจัดการความเสี่ยง 4 ระดับ

   - Dynamic Trailing Stop```txt

   - RSI Momentum FilterMetaTrader5>=5.0.45

pandas>=1.5.0

4. **DONCHAIN** - Donchian Channels Breakoutpandas-ta>=0.3.14b

   - เทรดตาม breakout ของ Donchian Channelsnumpy>=1.21.0

   - เหมาะสำหรับตลาด trendingmatplotlib>=3.5.0

mplfinance>=0.12.0

### 📊 Technical Indicatorsplotly>=5.0.0

tkinter (built-in with Python)

- **Supertrend** (10, 2.5) - ปรับให้เหมาะกับ 5m timeframe```

- **Bollinger Bands** (20, 2) - แถบสำหรับ volatility

- **EMA/SMA** - Moving averages หลากหลาย## 🎮 Usage

- **Donchian Channels** (20) - Support/Resistance zones

- **RSI** (14) - Relative Strength Index### Running the Application

- **MACD** (12, 26, 9) - Momentum indicator

1. **Start MetaTrader 5** and ensure it's logged into your trading account

### 🛡️ Risk Management System

2. **Run the bot**

#### Hard Stop-Loss

- ตั้ง Stop-Loss ที่ **-2%** จากราคาเปิด ```bash

- ป้องกันความเสียหายหนักสำหรับทุกออเดอร์ python mt5_v4.py

  ```

  ```

#### Dynamic Trailing Stop (4 Tiers)

3. **Or use the compiled executable**

**Tier 4** - Low Profit (1.5-3x lot) ```bash

- กำไร: 1.5-3x lot value MT5_Trading_Bot_v4_1.exe

- ล็อคกำไร: **60%** ```

- Minimum profit: **1x lot**

### 🖥️ Interface Overview

**Tier 3** - Medium Profit (3-4x lot)

- กำไร: 3-4x lot valueThe application features a 3-column layout:

- ล็อคกำไร: **70%**

- Minimum profit: **2x lot**- **Left Panel**: Trading controls and settings

**Tier 2** - High Profit (4-5x lot) - Symbol selection (default: XAUUSD)

- กำไร: 4-5x lot value - Period configuration (5-minute recommended)

- ล็อคกำไร: **80%** - Lot size adjustment

- Minimum profit: **4x lot** - Start/Stop trading controls

**Tier 1** - Maximum Profit (>5x lot)- **Center Panel**: Real-time chart visualization

- กำไร: >5x lot value

- **ปิดออเดอร์ทันที** เพื่อล็อคกำไร - Candlestick chart with volume

  - Supertrend indicator overlay

#### RSI Extreme Exit - Buy/Sell signal markers

- ปิด BUY เมื่อ RSI > 80 (Overbought) - Scrollable chart view

- ปิด SELL เมื่อ RSI < 20 (Oversold)

- **Right Panel**: Trading log and statistics

#### Entry Filters (SUPERTREND) - Active positions

- RSI ต้องอยู่ในช่วง **40-60** (Optimal zone) - Order history

- RSI ต้องมี momentum ตามทิศทาง - Profit/Loss tracking

- Supertrend signal confirmation - Performance metrics

---## 📊 Trading Strategy

## 💻 ความต้องการของระบบ (Requirements)### Supertrend Indicator

### SoftwareThe bot uses an optimized Supertrend strategy with the following parameters:

- **Windows 10/11** (64-bit)

- **MetaTrader 5** (ติดตั้งและเปิดใช้งาน)- **Length**: 10 periods

- **Python 3.8+** (สำหรับรันจาก source code)- **Multiplier**: 2.5

- **Timeframe**: 5 minutes (M5)

### Python Libraries (ถ้ารันจาก source)

`````bash#### Entry Signals

MetaTrader5

pandas- **BUY**: When Supertrend direction changes to +1 (bullish)

pandas_ta- **SELL**: When Supertrend direction changes to -1 (bearish)

mplfinance

matplotlib#### Exit Signals

tkinter

```- **Position Closing**: Based on Supertrend direction reversal

- **Stop Loss**: Automatic based on Supertrend levels

### Hardware (แนะนำ)- **Take Profit**: Dynamic adjustment with trend

- **CPU:** Intel i5 / AMD Ryzen 5 หรือสูงกว่า

- **RAM:** 4 GB ขึ้นไป## 🔧 Configuration

- **Storage:** 500 MB ว่าง

- **Internet:** เชื่อมต่อคงที่### Symbol Settings



---```python

# Default symbol (can be changed in GUI)

## 🚀 การติดตั้ง (Installation)symbol = "XAUUSD"



### วิธีที่ 1: ใช้ไฟล์ .exe (แนะนำ) ⭐# Lot size options

lot_sizes = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]

1. ดาวน์โหลดไฟล์ `MT5_Autobot_v4.2.exe` จากโฟลเดอร์ `dist/````



2. Double-click ไฟล์ `.exe` เพื่อเปิดโปรแกรม### Indicator Parameters



3. เสร็จแล้ว! ไม่ต้องติดตั้งอะไรเพิ่ม```python

# Supertrend settings (optimized for 5M)

### วิธีที่ 2: รันจาก Source Codesupertrend_length = 10

supertrend_multiplier = 2.5

#### 1. Clone Repository

```bash# Bollinger Bands

git clone https://github.com/kimookpong/MT5-bot-with-python.gitbb_length = 20

cd MT5-bot-with-pythonbb_std = 2

`````

# MACD

#### 2. สร้าง Virtual Environmentmacd_fast = 12

````bashmacd_slow = 26

python -m venv .venvmacd_signal = 9

.venv\Scripts\activate

```# RSI

rsi_length = 14

#### 3. ติดตั้ง Dependencies```

```bash

pip install -r requirements.txt## 📁 Project Structure

````

```````

#### 4. รันโปรแกรมMT5-bot-with-python/

```bash├── mt5_v4.py              # Main application file

python mt5_v4.py├── mt5_v3.py              # Previous version

```├── mt5_v2.py              # Legacy version

├── mt5.py                 # Original version

#### 5. Build เป็น .exe (Optional)├── future.py              # Development features

```bash├── icon.ico               # Application icon

pyinstaller --onefile --windowed --icon=icon.ico \├── main.py                # Alternative entry point

  --name "MT5_Autobot_v4.2" \├── README.md              # This file

  --hidden-import=MetaTrader5 \├── requirements.txt       # Python dependencies

  --hidden-import=pandas_ta \├── build/                 # PyInstaller build files

  --hidden-import=mplfinance \├── dist/                  # Compiled executables

  --hidden-import=matplotlib \└── .venv/                 # Virtual environment

  --hidden-import=matplotlib.backends.backend_tkagg \```

  --hidden-import=plotly \

  --hidden-import=tkinter \## 🔨 Building Executable

  --add-data "icon.ico;." \

  --noconsole \To create a standalone executable:

  mt5_v4.py

``````bash

# Install PyInstaller

---pip install pyinstaller



## 📖 วิธีใช้งาน (How to Use)# Build executable

.venv\Scripts\pyinstaller.exe --onefile --windowed --icon=icon.ico \

### 1️⃣ เปิดโปรแกรม    --hidden-import=MetaTrader5 \

    --hidden-import=pandas_ta \

- ดับเบิลคลิก `MT5_Autobot_v4.2.exe`    --hidden-import=mplfinance \

- โปรแกรมจะเปิดเป็นหน้าต่างขนาดเต็มจอ    --hidden-import=matplotlib \

    --hidden-import=plotly \

### 2️⃣ เชื่อมต่อ MT5    --name "MT5_Trading_Bot_v4_1" mt5_v4.py

```````

**กรอกข้อมูลใน Connection Section:**

The executable will be created in the `dist/` directory.

```

Account:  [หมายเลขบัญชี MT5]## ⚠️ Risk Disclaimer

Password: [รหัสผ่าน]

Server:   [ชื่อ Server เช่น Exness-MT5Real17]**IMPORTANT**: This software is for educational and research purposes only.

```

- **Trading Risk**: Forex and CFD trading involves substantial risk of loss

**กด 🔌 Connect**- **No Guarantee**: Past performance does not guarantee future results

- **Use at Your Own Risk**: Always test strategies on demo accounts first

หลังเชื่อมต่อสำเร็จจะเห็น:- **Capital Risk**: Never risk more than you can afford to lose

````

✅ [SUCCESS] Successfully connected to MT5!## 🤝 Contributing

💰 Balance: $XXX.XX USD

```Contributions are welcome! Please feel free to submit pull requests or open issues for:



### 3️⃣ ตั้งค่า Parameters- Bug fixes

- Feature enhancements

**Symbol:** เลือกสินทรัพย์- Strategy improvements

- `XAUUSDm` - ทองคำ (แนะนำ)- Documentation updates

- `BTCUSDm` - Bitcoin

## 📄 License

**Interval:** เลือก Timeframe

- `1m`, `5m` ⭐ (แนะนำ), `15m`, `30m`, `1h`, `4h`, `1d`This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



**Lot Size:** ขนาดออเดอร์## 👨‍💻 Author

- เริ่มต้นที่ `0.01` (แนะนำสำหรับบัญชีใหม่)

- ปรับตามความเสี่ยงที่รับได้**Kimookpong**



**Max Orders:** จำนวนออเดอร์สูงสุด- GitHub: [@kimookpong](https://github.com/kimookpong)

- ค่าเริ่มต้น: `100`

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

2. ดู Trading Dashboard:2. Create a new issue with detailed description

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
````

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
