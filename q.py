import gpiod
import time
import math
from PIL import Image
from luma.core.interface.serial import spi
from luma.lcd.device import st7735

# --- GPIO setup ---
chip = gpiod.Chip("gpiochip0")

RST_PIN = 27
DC_PIN = 25

rst = chip.get_line(RST_PIN)
dc = chip.get_line(DC_PIN)

rst.request(consumer="lcd", type=gpiod.LINE_REQ_DIR_OUT)
dc.request(consumer="lcd", type=gpiod.LINE_REQ_DIR_OUT)

# Reset the display
rst.set_value(0)
time.sleep(0.1)
rst.set_value(1)

# --- SPI setup ---
serial = spi(port=0, device=0, bus_speed_hz=16000000)
device = st7735(serial, width=160, height=80, rotate=0)

# --- Function to generate color based on time ---
def fade_color(t):
    return (
        int((math.sin(t) * 127) + 128),
        int((math.sin(t + 2) * 127) + 128),
        int((math.sin(t + 4) * 127) + 128),
    )

# --- Simple animation loop ---
t = 0
while True:
    color = fade_color(t / 10)
    img = Image.new("RGB", device.size, color)
    device.display(img)
    t += 1
    time.sleep(0.05)
