# Write your code here :-)
"""CircuitPython Essentials Servo standard servo example"""
import time
import board
import pwmio
import digitalio
import neopixel

from adafruit_motor import servo

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!
try: 
    import asyncio
except ImportError:
    print("Asyncio not supported on this board.")
    pass

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.15, auto_write=False)

# DimmList = [(0, 0, 0), (12, 12, 12), (24, 24, 24), (32, 32, 32), (48, 48, 48), (64, 64, 64), (80, 80, 80), (96, 96, 96), (112, 112, 112), (128, 128, 128), (144, 144, 144), (160, 160, 160), (176, 176, 176), (192, 192, 192), (208, 208, 208), (224, 224, 224), (240, 240, 240), (255, 255, 255)]

# Create a servo object, my_servo.
my_servo = servo.ContinuousServo(pwm)

switchA = digitalio.DigitalInOut(board.BUTTON_A)
switchA.direction = digitalio.Direction.INPUT
switchA.pull = digitalio.Pull.DOWN

switchB = digitalio.DigitalInOut(board.BUTTON_B)
switchB.direction = digitalio.Direction.INPUT
switchB.pull = digitalio.Pull.DOWN

slide_switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
slide_switch.direction = digitalio.Direction.INPUT
slide_switch.pull = digitalio.Pull.UP

wave_file = open("gameWAV.wav", "rb")
wave_file2 = open("leisure.wav", "rb")
wave = WaveFile(wave_file)
wave2 = WaveFile(wave_file2)
audio = AudioOut(board.SPEAKER)
lastplay = None

startTime = time.monotonic()
flipflop = False

# async def blink_leds():
#     interval = 0.1
#     while True:
#         for color in DimmList:
#             pixels.fill(color)
#             pixels.show()
#             await asyncio.sleep(interval)
#         for color in reversed(DimmList):
#             pixels.fill(color)
#             pixels.show()
#             await asyncio.sleep(interval)

# async def main():
#     asyncio.create_task(blink_leds())

while True:
    print(slide_switch.value)

    if switchA.value:
        if (not audio.playing or lastplay != wave) and slide_switch.value:
            audio.play(wave)
            lastplay = wave
        my_servo.throttle = 1
    elif switchB.value:
        if (not audio.playing or lastplay != wave2) and slide_switch.value:
            audio.play(wave2)
            lastplay = wave2
        my_servo.throttle = -1
    else:
        my_servo.throttle = 0
    
    if slide_switch.value == False:
        audio.stop()
    time.sleep(0.1)

# asyncio.run(main())