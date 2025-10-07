import gpiod
import time

# Use the main GPIO controller
chip = gpiod.Chip("gpiochip0")

# Choose the GPIO pin you connected the LED to
LED_PIN = 18

# Get the GPIO line
led = chip.get_line(LED_PIN)

# Request the pin for output
led.request(consumer="blink-test", type=gpiod.LINE_REQ_DIR_OUT)

print("Blinking LED on GPIO", LED_PIN)
while True:
    led.set_value(1)   # LED ON
    time.sleep(0.5)
    led.set_value(0)   # LED OFF
    time.sleep(0.5)
