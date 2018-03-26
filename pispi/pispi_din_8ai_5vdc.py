#!/usr/bin/python

import time
import sys

import pispi_din_lib as PISPIDIN

print("Start pispi_din_8ai_5vdc Test program")
print("Press CTRL C to exit")
print("")

'''
0 - 5 VDC Input

Input Voltage Divider = 56K / 56K
Input Full Scale VDC = 6.6 VDC
Voltage Reference for the MCP3208 = 3.30 VDC
6.6VDC AD Counts = (3.3 VDC / 3.30VDC) * 4095 Full Scale Counts = 4095 AD Counts

!!NOTE!! Actual counts may vary between module to module and channel to channel

'''

if __name__ == '__main__':
    try:
        print("Read 8 channels 4-20 mA")

        adc = [0] * 8           # Raw AD Counts
        vdc = [0] * 8           # VDC Reading * Scaler
        strAN = [""] * 8        # Reading Scaled in string format for display

        port = 1                # SPI port = 0 or 1
                                # Chip Select = CE1
        
        while True:

            for channel in range(0,8):        # Get mA Reading for Channels 1 thru 8
                adc[channel] = PISPIDIN.read_8ai_channel(PISPIDIN.CE1, port, channel)
                vdc[channel] = PISPIDIN.update_8ai_5vdc(adc[channel])
                strAN[channel] = "%s" % (PISPIDIN.update_8ai_5vdc_reading(vdc[channel]))
                print("Reading %d = %4d ADC, %s VDC" % (channel+1, adc[channel], strAN[channel]))

            print("")
            
            time.sleep(1)
	            
    except KeyboardInterrupt:   # Press CTRL C to exit Program
        sys.exit(0)
            
