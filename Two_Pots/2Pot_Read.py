import sys
import time
from collections import deque

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import serial

# === CONFIGURATION ===
PORT = '/dev/cu.usbmodem154739401'  # ← change to your actual port
BAUD = 115200
MAX_POINTS = 500
UPDATE_INTERVAL_MS = 0          # 0 = update as fast as possible

# === SERIAL SETUP ===
try:
    ser = serial.Serial(PORT, BAUD, timeout=0)
    time.sleep(2)
    ser.reset_input_buffer()
except serial.SerialException as e:
    print(f"Failed to open serial port {PORT}: {e}")
    sys.exit(1)

# === DATA BUFFERS ===
data0 = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
data1 = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)

# === QT APPLICATION & WINDOW ===
app = QtWidgets.QApplication([])

win = pg.GraphicsLayoutWidget(title="Live Teensy Dual-Pot Voltages")
win.show()

p0 = win.addPlot(row=0, col=0, title="Potentiometer A0")
p0.setYRange(0, 3.3)
p0.hideAxis('bottom')
curve0 = p0.plot()

p1 = win.addPlot(row=1, col=0, title="Potentiometer A1")
p1.setYRange(0, 3.3)
p1.hideAxis('bottom')
curve1 = p1.plot()

# === UPDATE CALLBACK ===
def update():
    while ser.in_waiting > 0:
        try:
            line = ser.readline().decode('ascii', errors='ignore').strip()
        except Exception:
            break
        parts = line.split(',')
        if len(parts) >= 3:
            try:
                v0 = float(parts[1])
                v1 = float(parts[2])
            except ValueError:
                continue
            data0.append(v0)
            data1.append(v1)
    # update plots
    curve0.setData(list(data0))
    curve1.setData(list(data1))

# === TIMER SETUP ===
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(UPDATE_INTERVAL_MS)

# === START EVENT LOOP ===
sys.exit(app.exec_())
