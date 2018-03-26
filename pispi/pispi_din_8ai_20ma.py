#!/usr/bin/python

import time
import sys

import pispi_din_lib as PISPIDIN

print("Start pispi_din_8ai_20ma Test program")
print("Press CTRL C to exit")
print("")

'''
4 - 20 mA Input

Input Load Resistor = 150 Ohms
Voltage Reference for the MCP3208 = 3.30 VDC
20 mA AD Counts = ((0.02A * 150 Ohms) / 3.30VDC) * 4095 Full Scale Counts = 3723 AD Counts

!!NOTE!! Actual counts may vary between module to module and channel to channel

'''

if __name__ == '__main__':
    try:
        print("Read 8 channels 4-20 mA")

        adc = [0] * 8           # Raw AD Counts
        mA = [0] * 8            # mA Reading * Scaler
        strAN = [""] * 8        # Reading Scaled in string format for display

        port = 0                # SPI port = 0 or 1
        channel = 0             # Chip Select = CE1
        
        while True:

            for channel in range(0,8):        # Get mA Reading for Channels 1 thru 8
                adc[channel] = PISPIDIN.read_8ai_channel(PISPIDIN.CE1, port, channel)
                mA[channel] = PISPIDIN.update_8ai_ma(adc[channel])
                strAN[channel] = "%s" % (PISPIDIN.update_8ai_ma_reading(mA[channel]))
                print("Reading %d = %4d ADC, %s mA" % (channel+1, adc[channel], strAN[channel]))

            print("")
            
            time.sleep(1)
	            
    except KeyboardInterrupt:   # Press CTRL C to exit Program
        sys.exit(0)
            
