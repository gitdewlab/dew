"""

DOTMATRIX DIGITAL CLOCK

NETWORK TIME SYNCHRONISED

DARKNESS SENSITIVE DISPLAY

8x32 MAX7219 DOTMATRIX SPACE


------------------------------
DOTMATRIX MODULE CONNECTION:
------------------------------
DOTMATRIX          ESP32

VCC                5V

GND                GND

DIN                D23

CS                 D5

CLK                D18
------------------------------


------------------------------
NEOPIXEL RING CONNECTION:
------------------------------
NEOPIXEL           ESP32

VCC                5V

GND                GND

DIN                D33
------------------------------


------------------------------
MULTI-SENSOR CONNECTION:
------------------------------
MULTI-SENSOR       ESP32

VCC                3V3

GND                GND

SDA                D21

SCL                D22
------------------------------


------------------------------
LIGHT SENSOR CONNECTION:
------------------------------
LIGHT SENSOR       ESP32

VCC                3V3

GND                GND

DOUT               D15
------------------------------

"""

import gc
import ota
import time
import sensor
import machine
import network
import ntptime
import neopixel
import dotmatrix


################# SETTINGS #################

TIMEZONE_OFFSET_SECONDS = 19800
SCREEN_UPDATE_INTERVAL_MS = 500
NTP_TIME_SYNC_INTERVAL_MS = 900000
SCREEN_UPDATE_HARDWARE_TIMER_ID = 2
NTP_UPDATE_HARDWARE_TIMER_ID = 3
SPI_BUS_FOR_DOTMATRIX_DISPLAY = 2
SPI_BUS_COMMUNICATION_BAUDRATE = 10000000
SPI_BUS_CLK_PIN = 18
SPI_BUS_DOUT_PIN = 23
DOTMATRIX_CHIPSELECT_PIN = 5
DOTMATRIX_NUMBER_OF_MODULES = 4
DOTMATRIX_BRIGHTNESS_LEVEL_DARK = 0
DOTMATRIX_BRIGHTNESS_LEVEL_LIGHT = 15
LIGHT_SENSOR_DOUT_PIN = 15
ONBOARD_LED_BLINK_PIN = 2
NEOPIXEL_DATA_PIN = 33
NEOPIXEL_PIXEL_COUNT = 24
I2C_BUS_FOR_SENSOR = 0
I2C_SDA_PIN = 21
I2C_SCL_PIN = 22
I2C_BUS_CLK_FREQUENCY = 400000
LOOP_SLEEP_DELAY = 0.05
WDT_TIMEOUT_MS = 30000
DOT_MATRIX_STARTUP_MESSAGE = "TIME"
DOT_MATRIX_STARTUP_MESSAGE_DURATION = 2
DOT_MATRIX_STARTUP_BLANK_DURATION = 1

################# SETTINGS #################


gc.collect()
gc.enable()

ota = ota.ota()
led = machine.Pin(ONBOARD_LED_BLINK_PIN, machine.Pin.OUT)
spi = machine.SPI(SPI_BUS_FOR_DOTMATRIX_DISPLAY, baudrate=SPI_BUS_COMMUNICATION_BAUDRATE, polarity=1, phase=0, sck=machine.Pin(SPI_BUS_CLK_PIN), mosi=machine.Pin(SPI_BUS_DOUT_PIN))
cs = machine.Pin(DOTMATRIX_CHIPSELECT_PIN, machine.Pin.OUT)
display = dotmatrix.dotmatrix(spi, cs, DOTMATRIX_NUMBER_OF_MODULES)
neo = neopixel.NeoPixel(machine.Pin(NEOPIXEL_DATA_PIN), NEOPIXEL_PIXEL_COUNT)
dark = machine.Pin(LIGHT_SENSOR_DOUT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
i2c = machine.I2C(I2C_BUS_FOR_SENSOR, scl=machine.Pin(I2C_SCL_PIN), sda=machine.Pin(I2C_SDA_PIN), freq=I2C_BUS_CLK_FREQUENCY)
wdt = machine.WDT(timeout=WDT_TIMEOUT_MS)

screen_update_due = False
ntp_update_due = False
system_time_synchronised = False
multi_sensor_active = False
colorPointer = 0
aht20_temperature = 0
aht20_relative_humidity = 0
bmp280_temperature = 0
bmp280_pressure = 0

screen_timer = machine.Timer(SCREEN_UPDATE_HARDWARE_TIMER_ID)
ntp_timer = machine.Timer(NTP_UPDATE_HARDWARE_TIMER_ID)
display.brightness(DOTMATRIX_BRIGHTNESS_LEVEL_DARK)

try:
    aht20 = sensor.aht20(i2c)
    bmp280 = sensor.bmp280(i2c)
    multi_sensor_active = True
except OSError as e:
    multi_sensor_active = False    

ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
    ap_if.active(False)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

display.clear()
display.show()
display.text(DOT_MATRIX_STARTUP_MESSAGE)
display.show()
time.sleep(DOT_MATRIX_STARTUP_MESSAGE_DURATION)
display.clear()
display.show()
time.sleep(DOT_MATRIX_STARTUP_BLANK_DURATION)

if wlan.isconnected():
    try:
        ntptime.settime()
        system_time_synchronised = True
    except OSError as e:
        pass

def ntp_update(timer):
    global ntp_update_due
    ntp_update_due = True

def screen_update(timer):
    global screen_update_due
    screen_update_due = True

def get_local_time(offset_seconds):
    utc_seconds = time.time()
    local_seconds = utc_seconds + offset_seconds
    local_time_tuple = time.localtime(local_seconds)
    return local_time_tuple

def multi_sensor():
    global multi_sensor_active
    global aht20_temperature
    global aht20_relative_humidity
    global bmp280_temperature
    global bmp280_pressure
    if multi_sensor_active:
        try:
            aht20_temperature = % aht20.temperature
            aht20_relative_humidity = % aht20.relative_humidity
            bmp280_temperature = % bmp280.temperature
            bmp280_pressure = % bmp280.pressure
            print(aht20_temperature, bmp280_temperature, aht20_relative_humidity, bmp280_pressure)
        except OSError as e:
            print('sensor data collection failed')
            multi_sensor_active = False
    else:
        print('multi-sensor inactive')
        try:
            devices = i2c.scan()
            if len(devices) == 0:
                multi_sensor_active = False
            else:
                #print(f"Found {len(devices)} I2C devices:\n")
                #for device in devices:
                    #print(f"Decimal address: {device} | Hexadecimal address: {hex(device)}") 
                try:
                    aht20 = sensor.aht20(i2c)
                    bmp280 = sensor.bmp280(i2c)
                    multi_sensor_active = True
                except OSError as e:
                    multi_sensor_active = False
        except OSError as e:
            multi_sensor_active = False  

def rainbow():
    global colorPointer
    numpixel = neo.n
    colorPointer = colorPointer - numpixel + 1
    if colorPointer < 0:
        colorPointer = colorPointer + 1 + 255
    for i in range(numpixel):
        if colorPointer < 85:
            pixelColor = colorPointer & 255
            neo[i] = (pixelColor * 3, 255 - pixelColor * 3, 0)
        elif colorPointer < 170:
            pixelColor = colorPointer & 255 - 85
            neo[i] = (255 - pixelColor * 3, 0, pixelColor * 3)
        else:
            pixelColor = colorPointer & 255 - 170
            neo[i] = (0, pixelColor * 3, 255 - pixelColor * 3)
        colorPointer = colorPointer + 1
        if colorPointer > 255:
            colorPointer = 0
    neo.write()

screen_timer.init(mode=machine.Timer.PERIODIC, period=SCREEN_UPDATE_INTERVAL_MS, callback=screen_update)
ntp_timer.init(mode=machine.Timer.PERIODIC, period=NTP_TIME_SYNC_INTERVAL_MS, callback=ntp_update)

while True:
    if screen_update_due:
        if system_time_synchronised:
            led.value(not led.value())
            current_local_time = get_local_time(TIMEZONE_OFFSET_SECONDS)
            #print("Local time: {0}/{1}/{2} {3}:{4}:{5}".format(*current_local_time))
            current_time = "{:02d}:{:02d}:{:02d}".format(current_local_time[3], current_local_time[4], current_local_time[5])
            
            display.clear()
            display.matrix(str(current_time[0]), x_offset=1)
            display.matrix(str(current_time[1]), x_offset=8)
            if not led.value():
                display.matrix(str(current_time[2]), x_offset=15)
            display.matrix(str(current_time[3]), x_offset=18)
            display.matrix(str(current_time[4]), x_offset=25)
            display.show()
        else:
            display.clear()
            display.text("::::")
            display.show()
            if wlan.isconnected():
                try:
                    ntptime.settime()
                    display.clear()
                    display.fill(1)
                    display.show()
                    system_time_synchronised = True
                except OSError as e:
                    display.clear()
                    display.fill(0)
                    display.show()
            else:
                try:
                    ota.wificonnect()
                    if wlan.isconnected():
                        try:
                            ntptime.settime()
                            display.clear()
                            display.fill(1)
                            display.show()
                            system_time_synchronised = True
                        except OSError as e:
                            display.clear()
                            display.fill(0)
                            display.show()
                except OSError as e:
                    pass
        wdt.feed()
        multi_sensor()
        rainbow()
        screen_update_due = False
        
    if ntp_update_due:
        if wlan.isconnected():
            try:
                ntptime.settime()
                display.clear()
                display.fill(1)
                display.show()
                system_time_synchronised = True
            except OSError as e:
                display.clear()
                display.fill(0)
                display.show()
        else:
            try:
                ota.wificonnect()
                if wlan.isconnected():
                    try:
                        ntptime.settime()
                        display.clear()
                        display.fill(1)
                        display.show()
                        system_time_synchronised = True
                    except OSError as e:
                        display.clear()
                        display.fill(0)
                        display.show()
            except OSError as e:
                pass
        ntp_update_due = False

    if dark.value():
        display.brightness(DOTMATRIX_BRIGHTNESS_LEVEL_DARK)
    else:
        display.brightness(DOTMATRIX_BRIGHTNESS_LEVEL_LIGHT)
        
    time.sleep(LOOP_SLEEP_DELAY)
