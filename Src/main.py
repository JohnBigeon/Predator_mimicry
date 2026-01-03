"""
Created on Sat Dec 28 17:41:49 2024

@author: JBI
"""


"""
###############################################
##Title             : predator_main.py
##Description       : Main script for Predator project
##Author            : John Bigeon   @ Github
##Date              : 20230730
##Version           : Test with
##Usage             : MicroPython (esp32-20220618-v1.19.1)
##Script_version    : 0.0.5 (not_release)
##Output            :
##Notes             :
###############################################
"""
###############################################
### Package
###############################################
import machine
from machine import Pin
import time
from dfplayermini import Player
from time import sleep
from machine import Pin    
import random

###############################################
### Functions
###############################################
# Define the callback function for motion detection
def callbackus(pin, music, led):
    print("Motion detected")
    my_task(music, led)  # Pass the music and led objects to the task

###############################################
### Functions
###############################################
# Define the wrapper function for motion detection
def create_callback(music, led):
    def callbackus(pin):
        print("Motion detected")
        my_task(music, led)  # Pass the music and led objects to the task
    return callbackus
    
def my_task(music, led):
    print("Executing task after motion detection")
    sound_num = random.randint(0,5)
    print(f'Playing sound number {sound_num}')
    music.play(sound_num)
    led.value(1)
    time.sleep(2)
    led.value(0)
    print("stop play with fadeout")
    music.fadeout(2000)
    # music.module_sleep()

###############################################
### Power management part
###############################################
## Via https://docs.micropython.org/en/latest/esp8266/tutorial/powerctrl.html
## https://forum.micropython.org/viewtopic.php?t=3555
# Reduce the CPU frequency
machine.freq(80000000)
freq_machine = machine.freq()
print(f'Machine running at {freq_machine}')

###############################################
### Main loop
###############################################
if __name__ == "__main__":
    ### Init
    pin_pir = Pin(2, mode=Pin.IN, pull=Pin.PULL_UP)  # Initialize the PIR sensor pin
    led = Pin(0, mode=Pin.OUT)  # Initialize the LED pin (GPIO2 as an example)

    # Initialize the music player object
    music = Player(pin_TX=21, pin_RX=20) # Connects TX to module's RX and vice versa #https://www.hackster.io/munir03125344286/df-player-mini-interface-with-esp32-f1efca
    print("Set volume")
    music.volume(100)

    print("Start play")
    music.play(1)

    # Use partial to bind the music and led objects to the callback
    pin_pir.irq(trigger=Pin.IRQ_RISING, handler=create_callback(music, led))
    
    try:
        while True:
            # Sleep to keep the program running; the interrupt will handle detection
            time.sleep_ms(20)
            
    except KeyboardInterrupt:
        print("Program stopped")
