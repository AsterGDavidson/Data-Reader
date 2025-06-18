
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
PORT = '/dev/cu.usbmodem154739401'  # ← change to your Teensy’s serial port
BAUD = 115200
MAX_POINTS = 500
UPDATE_INTERVAL_MS = 0         # 0 = refresh as fast as possible

# === OPEN SERIAL PORT ===
try:
    ser = serial.Serial(PORT, BAUD, timeout=0)
    time.sleep(2)              
    ser.reset_input_buffer()   
except serial.SerialException as e:
    print(f"Cannot open serial port {PORT}: {e}")
    sys.exit(1)

# === DATA BUFFERS ===
buffers = [deque([0]*MAX_POINTS, maxlen=MAX_POINTS) for _ in range(5)]

# === Qt/PyQtGraph SETUP ===
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(title="Live Teensy 5‑Pot Voltages")
win.show()

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
    while ser.in_waiting > 0:
        try:
            line = ser.readline().decode('ascii', errors='ignore').strip()
        except Exception:
            break
        if not line:
            continue
        parts = line.split()
        if len(parts) != 5:
            continue
        try:
            volts = [float(val) for val in parts]
        except ValueError:
            continue
        for buf, v in zip(buffers, volts):
            buf.append(v)
    for curve, buf in zip(curves, buffers):
        curve.setData(list(buf))

# === TIMER ===
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(UPDATE_INTERVAL_MS)

# === START EVENT LOOP ===
sys.exit(app.exec_())
