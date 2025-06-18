#!/usr/bin/env python3
import sys
import time
from collections import deque

try:
    from PyQt5 import QtWidgets, QtCore
    import pyqtgraph as pg
    import serial
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with:\n  pip install pyserial pyqtgraph PyQt5")
    sys.exit(1)

# === CONFIGURATION ===
PORT = '/dev/cu.usbmodem154739401'   # ← change to your Teensy’s port
BAUD = 115200
MAX_POINTS = 500                # rolling buffer length
UPDATE_INTERVAL_MS = 0          # 0 = update as fast as possible

# === OPEN SERIAL PORT ===
try:
    ser = serial.Serial(PORT, BAUD, timeout=0)
    time.sleep(2)
    ser.reset_input_buffer()
except serial.SerialException as e:
    print(f"Failed to open {PORT}: {e}")
    sys.exit(1)

# === DATA BUFFERS ===
buffers = [deque([0]*MAX_POINTS, maxlen=MAX_POINTS) for _ in range(5)]

# === Qt App and Window ===
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(title="Live Teensy 5‑Pot Voltages")
win.show()

# Create five subplots
plots = []
curves = []
for i in range(5):
    p = win.addPlot(row=i, col=0, title=f"Potentiometer A{i}")
    p.setYRange(0, 3.3)
    p.hideAxis('bottom')
    curve = p.plot()
    plots.append(p)
    curves.append(curve)

# === UPDATE CALLBACK ===
def update():
    # read all pending serial lines
    while ser.in_waiting > 0:
        try:
            line = ser.readline().decode('ascii', errors='ignore').strip()
        except Exception:
            break
        parts = line.split(',')
        # expect timestamp + 5 values = 6 parts
        if len(parts) >= 6:
            try:
                vols = [float(v) for v in parts[1:6]]
            except ValueError:
                continue
            # append to buffers
            for buf, v in zip(buffers, vols):
                buf.append(v)
    # update all curves
    for curve, buf in zip(curves, buffers):
        curve.setData(list(buf))

# === TIMER SETUP ===
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(UPDATE_INTERVAL_MS)

# Start Qt event loop
sys.exit(app.exec_())
