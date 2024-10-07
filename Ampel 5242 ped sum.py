#  Ampel 5242 ped sum.py
#
#  Auto-Ampel:              LED rot (GP 18) und Vor-Widerstand (GND)
#                           LED gelb (GP 19) und Vor-Widerstand (GND)
#                           LED grün (GP 20) und Vor-Widerstand (GND)
#  Fussgänger-Ampel:        LED rot (GP 9) und Vor-Widerstand (GND)
#                           LED grün (GP 8) und Vor-Widerstand (GND)
#  Anforderung:             Taster (3,3V) und (GP 13)
#  optische Bestätigung:    LED blau (GP 10) und Vor-Widerstand (GND)
#  akustische Bestätigung:  aktiver Summer (GP 0) und (GND)

from machine import Pin
from time import sleep

# GPIO-Pins für die Fahrzeugampel definieren und auf 0 setzen (ausgeschaltet)
red_led = Pin(18, Pin.OUT, value=0)
yellow_led = Pin(19, Pin.OUT, value=0)
green_led = Pin(20, Pin.OUT, value=0)

# GPIO-Pins für die Fußgängerampel definieren und auf 0 setzen (ausgeschaltet)
ped_red_led = Pin(9, Pin.OUT, value=0)
ped_green_led = Pin(8, Pin.OUT, value=0)

# GPIO-Pin für den Taster definieren (mit Pull-Down Widerstand)
button = Pin(13, Pin.IN, Pin.PULL_DOWN)

# GPIO-Pin für den Summer definieren und auf 0 setzen (ausgeschaltet)
buzzer = Pin(0, Pin.OUT, value=0)

# Variable zur Speicherung des Zustands der Fußgängerampel
pedestrian_request = False

# Zeitvariablen für alle Phasen (in Sekunden)
red_duration = 5         # Fahrzeug Rot-Phase
red_yellow_duration = 2   # Fahrzeug Rot-Gelb-Phase
green_duration = 4        # Fahrzeug Grün-Phase
yellow_duration = 2       # Fahrzeug Gelb-Phase

ped_green_duration = 5    # Fußgänger Grün-Phase

# Interrupt-Handler für den Taster
def button_handler(pin):
    global pedestrian_request
    pedestrian_request = True  # Fußgänger wollen überqueren

# Taster-Interrupt konfigurieren
button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

# Funktion zur Steuerung der Fahrzeugampel
def traffic_light():
    global pedestrian_request
    while True:
        # Rot-Phase
        red_led.on()
        yellow_led.off()
        green_led.off()
        ped_red_led.on()  # Fußgängerampel bleibt rot
        ped_green_led.off()
        sleep(red_duration)  # Wartezeit für die Rot-Phase
        
        # Überprüfen, ob der Fußgänger die Ampel anfordert
        if pedestrian_request:
            activate_pedestrian_light()  # Fußgängerampel aktivieren
            pedestrian_request = False  # Reset des Anforderungsstatus
        
        # Rot-Gelb-Phase
        red_led.on()
        yellow_led.on()
        green_led.off()
        sleep(red_yellow_duration)  # Wartezeit für die Rot-Gelb-Phase
        
        # Grün-Phase
        red_led.off()
        yellow_led.off()
        green_led.on()
        ped_red_led.on()  # Fußgänger müssen warten, daher rot
        ped_green_led.off()
        sleep(green_duration)  # Wartezeit für die Grün-Phase
        
        # Gelb-Phase
        red_led.off()
        yellow_led.on()
        green_led.off()
        sleep(yellow_duration)  # Wartezeit für die Gelb-Phase

# Funktion zur Aktivierung der Fußgängerampel mit Summer
def activate_pedestrian_light():
    # Fahrzeugampel bleibt auf Rot, während Fußgänger grün haben
    red_led.on()
    yellow_led.off()
    green_led.off()
    
    ped_red_led.off()   # Fußgängerampel auf Grün
    ped_green_led.on()

    # Fußgängerampel grün, Summer piepst
    for _ in range(ped_green_duration * 5):  # Piept 5 mal pro Sekunde
        buzzer.on()
        sleep(0.1)  # Summer für 100ms an
        buzzer.off()
        sleep(0.1)  # Summer für 100ms aus
    
    ped_green_led.off()  # Fußgängerampel wieder auf Rot
    ped_red_led.on()
    sleep(2)  # Kurze Pause bevor die Fahrzeugampel weitergeht

# Ampelsteuerung starten
traffic_light()