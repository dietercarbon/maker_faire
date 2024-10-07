#  Ampel 5242 ped sum Best.py
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

# Fahrzeugampel LEDs: Initialisieren der Pins für Rot, Gelb und Grün.
red_led = Pin(18, Pin.OUT, value=0)       # Rote LED an GPIO 5, ausgeschaltet
yellow_led = Pin(19, Pin.OUT, value=0)    # Gelbe LED an GPIO 4, ausgeschaltet
green_led = Pin(20, Pin.OUT, value=0)     # Grüne LED an GPIO 0, ausgeschaltet

# Fußgängerampel LEDs: Pins für Rot und Grün der Fußgängerampel.
ped_red_led = Pin(9, Pin.OUT, value=0)  # Rote Fußgänger-LED an GPIO 12, ausgeschaltet
ped_green_led = Pin(8, Pin.OUT, value=0) # Grüne Fußgänger-LED an GPIO 13, ausgeschaltet

# Taster für die Fußgängeranforderung: Initialisieren des Tasters als Eingang.
button = Pin(13, Pin.IN, Pin.PULL_DOWN)  # Taster an GPIO 14, Pull-Down-Widerstand aktiviert

# Summer: Initialisieren des Summers, der während der Fußgänger Grün-Phase piept.
buzzer = Pin(0, Pin.OUT, value=0)       # Summer an GPIO 15, ausgeschaltet

# LED-Anzeige für Fußgängeranforderung: Initialisieren der Anzeigelampe.
request_led = Pin(10, Pin.OUT, value=0)  # LED an GPIO 16, ausgeschaltet

# Variable, um den Status der Fußgängeranforderung zu speichern.
pedestrian_request = False

# Zeitvariablen für die Ampelphasen (in Sekunden)
red_duration = 5         # Dauer der Fahrzeug-Rot-Phase
red_yellow_duration = 2   # Dauer der Fahrzeug-Rot-Gelb-Phase
green_duration = 4        # Dauer der Fahrzeug-Grün-Phase
yellow_duration = 2       # Dauer der Fahrzeug-Gelb-Phase

ped_green_duration = 5    # Dauer der Fußgänger-Grün-Phase

# Interrupt-Handler-Funktion: Diese Funktion wird aufgerufen, wenn der Taster gedrückt wird.
def button_handler(pin):
    global pedestrian_request  # Zugriff auf die globale Variable 'pedestrian_request'
    pedestrian_request = True  # Setze die Anforderung auf True, wenn der Taster gedrückt wird
    request_led.on()  # Schalte die Anzeigelampe für die Fußgängeranforderung ein

# Taster-Interrupt: Der Taster ist so konfiguriert, dass er auf steigende Signale reagiert (wenn er gedrückt wird).
# Der Interrupt ruft die Funktion 'button_handler' auf, um die Fußgängeranforderung zu verarbeiten.
button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

# Hauptfunktion zur Steuerung der Fahrzeugampel.
def traffic_light():
    global pedestrian_request  # Zugriff auf die globale Fußgängeranforderungsvariable
    while True:  # Endlos-Schleife für die Ampelsteuerung
        # Fahrzeug Rot-Phase
        red_led.on()      # Schaltet die rote LED für Fahrzeuge ein
        yellow_led.off()  # Schaltet die gelbe LED aus
        green_led.off()   # Schaltet die grüne LED aus
        ped_red_led.on()  # Fußgänger müssen warten, also rote Fußgänger-LED einschalten
        ped_green_led.off()  # Fußgänger grün bleibt aus
        sleep(red_duration)  # Warten für die Dauer der Rot-Phase
        
        # Wenn während der Rot-Phase ein Fußgänger die Ampel anfordert, wird dies hier verarbeitet.
        if pedestrian_request:
            activate_pedestrian_light()  # Fußgängerampel aktivieren
            pedestrian_request = False   # Fußgängeranforderung zurücksetzen
            request_led.off()  # Schalte die Anzeigelampe aus, nachdem die Anforderung bearbeitet wurde
        
        # Fahrzeug Rot-Gelb-Phase
        red_led.on()      # Schaltet die rote LED für Fahrzeuge an
        yellow_led.on()   # Schaltet die gelbe LED für Fahrzeuge ein (Rot-Gelb-Phase)
        green_led.off()   # Grüne LED bleibt aus
        sleep(red_yellow_duration)  # Warten für die Dauer der Rot-Gelb-Phase
        
        # Fahrzeug Grün-Phase
        red_led.off()     # Schaltet die rote LED für Fahrzeuge aus
        yellow_led.off()  # Schaltet die gelbe LED für Fahrzeuge aus
        green_led.on()    # Schaltet die grüne LED für Fahrzeuge ein
        ped_red_led.on()  # Fußgänger müssen weiterhin warten, also rote Fußgänger-LED bleibt an
        ped_green_led.off()  # Fußgänger grün bleibt aus
        sleep(green_duration)  # Warten für die Dauer der Grün-Phase
        
        # Fahrzeug Gelb-Phase
        red_led.off()     # Rote LED bleibt aus
        yellow_led.on()   # Schaltet die gelbe LED für Fahrzeuge ein
        green_led.off()   # Schaltet die grüne LED für Fahrzeuge aus
        sleep(yellow_duration)  # Warten für die Dauer der Gelb-Phase

# Funktion zur Aktivierung der Fußgängerampel.
def activate_pedestrian_light():
    # Fahrzeugampel bleibt auf Rot, während die Fußgänger die Straße überqueren.
    red_led.on()         # Fahrzeug rote LED an
    yellow_led.off()     # Gelbe und grüne LEDs der Fahrzeugampel bleiben aus
    green_led.off()
    
    ped_red_led.off()    # Fußgänger rote LED aus
    ped_green_led.on()   # Fußgänger grüne LED an

    # Der Summer piept rhythmisch, solange die Fußgängerampel grün ist.
    for _ in range(ped_green_duration * 5):  # Wiederholt den Piep-Ton für die Dauer der Grün-Phase
        buzzer.on()   # Schaltet den Summer ein
        sleep(0.1)    # 100ms warten (Summer an)
        buzzer.off()  # Schaltet den Summer aus
        sleep(0.1)    # 100ms warten (Summer aus)
    
    ped_green_led.off()  # Fußgänger grüne LED aus (Übergang zur Rot-Phase)
    ped_red_led.on()     # Fußgänger rote LED an
    sleep(2)  # Kurze Pause (Rot-Phase für Fußgänger) bevor die Fahrzeugampel weitergeht

# Startet die Haupt-Ampelsteuerung
traffic_light()

