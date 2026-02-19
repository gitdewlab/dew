import ota
import machine
import network

# github repository access and files to update
ota = ota.ota(
  user="gitdewlab",
  repo="dew",
  branch="main",
  working_dir="dew",
  files = ["boot.py", "sensor.py", "dotmatrix.py", "main.py"]
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
