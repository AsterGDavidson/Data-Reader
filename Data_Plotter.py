import sys
import time
from collections import deque

try:
    from PyQt5 import QtWidgets, QtCore
    import pyqtgraph as pg
    import serial
except ImportError as e:
    print(f"Missing dependency: {e}. Please run:")
    print("  pip install pyserial pyqtgraph PyQt5")
    sys.exit(1)

# === CONFIGURATION ===
PORT = '/dev/cu.usbmodem154739401'   
BAUD = 115200
MAX_POINTS = 500                
UPDATE_INTERVAL_MS = 0          # 0 = as fast as your machine allows

# === SERIAL SETUP ===
ser = serial.Serial(PORT, BAUD, timeout=0)
time.sleep(2)

# === DATA BUFFER ===
data_buffer = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)

# === QT/PyQtGraph SETUP ===
app = QtWidgets.QApplication([])

win = pg.GraphicsLayoutWidget(title="Live Teensy Voltage")
plot = win.addPlot()
plot.setYRange(0, 5)        
plot.hideAxis('bottom')       
curve = plot.plot()           

win.show()

# === UPDATE CALLBACK ===
def update():
    while True:
        line = ser.readline().decode('ascii', errors='ignore').strip()
        if not line:
            break
        parts = line.split(',')
        try:
            voltage = float(parts[-1])
        except ValueError:
            continue
        data_buffer.append(voltage)
    curve.setData(list(data_buffer))

# === TIMER ===
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(UPDATE_INTERVAL_MS)

# === START EVENT LOOP ===
sys.exit(app.exec_())
