import gpiod
import time

chip = gpiod.Chip("gpiochip0")  # main GPIO controller
config = gpiod.LineSettings(direction=gpiod.LineDirection.OUTPUT)

line = chip.request_lines(
    consumer="LED_Test",
    config={17: config}  # use GPIO 17 (BCM pin)
)

while True:
    line.set_value(17, 1)  # turn LED ON
    time.sleep(1)
    line.set_value(17, 0)  # turn LED OFF
    time.sleep(1)
