#  Ampel 5242.py
#
#  Auto-Ampel:              LED rot (GP 18) und Vor-Widerstand (GND)
#                           LED gelb (GP 19) und Vor-Widerstand (GND)
#                           LED grün (GP 20) und Vor-Widerstand (GND)

from machine import Pin
from time import sleep

# GPIO-Pins für die LEDs definieren
red_led = Pin(18, Pin.OUT)
yellow_led = Pin(19, Pin.OUT)
green_led = Pin(20, Pin.OUT)

# Endlosschleife zur Steuerung der Ampelphasen
while True:
    # Rot-Phase
    red_led.on()
    yellow_led.off()
    green_led.off()
    sleep(5)  # Rot für 5 Sekunden
    
    # Rot-Gelb-Phase
    red_led.on()
    yellow_led.on()
    green_led.off()
    sleep(2)  # Rot-Gelb für 2 Sekunden
    
    # Grün-Phase
    red_led.off()
    yellow_led.off()
    green_led.on()
    sleep(4)  # Grün für 4 Sekunden
    
    # Gelb-Phase
    red_led.off()
    yellow_led.on()
    green_led.off()
    sleep(2)  # Gelb für 2 Sekunden


