import time
from audiocore import WaveFile
from audioio import AudioOut
import board
import digitalio
import neopixel
from analogio import AnalogIn
import pwmio
from adafruit_motor import servo
import random

spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True  # enable speaker


# read analog pin A5
analog_value = AnalogIn(board.A5)
analog_value_2 = AnalogIn(board.A6)
pump_pin = digitalio.DigitalInOut(board.A4)
pump_pin.direction = digitalio.Direction.OUTPUT
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=False)
pump_pin.value = False  # ensure pump is off initially
sugarLvl = 0

MorningVFX = open("Morning2.wav", "rb")
AfternoonVFX = open("Afternoon2.wav", "rb")
NightVFX = open("Night2.wav", "rb")
waveMorning = WaveFile(MorningVFX)
waveAfternoon = WaveFile(AfternoonVFX)
waveNight = WaveFile(NightVFX)
audio = AudioOut(board.SPEAKER)
audioToPlay = None
milkAmount = 0


while True:
    # read the analog value (0-65535)
    waterlvl_value = analog_value.value
    lightlvl_value = analog_value_2.value
    print("current waterlvl_dect value is: " + str(waterlvl_value))
    print("current lightlvl_dect value is: " + str(lightlvl_value))
    if waterlvl_value >= 18000:
        sugarLvl = random.randint(0, 2)
        if lightlvl_value < 27001 and lightlvl_value >= 27000:
            pixels[0] = (255, 0, 0)  # Red for No Sugar, Espresso
            audioToPlay = waveMorning
            milkAmount = 80
        elif lightlvl_value >= 27001:
            pixels[0] = (255, 255, 255)  # One White for regular Sugar, Regular Latte
            audioToPlay = waveAfternoon
            milkAmount = 120
        else:
            pixels[0] = (255, 255, 255)  # Two Whites for Double Sugar, Sweet Milky Latte
            pixels[1] = (255, 255, 255)
            audioToPlay = waveNight
            milkAmount = 180

        pixels.show()

        time.sleep(8)
        # ignite the pump
        pump_pin.value = True
        print("Pump ON")
        time.sleep(milkAmount)
        # turn off the pump
        pump_pin.value = False
        print("Pump OFF")
        audio.play(audioToPlay)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(420)  # wait for 7 minutes before next reading

    time.sleep(0.1) 
32