import board
import displayio
import terminalio
from adafruit_display_text import label
import digitalio
import adafruit_displayio_ssd1306
import busio
from i2cdisplaybus import I2CDisplayBus
import adafruit_ds1307
import time
import busio
import adafruit_hcsr04
import adafruit_vl53l0x

# --- Configuration ---
# Your OLED's dimensions
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 32
I2C_ADDRESS = 0x3C # Standard I2C address for 128x32 SSD1306
pump_pin = digitalio.DigitalInOut(board.D7)
pump_pin.direction = digitalio.Direction.OUTPUT
pump_pin.value = False  # ensure pump is off initially
displayio.release_displays()
i2c = busio.I2C(board.SCL, board.SDA) 
# sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A5, echo_pin=board.A4)
display_bus = I2CDisplayBus(i2c, device_address=I2C_ADDRESS)
display = adafruit_displayio_ssd1306.SSD1306(
    display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT
)

i2c_time = busio.I2C(scl=board.D1, sda=board.D0)
rtc = adafruit_ds1307.DS1307(i2c_time)
# rtc.datetime = time.struct_time((2025,12,9,20,24,30,1,343,-1)) // for setting time

i2c_dist = busio.I2C(scl=board.A3, sda=board.A2)
vl53_dist = adafruit_vl53l0x.VL53L0X(i2c_dist)
milkLvl = 0
trigger_distance = 130  
consecutive_count = 0
required_consecutive = 10  # counter for stable detection

splash = displayio.Group()
display.root_group = splash
text_area = label.Label(
    terminalio.FONT,
    text="Anyone want\na cup of latte?", 
    color=0xFFFFFF,            
    x=2,                        
    y=4                        
)

# Add the text label to the display group
splash.append(text_area)

while True:
    dist = vl53_dist.range
    try:
        print(dist)
    except RuntimeError:
        print("Retrying!")
    time.sleep(.4)
    
    if dist < trigger_distance:
        consecutive_count += 1
    else:
        consecutive_count = 0
    
    if consecutive_count >= required_consecutive:
        t = rtc.datetime.tm_hour
        if t < 10:
            text_area.text = "Good Morning!\nTime to Wake up!"
            milkLvl = 24
        elif 10 <= t < 14:
            text_area.text = "Ha, So you \nwant a coffee break!"
            milkLvl = 30
        elif 14 <= t < 20:
            text_area.text = "TAKE THIS CUP OF\nLATTE AND KEEP WORKING!"
            milkLvl = 40
        else:
            text_area.text = "Wake Up!\nIt's time for sleep!"
            milkLvl = 64
        display.refresh()
        time.sleep(8)
        # ignite the pump
        pump_pin.value = True
        print("Pump ON")
        time.sleep(milkLvl)
        # turn off the pump
        pump_pin.value = False
        print("Pump OFF")
        time.sleep(4800) # code done running
        
