import bluetooth, time
from sense_hat import SenseHat

sense = SenseHat()
red = 255
addr = None

if addr == None:
    try:
        input("When you are ready to begin, press the Enter key to begin searching...")
    except SyntaxError:
        pass

    print("Searching for devices...")

    nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True)

    if len(nearby_devices) > 0:
        print("Found %d devices!" % len(nearby_devices))
    else:
        print("I was unable to locate any bluetooth devices")
        sense.clear(255,0,0)
        exit(0)

    i = 0
    for addr, name in nearby_devices:
        print("%s. %s - %s" % (i, addr, name))
        i =+ 1

    device_num = input("Option for bluetooth device ")

    # extract out the useful info on the desired device for use later
    addr, name = nearby_devices[device_num][0], nearby_devices[device_num][1]

print("The script will now scan for the device %s." % (addr))

while True:
    # Try to gather information from the desired device.
    # We're using two different metrics (readable name and data services)
    # to reduce false negatives.
    state = bluetooth.lookup_name(addr, timeout=20)
    services = bluetooth.find_service(address=addr)
    # Flip the LED pin on or off depending on whether the device is nearby
    if state == None and services == []:
        print("No device detected in range...")
    else:
        print("Device detected!")
    # Arbitrary wait time
    time.sleep(10)
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM, bluez.btsocket())
