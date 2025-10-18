# 🤖 MT5 Autobot - โปรแกรมเทรดอัตโนมัติสำหรับ MetaTrader 5

โปรแกรมเทรดอัตโนมัติที่มี GUI สวยงาม สำหรับเทรด Forex, Gold (XAU), Bitcoin และสินทรัพย์อื่นๆ ผ่าน MetaTrader 5

![Version](https://img.shields.io/badge/version-4.3-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 คืออะไร?

**MT5 Autobot** คือโปรแกรมเทรดอัตโนมัติที่ใช้งานผ่าน GUI แบบ Full Screen พัฒนาด้วย Python สำหรับเชื่อมต่อกับ MetaTrader 5 โดยมีฟีเจอร์หลัก:

- 📊 **วิเคราะห์กราฟแบบเรียลไทม์** ด้วย Technical Indicators
- 🎯 **เทรดอัตโนมัติ** ตาม Strategy ที่กำหนด
- 💰 **Trailing Profit** ระบบล็อคกำไรอัจฉริยะ
- 🛡️ **Stop Loss อัตโนมัติ** ตามเงื่อนไข Indicator
- 📈 **แสดงกราฟแบบ Interactive** ด้วย Candlestick และ Indicators
- ⏱️ **Cooldown System** ป้องกันการเปิดออเดอร์ติดกัน

---

## ✨ ฟีเจอร์เด่น

### 📊 Indicators ที่รองรับ

- **BULLMARKET** - กลยุทธ์ตามแนวโน้มกระทิง (EMA + RSI)
- **BOLLINGER** - กลยุทธ์ Bollinger Bands + RSI
- **SUPERTREND** - Supertrend Indicator + RSI (ใหม่! 🔥)
- **DONCHAIN** - Donchian Channels Breakout + RSI (ใหม่! 🔥)

### 🎨 หน้าตาสวยงาม

- Modern Light Theme UI
- แสดงสถานะการเชื่อมต่อแบบ Real-time
- กราฟ Candlestick พร้อม Indicators
- แสดงกำไร/ขาดทุนแบบเรียลไทม์
- ระบบ Log แยกสีตามประเภทข้อความ

### 🔧 การตั้งค่าที่ยืดหยุ่น

- เลือกคู่เทรดได้ (XAUUSD, BTCUSD, ฯลฯ)
- เลือก Timeframe (M1, M5, M15, H1, H4, D1)
- ตั้งค่า Lot Size
- กำหนด Trigger Profit
- Cooldown เวลา 20 วินาที

---

## 🚀 วิธีใช้งาน

### 1️⃣ ติดตั้ง Requirements

```bash
pip install -r requirements.txt
```

**ไลบรารีที่ใช้:**

- MetaTrader5 - เชื่อมต่อกับ MT5
- pandas & pandas-ta - จัดการข้อมูลและคำนวณ Indicators
- numpy - คำนวณทางคณิตศาสตร์
- matplotlib & mplfinance - แสดงกราฟ
- plotly - กราฟ Interactive
- tkinter - สร้าง GUI

### 2️⃣ เปิดโปรแกรม

```bash
python mt5_v4.py
```

### 3️⃣ เชื่อมต่อกับ MT5

1. เปิด MetaTrader 5 บนเครื่องก่อน
2. กดปุ่ม **"Connect to MT5"** ในโปรแกรม
3. รอจนสถานะเป็น ✅ **Connected**

### 4️⃣ ตั้งค่าการเทรด

- **Symbol**: เลือกคู่เทรด (เช่น XAUUSD, BTCUSD)
- **Timeframe**: เลือกกรอบเวลา (M1, M5, M15, H1, H4, D1)
- **Indicator**: เลือกกลยุทธ์ที่ต้องการใช้
- **Lot Size**: จำนวน Lot ต่อออเดอร์
- **Trigger Profit**: กำไรขั้นต่ำที่จะเริ่มใช้ Trailing

### 5️⃣ เริ่มเทรด

กดปุ่ม **"Start Bot"** เพื่อเริ่มเทรดอัตโนมัติ 🎯

---

## 📊 หน้าจอโปรแกรม

โปรแกรมแบ่งเป็น 3 ส่วนหลัก:

### 🎛️ ส่วนควบคุม (ซ้าย)

- ปุ่ม Connect/Disconnect MT5
- ตั้งค่าการเทรด
- ปุ่ม Start/Stop Bot
- แสดงสถานะบัญชี

### 📈 กราฟ (กลาง)

- Candlestick Chart แบบเรียลไทม์
- แสดง Indicators ตามที่เลือก
- จุด Buy/Sell Signals
- Volume Bar

### 📋 Log & Stats (ขวา)

- ข้อความ Log แยกสีตามประเภท
- สถิติการเทรด (Orders, Profit/Loss)
- เวลาที่โปรแกรมทำงาน
- จำนวน Periods

---

## ⚙️ กลยุทธ์การเทรด

### 🐂 BULLMARKET Strategy

- ใช้ **EMA Fast (21)**, **EMA Slow (55)**, **EMA Trend (100)** และ **RSI**
- เข้า BUY: เมื่อราคาอยู่เหนือ EMA 100 และย่อตัวลงมาในโซนซื้อ (ระหว่าง EMA 21-55)
- Stop Loss: ปิดออเดอร์เมื่อราคาหลุดแนวรับ EMA Slow

### 📊 BOLLINGER Strategy

- ใช้ Bollinger Bands เพื่อหาจุด Overbought/Oversold
- เข้า BUY: เมื่อราคากลับเข้ามาในกรอบล่าง และ RSI > 30
- เข้า SELL: เมื่อราคากลับเข้ามาในกรอบบน และ RSI < 70
- Take Profit: ปิดที่เส้นกลาง (Middle Band)

### 🔄 SUPERTREND Strategy

- ใช้ **Supertrend Indicator** (Length=12, Multiplier=3.0) และ **RSI**
- เข้า BUY: เมื่อ Supertrend พลิกเป็นสีเขียว (ขาขึ้น) และ RSI > 50
- เข้า SELL: เมื่อ Supertrend พลิกเป็นสีแดง (ขาลง) และ RSI < 50
- Trailing Stop: ใช้เส้น Supertrend เป็น Dynamic Stop Loss
- ปิดออเดอร์อัตโนมัติเมื่อราคาข้ามเส้น Supertrend

### 📦 DONCHAIN Strategy

- ใช้ **Donchian Channels** (Period=25) และ **RSI**
- เข้า BUY: เมื่อราคา Breakout ช่องบน และ RSI > 60
- เข้า SELL: เมื่อราคา Breakdown ช่องล่าง และ RSI < 40
- Stop and Reverse: ปิดออเดอร์เมื่อราคาหลุดช่องตรงข้าม
- Take Profit: ปิดที่เส้นกลาง (Middle Channel) เมื่อมีกำไร

### � Trailing Profit System

- ติดตามและล็อคกำไรอัตโนมัติ
- เมื่อกำไรเพิ่มขึ้นเกิน Trigger จะอัพเดท Trailing
- ปิดออเดอร์อัตโนมัติเมื่อกำไรลดลงจากจุดสูงสุด

---

## 🛡️ ระบบความปลอดภัย

- ✅ **Cooldown 20 วินาที** - ป้องกันการเปิดออเดอร์ติดกัน
- ✅ **Stop Loss อัตโนมัติ** - ตัดขาดทุนตามเงื่อนไขทางเทคนิค
- ✅ **Trailing Profit** - ล็อคกำไรเมื่อตลาดกลับตัว
- ✅ **ตรวจสอบ Symbol** - แจ้งเตือนถ้าไม่พบคู่เทรด

---

## 📝 หมายเหตุ

> ⚠️ **คำเตือน**: การเทรดมีความเสี่ยง โปรดศึกษาและทดสอบกับบัญชี Demo ก่อนใช้งานจริง

- โปรแกรมนี้เป็นเครื่องมือช่วยเทรด ไม่ใช่คำแนะนำในการลงทุน
- ควรติดตามและตรวจสอบการทำงานอยู่เสมอ
- ปรับ Lot Size และ Risk Management ให้เหมาะสมกับเงินทุน

---

## 👨‍💻 ผู้พัฒนา

**kimookpong**

Version: 4.3

---

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

---

## 🙏 ขอบคุณ

ขอบคุณทุกท่านที่ใช้งาน หากมีข้อเสนอแนะหรือพบปัญหา สามารถแจ้งได้ครับ

**Happy Trading! 📈💰**
