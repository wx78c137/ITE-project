import RPi.GPIO as GPIO
import spidev
spi = spidev.SpiDev()
from lib_tft144 import TFT144
TFT = TFT144(GPIO, spi, 0, 24)
TFT.clear_display(TFT.BLUE)
TFT.put_string(“Hello master Vu”, 50, 30, TFT.BLACK, TFT.BLUE, 4)
# This example uses CE0 on the SPI, and GPIO pin22 to “A0” on the module.
# It prints “Hello” near centre of screen, white lettering on all blue background, large font 4.
