import bluetooth
import time
import os
from sense_hat import SenseHat

sense = SenseHat()

# Function to record current temp rounded to 1 decimal
def getSenseHatData():
    temp = round(sense.get_temperature(), 1)

    return temp

# Main function will search for a bluetooth device and display the current temp on the SenseHat
def main():
    temp = getSenseHatData()
    bt_address = None

    if bt_address == None:
        try:
                input("Press the ENTER key to begin BlueTooth search")
        except SyntaxError:
                pass

        print("Searching...\n")

        bt_devices = bluetooth.discover_devices(duration=5, lookup_names=True)

        if len(bt_devices) > 0:
                print("Found %d devices!" % len(bt_devices))
                sense.clear(0,255,0)
        else:
                print("No device was found, aborting!")
                sense.clear(255,0,0)
                exit(0)

        i = 0
        for bt_address, name in bt_devices:
                print("%s. %s - %s\n" % (i, bt_address, name))
                i =+ 1

        device_num = input("Select your option for bluetooth device and press ENTER\n")
        bt_address, name = bt_devices[device_num][0], bt_devices[device_num][1]

        print("Pairing... %s.\n" % (bt_address))

    while True:
        bt_state = bluetooth.lookup_name(bt_address, timeout=20)
        bt_services = bluetooth.find_service(address=bt_address)

        if bt_state == None and bt_services == []:
                print("Could not pick up device")
        else:
                sense.show_message("Hi {}!, Current temp is {}*c".format(name, temp), scroll_speed=0.05)


#Execute main program
main()
