import bluetooth
import time
import os
from sense_hat import SenseHat

sense = SenseHat()

def getSenseHatData():
    temp = round(sense.get_temperature(), 1)

    return temp

def main():
    temp = getSenseHatData()
    addr = None

    if addr == None:
        try:
                input("Press the ENTER key to begin BlueTooth search")
        except SyntaxError:
                pass

        print("Searching...\n")

        nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True)

        if len(nearby_devices) > 0:
                print("Found %d devices!" % len(nearby_devices))
                sense.clear(0,255,0)
        else:
                print("No device was found, aborting!")
                sense.clear(255,0,0)
                exit(0)

        i = 0
        for addr, name in nearby_devices:
                print("%s. %s - %s\n" % (i, addr, name))
                i =+ 1

        device_num = input("Select your option for bluetooth device and press ENTER\n")
        addr, name = nearby_devices[device_num][0], nearby_devices[device_num][1]

        print("Pairing... %s.\n" % (addr))

    while True:
        state = bluetooth.lookup_name(addr, timeout=20)
        services = bluetooth.find_service(address=addr)

        if state == None and services == []:
                print("Could not pick up device")
        else:
                sense.show_message("Hi {}!, Current temp is {}*c".format(name, temp), scroll_speed=0.05)


#Execute main
main()
