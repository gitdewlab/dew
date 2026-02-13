import gc
import time
import machine
import network
import ntptime
import dotmatrix

gc.collect()
gc.enable()

TIMEZONE_OFFSET_SECONDS = 19800

led = machine.Pin(2, machine.Pin.OUT)

spi = machine.SPI(2, baudrate=10000000, polarity=1, phase=0, sck=machine.Pin(18), mosi=machine.Pin(23))
cs = machine.Pin(5, machine.Pin.OUT)
display = dotmatrix.dotmatrix(spi, cs, 4)

display.brightness(3)
display.clear()
display.show()

display.text("TIME")
display.show()

time.sleep(2)

display.clear()
display.show()

time.sleep(1)

screen_update_timer_id = 2
ntp_update_timer_id = 3

screen_update_due = False
ntp_update_due = False
time_valid = False

screen_timer = machine.Timer(screen_update_timer_id)
ntp_timer = machine.Timer(ntp_update_timer_id)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if wlan.isconnected():
    try:
        ntptime.settime()
        time_valid = True
    except OSError as e:
        pass

def ntp_update(timer):
    global ntp_update_due
    ntp_update_due = True

def screen_update(timer):
    global screen_update_due
    screen_update_due = True
    
screen_timer.init(mode=machine.Timer.PERIODIC, period=500, callback=screen_update)
ntp_timer.init(mode=machine.Timer.PERIODIC, period=10000, callback=ntp_update)

def get_local_time(offset_seconds):
    utc_seconds = time.time()
    local_seconds = utc_seconds + offset_seconds
    local_time_tuple = time.localtime(local_seconds)
    return local_time_tuple

while True:
    if screen_update_due:
        if time_valid: # ---------
            led.value(not led.value())
            current_local_time = get_local_time(TIMEZONE_OFFSET_SECONDS)
            print("Local time tuple:", current_local_time)
            # You can format the tuple into a readable string if needed
            print("Local time: {0}/{1}/{2} {3}:{4}:{5}".format(*current_local_time))
            display.clear()
            #display.text("TIME")
            display.matrix("8", x_offset=1)
            display.matrix("8", x_offset=8)
            display.matrix(":", x_offset=15)
            display.matrix("8", x_offset=19)
            display.matrix("8", x_offset=26)
            display.show()
        else:
            display.clear()
            display.text("::::")
            display.show()            
        screen_update_due = False
        
    if ntp_update_due:
        if wlan.isconnected():
            try:
                ntptime.settime()
                display.clear()
                display.text("SYNC")
                display.show()
                time_valid = True
            except OSError as e:
                display.clear()
                display.text("::::")
                display.show()
                time_valid = False
        ntp_update_due = False
         
    time.sleep(0.05)
