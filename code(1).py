"""
Pico 2W - Wi-Fi Network Scanner
Shows ALL networks found. No connection needed.
Just copy to CIRCUITPY and run.
"""

import time
import wifi

# ── ANSI colours ──────────────────────────────────────────────────────────────
RST  = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
RED  = "\033[91m"
GRN  = "\033[92m"
YLW  = "\033[93m"
BLU  = "\033[94m"
MAG  = "\033[95m"
CYN  = "\033[96m"
WHT  = "\033[97m"

def c(text, *codes):
    return "".join(codes) + str(text) + RST

def pad(s, w, right=False):
    s = str(s)
    if len(s) > w:
        s = s[:w-1] + "~"
    spaces = " " * (w - len(s))
    if right:
        return spaces + s
    return s + spaces

# ── Auth names ────────────────────────────────────────────────────────────────
AUTH = {
    0: ("Open",     RED),
    1: ("WEP",      YLW),
    2: ("WPA",      GRN),
    3: ("WPA2",     GRN),
    4: ("WPA/WPA2", GRN),
    5: ("WPA2-Ent", CYN),
    6: ("WPA3",     CYN),
}

# ── Signal bars ───────────────────────────────────────────────────────────────
def sig_bar(q):
    filled = round(q / 20)
    col = GRN if q >= 70 else (YLW if q >= 40 else RED)
    bar = ""
    for i in range(1, 6):
        bar += c("*", col) if i <= filled else c(".", DIM)
    pct = str(q)
    while len(pct) < 3:
        pct = " " + pct
    return bar + " " + c(pct + "%", col, BOLD)

# ── Scan - collect EVERYTHING, no time limit ──────────────────────────────────
def scan():
    networks = []
    seen     = set()

    wifi.radio.enabled = True

    try:
        aps = wifi.radio.start_scanning_networks()
        for ap in aps:
            try:
                mac = ":".join("{:02X}".format(b) for b in bytes(ap.bssid))
            except Exception:
                mac = "??:??:??:??:??:??"

            if mac in seen:
                continue
            seen.add(mac)

            try:
                ssid = ap.ssid if ap.ssid else "(hidden)"
            except Exception:
                ssid = "(hidden)"

            rssi    = ap.rssi
            quality = max(0, min(100, 2 * (rssi + 100)))
            ch      = ap.channel

            if ch == 0:
                band = "?   "
            elif ch <= 14:
                band = "2.4G"
            else:
                band = "5G  "

            try:
                auth = int(ap.authmode)
            except Exception:
                auth = -1

            networks.append({
                "ssid":    ssid,
                "mac":     mac,
                "ch":      ch,
                "band":    band,
                "rssi":    rssi,
                "quality": quality,
                "auth":    auth,
            })
    finally:
        wifi.radio.stop_scanning_networks()

    # sort strongest first
    for i in range(len(networks)):
        for j in range(i + 1, len(networks)):
            if networks[j]["rssi"] > networks[i]["rssi"]:
                networks[i], networks[j] = networks[j], networks[i]

    return networks

# ── Drawing ───────────────────────────────────────────────────────────────────
DIV = c("  +" + "-" * 82 + "+", CYN)

def print_banner(scan_num, ts):
    print()
    print(c("  +--------------------------------------------------------------------------------+", CYN))
    print(c("  |", CYN)
        + c("         >> PICO 2W  Wi-Fi NETWORK SCANNER <<                                  ", WHT, BOLD)
        + c("|", CYN))
    print(c("  |", CYN)
        + c("            CircuitPython  .  Passive Scan  .  No connection required           ", DIM)
        + c("|", CYN))
    print(c("  |", CYN)
        + c("            Scan #" + pad(str(scan_num), 4) + "  .  " + ts + "                                         ", CYN)
        + c("|", CYN))
    print(c("  +--------------------------------------------------------------------------------+", CYN))
    print()

def print_table(networks):
    print(DIV)
    print("  |"
        + c(pad(" #",  3),           CYN, BOLD) + "  "
        + c(pad("SSID", 22),         CYN, BOLD) + "  "
        + c(pad("MAC ADDRESS", 17),  CYN, BOLD) + "  "
        + c(pad("CH",  3),           CYN, BOLD) + "  "
        + c(pad("BAND", 4),          CYN, BOLD) + "  "
        + c(pad("SECURITY", 10),     CYN, BOLD) + "  "
        + c(pad("SIGNAL", 12),       CYN, BOLD) + "  "
        + c(pad("RSSI", 9, right=True), CYN, BOLD)
        + "|")
    print(DIV)

    for i, n in enumerate(networks, 1):
        auth_name, auth_col = AUTH.get(n["auth"], ("?", DIM))

        if n["quality"] >= 70:
            scol = (WHT, BOLD)
        elif n["quality"] >= 40:
            scol = (WHT,)
        else:
            scol = (DIM,)

        rssi_str = str(n["rssi"]) + " dBm"

        print("  |"
            + c(pad(str(i),    3),        DIM)      + "  "
            + c(pad(n["ssid"], 22),       *scol)    + "  "
            + c(pad(n["mac"],  17),       MAG)      + "  "
            + c(pad(n["ch"],   3),        YLW)      + "  "
            + c(pad(n["band"], 4),        BLU)      + "  "
            + c(pad(auth_name, 10),       auth_col) + "  "
            + sig_bar(n["quality"])                 + "  "
            + c(pad(rssi_str, 9, right=True), DIM)
            + "|")

    print(DIV)

def print_summary(networks, elapsed):
    total  = len(networks)
    open_n = sum(1 for n in networks if n["auth"] == 0)
    g24    = sum(1 for n in networks if "2.4" in n["band"])
    g5     = sum(1 for n in networks if "5G"  in n["band"])
    best   = networks[0] if networks else None

    print()
    print(c("  +--------------------------------------------------+", CYN))
    print(c("  |", CYN)
        + "  "
        + c("Total: ",    DIM) + c(pad(str(total),  4), CYN, BOLD)
        + c("  Open: ",   DIM) + c(pad(str(open_n), 4), RED, BOLD)
        + c("  2.4GHz: ", DIM) + c(pad(str(g24),    4), GRN, BOLD)
        + c("  5GHz: ",   DIM) + c(pad(str(g5),     4), YLW, BOLD)
        + c("  time: " + str(round(elapsed, 1)) + "s", DIM)
        + "  " + c("|", CYN))

    if best:
        print(c("  |", CYN)
            + "  "
            + c("Best signal:  ", DIM)
            + c(pad(best["ssid"], 20), WHT, BOLD)
            + "  "
            + c(str(best["rssi"]) + " dBm", GRN)
            + "  "
            + c(str(best["quality"]) + "%", GRN, BOLD)
            + "  " + c("|", CYN))

    worst = networks[-1] if networks else None
    if worst:
        print(c("  |", CYN)
            + "  "
            + c("Worst signal: ", DIM)
            + c(pad(worst["ssid"], 20), DIM)
            + "  "
            + c(str(worst["rssi"]) + " dBm", RED)
            + "  "
            + c(str(worst["quality"]) + "%", RED)
            + "  " + c("|", CYN))

    print(c("  +--------------------------------------------------+", CYN))
    print()

# ── Main loop ─────────────────────────────────────────────────────────────────
SCAN_INTERVAL = 20
scan_num = 0

print()
print(c("  Powering radio...", DIM))
wifi.radio.enabled = True
print(c("  Radio on. Starting scan loop.\n", GRN))

while True:
    scan_num += 1

    now = time.localtime()
    hh  = str(now.tm_hour);  hh = ("0" + hh) if len(hh) < 2 else hh
    mm  = str(now.tm_min);   mm = ("0" + mm)  if len(mm) < 2 else mm
    ss  = str(now.tm_sec);   ss = ("0" + ss)  if len(ss) < 2 else ss
    ts  = hh + ":" + mm + ":" + ss

    print(c("  [" + ts + "]  Scanning... (collecting all networks)", DIM))

    t0       = time.monotonic()
    networks = scan()
    elapsed  = time.monotonic() - t0

    print_banner(scan_num, ts)

    if networks:
        print_table(networks)
        print_summary(networks, elapsed)
        print(c("  " + str(len(networks)) + " networks found.", CYN, BOLD))
    else:
        print(c("  No networks found. Move closer to an access point.", YLW))

    print()
    print(c("  Ctrl+C to stop", DIM))
    print()

    for remaining in range(SCAN_INTERVAL, 0, -1):
        r = str(remaining)
        if len(r) < 2:
            r = " " + r
        print(c("\r  Next scan in " + r + "s ... ", DIM), end="")
        time.sleep(1)

    print("\r" + " " * 35 + "\r")
