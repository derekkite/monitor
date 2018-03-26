import minimalmodbus
import time

minimalmodbus.BAUDRATE = 38400

# port name, slave address (in decimal)
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)

while True:
        # Register number, number of decimals, function code
        temperature = instrument.read_register(1, 2, 4)
        print temperature
        time.sleep(1)
