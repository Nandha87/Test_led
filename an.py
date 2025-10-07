import gpiod
import time
import math
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import spi
from luma.lcd.device import st7735

# --- GPIO setup using gpiod (manual control) ---
chip = gpiod.Chip("gpiochip0")  # main GPIO controller

RST_PIN = 27
DC_PIN = 25

# Get GPIO lines
rst = chip.get_line(RST_PIN)
dc = chip.get_line(DC_PIN)

# Request lines as OUTPUT
rst.request(consumer="lcd", type=gpiod.LINE_REQ_DIR_OUT)
dc.request(consumer="lcd", type=gpiod.LINE_REQ_DIR_OUT)

# Reset the display manually
rst.set_value(0)
time.sleep(0.1)
rst.set_value(1)

# --- SPI setup for display (no RST/DC) ---
serial = spi(port=0, device=0, bus_speed_hz=16000000)
device = st7735(serial, width=160, height=80, rotate=0)

# Font for text
font = ImageFont.load_default()

# --- Function to generate color based on time ---
def fade_color(t):
    return (
        int((math.sin(t) * 127) + 128),
        int((math.sin(t + 2) * 127) + 128),
        int((math.sin(t + 4) * 127) + 128),
    )

# --- Main animation loop ---
t = 0
while True:
    # Create image with fading background color
    img = Image.new("RGB", device.size, fade_color(t / 10))
    draw = ImageDraw.Draw(img)
    
    # Draw a pulsing circle
    radius = int(20 + 10 * math.sin(t / 5))
    x, y = device.width // 2, device.height // 2
    draw.ellipse((x - radius, y - radius, x + radius, y + radius),
                 outline="white", width=2)
    
    # Draw text
    text = "Rozaeta"
    w, h = draw.textsize(text, font)
    draw.text(((device.width - w) / 2, (device.height - h) / 2),
              text, font=font, fill="white")
    
    # Display image
    device.display(img)
    
    t += 1
    time.sleep(0.05)
