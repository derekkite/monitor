#!/usr/bin/python

'''
PI-SPI-DIN Library  VP Process In c. / Widgetlords Electronics

Release Version 1.0
Release Date:   December 18, 2017

Modules Supported:
PI-SPI-DIN-8AI-20mA  8 Channel Analog Input 4 - 20 mA Module
PI-SPI-DIN-4AO       4 Channel Analog Output 4-20 mA Moudle
PI-SPI-DIN-8DI       8 Channle Digital Input Module
PI-SPI-DIN-4KO       4 Channel Relay Output Module

'''
  
import RPi.GPIO as GPIO
import time
import math
import sys
import smbus
import spidev
import serial

GPIO.setmode(GPIO.BCM)  # Use RPi GPIO numbers
GPIO.setwarnings(False) # disable warnings

# open SMBus port for I2C communication
din4ao = smbus.SMBus(1)

# spidev normally installed with RPi 3 distro's
# Make Sure SPI is enabled in RPi preferences
spi = spidev.SpiDev()   
                        
# Chip select definitions for PI-SPI-DIN series modules
# PI-SPI-DIN Expansion Modules Chip Selects
CE1 = 7
CE0 = 8
CE2 = 24
CE3 = 23
CE4 = 18

GPIO.setup(CE1,GPIO.OUT)            # PI-SPI-DIN Series Chip Select 1 - Active Low
GPIO.output(CE1,1)           
GPIO.setup(CE0,GPIO.OUT)            # PI-SPI-DIN Series Chip Select 0 - Active Low
GPIO.output(CE0,1)           
GPIO.setup(CE2,GPIO.OUT)            # PI-SPI-DIN Series Chip Select 2 - Active Low
GPIO.output(CE2,1)           
GPIO.setup(CE3,GPIO.OUT)            # PI-SPI-DIN Series Chip Select 3 - Active Low
GPIO.output(CE3,1)           
GPIO.setup(CE4,GPIO.OUT)            # PI-SPI-DIN Series Chip Select 4 - Active Low
GPIO.output(CE4,1)           

def close_spi():
        spi.close()
        return

#   PI-SPI-DIN-8AI_20MA Module
#   8 Channel 4-20 mA Input

mASpan = 2000                   # mA Full Scale = 20.00 mA
VDC_5_Span = 660                # VDC Full Scale = 6.6 VDC
VDC_10_Span = 1000              # VDC Full Scale = 6.6 VDC

Scaler = 100                    # Scaler factor - all reading are * 100

mASpanAdc = 3723                # AD Counts to equal 20 mA
VDC_5_SpanAdc = 4095            # AD Counts to equal 6.6 VDC
VDC_10_SpanAdc = 3685           # AD Counts to equal 10 VDC

#   !!NOTE!! Actual counts may vary between module to module and channel to channel

def buildReadCommand(channel):  # Build MCP3208 ADC Command and Channel No
        input = 0x0600 | (channel << 6)
        buf_0 = (input >> 8) & 0xff
        buf_1 = input & 0xff
        buf_2 = 0;
        return [buf_0, buf_1, buf_2] # 3 bytes to be sent to MCP3208   

def read_8ai_channel(chip_select, port, channel):           # SPI Write and Read transfer for channel no.
                                # Chip Select for Analog Input Module is GPIO-7 (CE_1)

        spi.open(0, port)           # Open SPI Channel 1 Chip Select is GPIO-7 (CE_1)

        if((channel > 7) or (channel < 0)):
                return -1

        GPIO.output(chip_select, 0)
        adc = spi.xfer(buildReadCommand(channel)) # Chip Select handled automatically by spi.xfer
        GPIO.output(chip_select, 1)
        spi.close()
        return processAdcValue(adc)   

def processAdcValue(result):    # Process two bytes data for 12 bit resolution
        byte2 = (result[1] & 0x0f)
        return (byte2 << 8) | result[2]

def update_8ai_ma(adc):
        return (adc * mASpan) / mASpanAdc

def update_8ai_ma_reading(mA):
        return "%5.2f" % (((float)(mA))/Scaler)
    
def update_8ai_5vdc(adc):
        return (adc * VDC_5_Span) / VDC_5_SpanAdc

def update_8ai_5vdc_reading(vdc):
        return "%5.2f" % (((float)(vdc))/Scaler)

def update_8ai_10vdc(adc):
        return (adc * VDC_10_Span) / VDC_10_SpanAdc

def update_8ai_10vdc_reading(vdc):
        return "%5.2f" % (((float)(vdc))/Scaler)

def update_8ai_temp_reading(temp):
        return "%5.2f" % ((float)(temp))

def update_8ai_temperature(channel_adc):
        if (channel_adc > 0):
                R_LOAD =	10000.0 # Load Resistor Value
                R_ROOM_TEMP =	10000.0 # for 25 Deg C
                T_BETA =	3380.0  # Beta Value of Thermistor being Used
                T_KELVIN =      273.15  # Kelvin Degree Offset
                T_AD_COUNTS =	4095.0	# MCP3208 is 12 bit ADC
                ROOM_TEMP_NOM =	25.0    # Nominal Room Temperature for Beat Value
                r_reading = (channel_adc * R_LOAD ) / (T_AD_COUNTS - channel_adc) 
                t25 = T_KELVIN + 25.0   # 25 Deg C in Kelvin
                # Steinhart Equation
                inv_T = 1/t25 + 1/T_BETA * math.log(r_reading/R_ROOM_TEMP)
                T = (1/inv_T - T_KELVIN)
                return T                # Return Temperature in Deg C
        else:
                return 0
 

#   PI-SPI-DIN-8DI Module
#   8 Channel Isolated Digital Inputs

#   Initialize PI-SPI-DIN-8DI Digital Input Module
def initialize_8di(chip_select, port):
        addr = 0x40 
        buf = [0] * 8
        buf[0] = addr                   # Write Command
        buf[1] = 0x00                   # Set Address IODIR
        buf[2] = 0xff                   # Set IODIR to Inputs
        buf[3] = 0xff                   # Set IPOL Polarity to Invert
        buf[4] = 0x00                   # Set GPINTEN
        buf[5] = 0x00                   # Set DEFVAL
        buf[6] = 0x00                   # Set INTCON
        buf[7] = 0x08                   # Set IOCON to enable Hardware Addressing
        GPIO.output(chip_select,0)      # Set Chip Select 8DI LOW
        spi.open(0,port)                # open SPI channel 0 CS 0
        spi.writebytes(buf)             # write command
        GPIO.output(chip_select,1)      # Set Ship Select 2AO HIGH
        spi.close
        return

#   Read all 8 inputs at once, 8 bits of data in 1 byte where DI1 = bit 0, DI8 = bit 7
def read_8di(chip_select, port, address):
        addr = 0x41 + (address<<1)
        buf = [0] * 2
        buf[0] = addr                   # Read Command
        buf[1] = 0x09                   # Register Address        
        GPIO.output(chip_select,0)      # Set Chip Select 8DI LOW
        spi.open(0,port)
        spi.writebytes(buf)             # write command
        data = spi.readbytes(2)
        GPIO.output(chip_select,1)      # Set Chip Select 8DI HIGH
        spi.close                       # close SPI 
        return data[0]

#   Update Single Digital Input Reading 
def update_8di_single(dig_io, channel):
        if(dig_io&channel):
                return 1
        else:
                return 0

        

#   PI-SPI-DIN-4KO Module
#   4 Channel Relay Contact Output

#   Initialzide PI-SPI-DIN-4KO module
def initialize_4ko(chip_select, port):
        addr = 0x40 
        buf = [0] * 8
        buf[0] = addr               # Write Command
        buf[1] = 0x00               # Set Address IODIR
        buf[2] = 0x00               # Set IODIR to Outputs
        buf[3] = 0xff               # Set IPOL Polarity to Invert
        buf[4] = 0x00               # Set GPINTEN
        buf[5] = 0x00               # Set DEFVAL
        buf[6] = 0x00               # Set INTCON
        buf[7] = 0x08               # Set IOCON to enable Hardware Addressing

        GPIO.output(chip_select,0)      # Set Chip Select 8DI LOW
        spi.open(0,port)                # open SPI channel 0 CS 0
        spi.writebytes(buf)             # write command
        GPIO.output(chip_select,1)      # Set Ship Select 2AO HIGH
        spi.close
        return

#   Write 4 relays all at once
def write_4ko(chip_select, port, address, relay_status):
        addr = 0x40 + (address<<1)
        buf = [0] * 3
        buf[0] = addr               # Read Command
        buf[1] = 0x09               # Register Address 
        buf[2] = relay_status       # Relay Status
        GPIO.output(chip_select,0)     
        spi.open(0,port)
        spi.writebytes(buf) 
        GPIO.output(chip_select,1)       
        spi.close               
        return 

#   Set status of relay based on relay_status byte and relay number
def update_4ko_relay_status(relay_status, relay, status):

        if (status):
                relay_status |= relay           # Set Relay ON
        else:
                relay_status &= ~relay          # Set Relay OFF          

        return  relay_status 


#   PI-SPI-DIN-4AO Module
#   4 Channel 4-20mA (0-20mA) Output

#   4 mA  = 800  DAC Counts
#   8 mA  = 1600 DAC Counts
#   12 mA = 2400 DAC Counts
#   16 mA = 3200 DAC Counts
#   20 mA = 4000 DAC Counts

#   !!NOTE!! Actual counts may vary between module to module and channel to channel

#   Write all 4 DAC channels at the same time
def write_din_4ao(address, dac1, dac2, dac3, dac4):
        data = [0] * 12

        data0 = 0x40;		        # Multi-Write Command Channel 0
        data[0] = 0x80;		        # Set Internal Ref Voltage
        data[0] |= (dac1>>8)&0x0f;	# Add dac1 high byte
        data[1] = dac1&0x00ff;	        # dac1 low byte

        data[2] = 0x42;		        # Multi-Write Command Channel 1
        data[3] = 0x80;		        # Set Internal Ref Voltage
        data[3] |= (dac2>>8)&0x0f;	# Add dac2 high byte
        data[4] = dac2&0x00ff;	        # dac2 low byte

        data[5] = 0x44;		        # Multi-Write Command Channel 2
        data[6] = 0x80;		        # Set Internal Ref Voltage
        data[6] |= (dac3>>8)&0x0f;	# Add dac3 high byte
        data[7] = dac3&0x00ff;	        # dac3 low byte

        data[8] = 0x46;		        # Multi-Write Command Channel 3
        data[9] = 0x80;		        # Set Internal Ref Voltage
        data[9] |= (dac4>>8)&0x0f;	# Add dac4 high byte
        data[10] = dac4&0x00ff;	        # dac4 low byte
        data[11] = 0x00;		# dummy byte

        din4ao.write_i2c_block_data(address,data0,data)
        return

#  Write individual DAC channels
def write_din_4ao_single(address, channel, dac_counts):
        data = [0] * 3

        if (channel > 3):               # valid addresses are 0,1,2 and 3
                return

        if (channel == 0):              # get command address value          
                data0 = 0x40
        elif (channel == 1):
                data0 = 0x42
        elif (channel == 2):
                data0 = 0x44
        elif (channel == 3):
                data0 = 0x46
                
        data[0] = 0x80;		        # Set Internal Ref Voltage
        data[0] |= (dac_counts>>8)&0x0f;        # Add dac_counts high byte
        data[1] = dac_counts&0x00ff;	        # dac_counts low byte
        data[2] = 0;	                # dummy byte

        din4ao.write_i2c_block_data(address,data0,data)
        return

