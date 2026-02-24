"""

24 BIT NEOPIXEL PATTERN CLOCK

NETWORK TIME SYNCHRONISED


NEOPIXEL RING CONNECTION:

NEOPIXEL           ESP32

VCC                5V

GND                GND

DIN                D13


"""


import time
import machine
import neopixel


################# SETTINGS #################

NEOPIXEL_DATA_PIN = 13
NEOPIXEL_PIXEL_COUNT = 24
NEOPIXEL_PATTERN_DELAY_MS = 60

################# SETTINGS #################


np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_DATA_PIN, machine.PIN.OUT), NEOPIXEL_PIXEL_COUNT)

def pattern(np):
    n = np.n


    
    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 128, 0)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

        # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (128, 0, 0)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

        # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 128, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (128, 128, 0)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

        # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (128, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()
        time.sleep_ms(35)

        # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (0, val, 0)
        np.write()
        time.sleep_ms(35)

        # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (0, 0, val)
        np.write()
        time.sleep_ms(35)

        # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, val, 0)
        np.write()
        time.sleep_ms(35)

        # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (0, val, val)
        np.write()
        time.sleep_ms(35)

        # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, val)
        np.write()
        time.sleep_ms(35)

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()



while True:
  pattern(np)
