import machine
import sensor
import time


i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)

aht20 = sensor.aht20(i2c)
bmp280 = sensor.bmp280(i2c)


def scan_i2c_bus():
    print("\nScanning I2C addresses...")
    devices = i2c.scan()

    if len(devices) == 0:
        print("No I2C devices found!")
    else:
        print(f"Found {len(devices)} I2C devices:\n")
        for device in devices:
            print(f"Decimal address: {device} | Hexadecimal address: {hex(device)}")       
            
            
while True:
    scan_i2c_bus()
    print("\naht20 Temperature: %0.2f C" % aht20.temperature)
    print("aht20 Humidity: %0.2f %%" % aht20.relative_humidity)
    print("\nbmp280 Temperature: %0.2f C" % bmp280.temperature)
    print("bmp280 Pressure: %0.2f hPa" % bmp280.pressure)
    time.sleep(5)

"""
if __name__ == '__main__':
    scan_i2c_bus()
"""
