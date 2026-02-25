import ota
import machine
import network

# downloading from github repository to update device files
ota = ota.ota(
  user="gitdewlab",
  repo="dew",
  branch="main",
  working_dir="dew",
  files = ["boot.py", "main.py", "dotmatrix.py", "sensor.py"]
)

try:
    ota.wificonnect()
    if ota.update():
        print("rebooting...")
        machine.reset()
    else:
        # deactivate micropython ap
        ap = network.WLAN(network.AP_IF)
        if ap.active():
            ap.active(False)
except OSError as e:
    print(f"error: {e}")
