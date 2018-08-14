import bluetooth
import time
import os
from sense_hat import SenseHat

sense = SenseHat()
addr = None
temp = round(sense.get_temperature(), 1)

if addr == None:
    try:
        input("When you are ready to begin, press the Enter key to begin searching...")
    except SyntaxError:
        pass

    print("Searching for devices...")

    nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True)

    if len(nearby_devices) > 0:
        print("Found %d devices!" % len(nearby_devices))
        sense.clear(0,255,0)
    else:
        print("I was unable to locate any bluetooth devices")
        sense.clear(255,0,0)
        exit(0)

    i = 0
    for addr, name in nearby_devices:
        print("%s. %s - %s" % (i, addr, name))
        i =+ 1

    device_num = input("Option for bluetooth device ")
    addr, name = nearby_devices[device_num][0], nearby_devices[device_num][1]

print("The script will now scan for the device %s." % (addr))

while True:
    state = bluetooth.lookup_name(addr, timeout=20)
    services = bluetooth.find_service(address=addr)

    if state == None and services == []:
        print("No device detected in range...")
    else:
        sense.show_message("Hi {}!, Current temp is {}*c".format(name, temp), scroll_speed=0.05)


