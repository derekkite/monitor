#!/usr/bin/env python
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1, stopbits = 1, bytesize = 8,  parity='N', baudrate= 9600)
client.connect()

var = 0

while var < 3:
#        rr = client.read_discrete_inputs(address=var, count=1, unit=1);
#        print rr.registers;

#        rr1 = client.read_coils(address=var, count=1, unit=1);
#        print rr1.registers;

        rr2 = client.read_holding_registers(address=var, count=1, unit=1);
        print rr2.registers;

        rr3 = client.read_input_registers(address=var, count=1, unit=1);
        print rr3.registers;

        var=var+1
