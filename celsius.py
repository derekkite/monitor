#!/usr/bin/env python
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1, stopbits = 1, bytesize = 8,  parity='N', baudrate= 9600)
client.connect()

client.write_register(22,10)

