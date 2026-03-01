<div align="center">

```
██████╗ ██╗ ██████╗ ██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██║██╔════╝██╔═══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║
██████╔╝██║██║     ██║   ██║███████╗██║     ███████║██╔██╗ ██║
██╔═══╝ ██║██║     ██║   ██║╚════██║██║     ██╔══██║██║╚██╗██║
██║     ██║╚██████╗╚██████╔╝███████║╚██████╗██║  ██║██║ ╚████║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
```

**A passive Wi-Fi network scanner for the Raspberry Pi Pico 2W**  
*No connection required · Colourful serial output · CircuitPython*

![CircuitPython](https://img.shields.io/badge/CircuitPython-10.x-blueviolet?style=flat-square&logo=circuitpython)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20Pico%202W-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![No Libraries](https://img.shields.io/badge/Libraries-None%20Required-brightgreen?style=flat-square)
![Author](https://img.shields.io/badge/Author-flandreiii-cyan?style=flat-square)

</div>

---

## 📡 What is PicoScan?

**PicoScan** turns your Raspberry Pi Pico 2W into a standalone Wi-Fi network scanner. It passively listens for beacon frames from every nearby access point and prints a full colourful report directly to your serial console — **no Wi-Fi connection, no credentials, no extra libraries needed.**

Just flash CircuitPython, drop one file onto the board, and start scanning.

---

## ✨ Features

- 📋 **Shows ALL nearby networks** — no artificial limit on results
- 🔴 **MAC address** for every access point
- 📶 **Signal strength** — visual bar + percentage + raw dBm value
- 🔒 **Security type** — Open, WEP, WPA, WPA2, WPA2-Enterprise, WPA3
- 📻 **Frequency band** — 2.4 GHz or 5 GHz
- 📡 **Channel number** — exact 802.11 channel
- 🏆 **Best & Worst signal** summary after every scan
- 🔄 **Auto-rescans** every 20 seconds
- 🎨 **ANSI colours** — cyan, green, yellow, red, magenta in your terminal
- ⚡ **Zero dependencies** — only built-in CircuitPython modules

---

## 🖥️ Preview

```
  +--------------------------------------------------------------------------------+
  |         >> PICO 2W  Wi-Fi NETWORK SCANNER <<                                  |
  |            CircuitPython  .  Passive Scan  .  No connection required           |
  |            Scan #3  .  18:42:07                                                |
  +--------------------------------------------------------------------------------+

  +------------------------------------------------------------------------------+
   #   SSID                    MAC ADDRESS        CH   BAND  SECURITY    SIGNAL        RSSI
  +------------------------------------------------------------------------------+
   1   HomeNetwork             AA:BB:CC:DD:EE:FF   6   2.4G  WPA2       ***** 94%   -53 dBm
   2   Office_WiFi             11:22:33:44:55:66   1   2.4G  WPA/WPA2   ***.. 61%   -70 dBm
   3   Neighbor_5G             FF:EE:DD:CC:BB:AA  36   5G    WPA2       **... 42%   -79 dBm
   4   FreeWifi                AB:CD:EF:01:23:45  11   2.4G  Open       *.... 20%   -90 dBm
  +------------------------------------------------------------------------------+

  +--------------------------------------------------+
  |  Total: 4   Open: 1   2.4GHz: 3   5GHz: 1   (5.2s)  |
  |  Best signal:  HomeNetwork       -53 dBm  94%        |
  |  Worst signal: FreeWifi          -90 dBm  20%        |
  +--------------------------------------------------+

  4 networks found.
```

---

## 🛠️ Requirements

| Item | Details |
|---|---|
| **Hardware** | Raspberry Pi Pico 2W (RP2350 + CYW43439) |
| **Firmware** | CircuitPython 9.x or 10.x |
| **Libraries** | None — zero external dependencies |
| **Software** | Thonny IDE (recommended) or any serial terminal |

---

## 🚀 Installation

### Step 1 — Flash CircuitPython

1. Hold the **BOOTSEL** button on your Pico 2W and plug it into USB
2. A drive called **RPI-RP2** will appear
3. Download the `.uf2` firmware for the **Pico 2W**:  
   👉 https://circuitpython.org/board/raspberry_pi_pico2_w/
4. Drag the `.uf2` file onto the **RPI-RP2** drive
5. The board reboots and a **CIRCUITPY** drive appears

### Step 2 — Copy the file

Copy `code.py` to the **root** of your CIRCUITPY drive:

```
CIRCUITPY/
└── code.py    ← just this one file, nothing else needed
```

### Step 3 — Open the serial console

Open **Thonny**, select **Run → Configure interpreter → CircuitPython (generic)**, connect to your Pico 2W, and watch the output in the shell panel.

Or use any serial terminal at **115200 baud**:

```bash
# Linux / macOS
screen /dev/ttyACM0 115200

# Windows — use PuTTY or Thonny
```

---

## ⚙️ Configuration

Only one setting you might want to change inside `code.py`:

```python
SCAN_INTERVAL = 20   # seconds between automatic rescans
```

Lower it for more frequent scans, raise it to reduce radio activity.

---

## 📊 Output Explained

| Column | Description |
|---|---|
| `#` | Rank by signal strength (1 = strongest) |
| `SSID` | Network name (`(hidden)` if not broadcast) |
| `MAC ADDRESS` | Hardware address of the access point |
| `CH` | 802.11 channel number |
| `BAND` | `2.4G` or `5G` |
| `SECURITY` | Encryption type of the network |
| `SIGNAL` | Visual bar `*****` + percentage (0–100%) |
| `RSSI` | Raw signal in dBm (closer to 0 = stronger) |

### Signal colour guide

| Colour | Range | Meaning |
|---|---|---|
| 🟢 Green | 70–100% | Strong signal |
| 🟡 Yellow | 40–69% | Medium signal |
| 🔴 Red | 0–39% | Weak signal |

### Security colour guide

| Colour | Type | Meaning |
|---|---|---|
| 🔴 Red | Open | No password — unsecured network |
| 🟡 Yellow | WEP | Legacy encryption — considered insecure |
| 🟢 Green | WPA / WPA2 | Standard modern encryption |
| 🔵 Cyan | WPA3 / Enterprise | Latest / business-grade encryption |

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `No module named 'wifi'` | Thonny is using your PC's Python. Go to **Run → Configure interpreter** and select **CircuitPython (generic)** |
| `No networks found` | Move closer to a router. Make sure `wifi.radio.enabled = True` runs without error |
| Garbled / no colours | Your terminal doesn't support ANSI codes. Use Thonny's shell or Windows Terminal / iTerm2 |
| Board not detected | Try a different USB cable — some cables are charge-only and carry no data |
| Scan seems slow | Normal — the radio collects all beacon frames before returning results |

---

## 📁 Project Structure

```
picoscan/
└── code.py        # Everything — scanner, renderer, main loop
```

One file. That's the whole project.

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Ideas for future features:
- [ ] Save scan results to a `.csv` file on CIRCUITPY
- [ ] Display on an SSD1306 OLED screen
- [ ] Track new networks that appear between scans
- [ ] Count total times each network is seen

---

## 📜 License

```
MIT License

Copyright (c) 2026 flandreiii

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
```

---

<div align="center">

**Made by [flandreiii](https://github.com/flandreiii)**

*PicoScan — because knowing what's around you is always useful 📡*

</div>
