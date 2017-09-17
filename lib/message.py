################################################################################
#
# pye-motion - an open source diagnostic toolkit for BH E-bike systems
# This code is released under MIT license.
#
# Copyright (c) 2017 nasrudin2468
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################


################################################################################
# Import Libraries

import array
import binascii
import configparser
import datetime
import io
import logging
import os
import serial
import sys
import time


################################################################################
# Constants


################################################################################
# classes / structs


################################################################################
# Import external functions


################################################################################
# Functions

# function:	addchecksum(message)
# 	calculate and add checksum value to a message
# 	Input:	type class smessage
#	Output:	modifies input variable
def addchecksum(message):
	chkecb=0
	for i in range (message.slength-4):
		chkecb ^= message.rawbuffer[i+1]
	ecbhigh = (chkecb >> 4)
	ecblow = chkecb - (16 * ecbhigh)
	#print(ecbhigh, ecblow)
	message.rawbuffer[message.slength-3] = MASCII[ecbhigh]
	message.rawbuffer[message.slength-2] = MASCII[ecblow]
	message.rawbuffer[message.slength-1] = 13
	message.rawbuffer[message.slength-0] = 0
	return

# addframe(message)
# 	adds message frame to given message and transfers it into rawbuffer of 
# 	given variable
# 	Input:	type class smessage
#	Output:	modifies input variable	
def addframe(message):
	#calc size of payload
	message.slength = len(message.payload) + 6
	
	if message.slength <= 8:
		print("bad message.")
		return
	
	#convert payload, add header and footer
	message.rawbuffer[0] = 64
	message.rawbuffer[1] = 48
	message.rawbuffer[2] = 49
	
	for i in range(message.slength-6):
		message.rawbuffer[i+3]=ord(message.payload[i])
	return

# parse(message, bhdata)
# parses a raw message string and extracts information into given variable
# 	Input:	raw message string
# 	Output:	type class smessage	
def parse(message, bhdata):
	parserindex = 0

	# get message type
	bhdata.mtype = message.payload[0]
	
	# P-Type messages
	if (bhdata.mtype == "P"):
		bhdata.pnumber = message.payload[1:3]
		print ("bhdata.mtype: ", bhdata.mtype)
		print ("bhdata.pnumber: ", bhdata.pnumber)
		if message.slength <= 9:
			#no further data, quit parsing
			return
		#calculate length and get  p-value
		pdatalength = message.slength-9
		bhdata.pvalue=message.payload[3:(6+pdatalength)]
		print ("bhdata.pvalue: ", bhdata.pvalue)
		
	elif (bhdata.mtype == "D"):
		bhdata.RX		= message.payload[0:24]
		bhdata.Voltage 	= message.payload[1:4]
		bhdata.Current 	= message.payload[4:7]
		bhdata.SC1RX 	= message.payload[7:8]
		bhdata.SC2		= message.payload[8:10]
		bhdata.Speed 	= message.payload[10:13]
		bhdata.D1618	= message.payload[13:16]
		bhdata.D1921	= message.payload[16:19]
		bhdata.D2224	= message.payload[19:22]
		bhdata.D2527	= message.payload[22:25]
		return
		
	elif (bhdata.mtype == "C"):
		bhdata.TX		= message.payload[0:10]
		bhdata.Lights 	= message.payload[1]
		bhdata.SC1TX 	= message.payload[2]
		bhdata.percAssist = message.payload[3:5]
		bhdata.AWD		= message.payload[6]
		bhdata.C10		= message.payload[7]
		return

# serialSend(message, device)
# send a given message via USB-serial adapter to a given device / bus direction
# 	Input:	raw message string, device / bus direction
# 	Output:	- 	
def serialSend(message, device):
	
	#send
	device.write(message.rawbuffer)
	
	return

# serialOpen(configarray)
# Open Serial Adapters
# 	Input:
# 	Output:
def serialOpen(cfg):
	if (cfg.hwconfig in ("usb-serial-a", "usb-serial-full")):
		print()
		print('Parameters Serial-A (Controller):')
		print(' port = '+ cfg.port_A)
		print(' baudrate = '+ cfg.baud_A)
		print(' busconfig = '+cfg.bitcount_A+cfg.parity_A+cfg.stopbit_A)
		print()
		print ("Open Serial-A adapter...")
		cfg.bhController = serial.Serial(cfg.port_A, baudrate=cfg.baud_A, timeout=1)  # open first serial port
		print ("Success! Port: " + cfg.bhController.portstr)


	if (cfg.hwconfig in ("usb-serial-b", "usb-serial-full")):  
		print()
		print('Parameters Serial-B (Display):')
		print(' port = '+ cfg.port_B)
		print(' baudrate = '+ cfg.baud_B)
		print(' busconfig = '+cfg.bitcount_B+cfg.parity_B+cfg.stopbit_B)
		print()
		cfg.bhDisplay = serial.Serial(cfg.port_B, baudrate=cfg.baud_B, timeout=1)  # open second serial port
		print ("Success! Port: " + cfg.bhDisplay.portstr)
	
	return


# serialClose(configarray)
# Close Serial Adapters
# 	Input:
# 	Output:
def serialClose(cfg):
	if (cfg.hwconfig in ("usb-serial-a", "usb-serial-full")):
		cfg.bhController.close()
	
	if (cfg.hwconfig in ("usb-serial-b", "usb-serial-full")):  	
		cfg.bhDisplay.close()
	
	return

# serialReceive(message, device)
# Receive Data via USB-serial adapter from a  given device / bus direction via USB-serial adapter
# 	Input:	raw message string, device / bus direction
# 	Output:	writes into given raw message string 
def serialReceive(message, device):
	while True:
		temp = 0
		temp = int.from_bytes(device.read(),byteorder='little')
		
		if  temp != 0:
			# something was transmitted. write into objbuffer
			message.rawbuffer[message.slength] = temp
			message.slength+=1
			
			
		if temp == 0:
			# nothing in Fifo, wait for next func call
			return
			
		if temp == 13:
			# decode, set readbit, finish
			message.rawbuffer[message.slength]=0
			
			# check message for basic validity
			#if message.slength <= 8:
				#print ("bad message.")
				#return
			
			i=0
			
			#extract header and payload
			for i in range(3):
				message.header+=chr(message.rawbuffer[i])
			
			for i in range((message.slength)-6):
				message.payload+=chr(message.rawbuffer[i+3])
			
			#extract ecb	
			for j in range(16):
				if MASCII[j] == message.rawbuffer[message.slength-3]:
					message.ecb = 16*j
					#print (message.ecb)
			for j in range(16):
				if MASCII[j] == message.rawbuffer[message.slength-2]:
					message.ecb += j
					#print (message.ecb)
				
			#calculate ecb
			chkecb=0
			for i in range (message.slength-4):
				chkecb ^= message.rawbuffer[i+1]
			#message.ecb = 16*message.rawbuffer[message.slength-3]
			#message.ecb = message.rawbuffer[message.slength-2]
			#message.ecb=binascii.b2a_hex(ecstr)
			#message.ecb=binascii.hexlify(b, ecstr)
				
			message.readable=1
			#print("Rawbuffer: ", message.rawbuffer)
			#print("Bufferindex: ", message.slength)
			#print("Header: ", message.header)
			#print("Payload: ", message.payload)
			#print("ECB Buffer: ", message.ecb)
			#print("ECB calculated: ", chkecb)
			return
	return
	
	
		