from parser import parse_devices_from_spreadsheet
from plc_io import PylogixPLC
import time
import itertools
import sys

def main():
    plc = PylogixPLC('192.168.3.20')  # Replace with your PLC IP
    devices = parse_devices_from_spreadsheet("devices.xlsm", plc)  # <-- updated here
    valves = devices["valves"]

    print(f"Loaded {len(valves)} valves. Starting simulation...\n")

    spinner = itertools.cycle(['|', '/', '-', '\\'])

    tick = 0
    while True:
        for valve in valves:
            valve.simulate_behavior()
            #print("running simulation")
        if tick % 5 == 0:
            sys.stdout.write(f"\rRunning simulation... {next(spinner)}")
            sys.stdout.flush()

        time.sleep(0.1)
        tick += 1

if __name__ == "__main__":
    main()