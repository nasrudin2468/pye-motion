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
import signal
import sys
import time


################################################################################
# Constants


################################################################################
# classes / structs
	
class mondata:
	def __init__(self):
		self.viewmode=0
		self.Lights="0"
		self.SC1TX="0"
		self.percAssist="000"
		self.AWD="0"
		self.C10="0"
		self.Voltage="000"
		self.Current="000"
		self.SC1RX="0"
		self.SC2="00"
		self.Speed="000"
		self.D1618="000"
		self.D1921="000"
		self.D2224="000"
		self.D2527="000"
		self.wsize="0"
		self.TX=""
		self.RX=""
		self.PLIST=["---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---","---"]
		
		
################################################################################
# Import external functions

import lib.message	as msg
import lib.config	as cfg
import lib.osys		as osy
import arg		as arg


#	TODO:
#	- TX RX Handlers
#	- TX RX Parsers
#	- Basic Logging
#	- Basic TX Construction mode (Parameter Reading P00 P59)
#	- PDCURSES?


################################################################################
# Functions

def signal_handler(signal, frame):
	sys.exit(0)


################################################################################
# beginn main

# init global vars
monitordata= mondata()
mondata.viewmode=0
signal.signal(signal.SIGINT, signal_handler)

cfg.read(cfg)

if len(sys.argv) == 1:
	print('No command line argument given. type pye-motion - help for valid arguments')
	
else:
	if (sys.argv[1] in ("-help")):
		print("not implemented.")
		exit()
		
	elif (sys.argv[1] in ( "-install")):
		print("not implemented.")
		exit()
		
	elif (sys.argv[1] in ( "-listen")):
		msg.serialOpen(cfg)
		arg.listen(monitordata)
	
	elif (sys.argv[1] in ( "-plisten")):	
		msg.serialOpen(cfg)
		arg.plisten(monitordata)
	
	elif (sys.argv[1] in ( "-pquery")):	
		msg.serialOpen(cfg)
		arg.pquery(monitordata)
		
	elif (sys.argv[1] in ( "-speedlimit")):
		print("not implemented.")
		exit()
		
	else: 
		print('Invalid command line argument given. type pye-motion - help for valid arguments')



# sample code for opening, sending, receiving and closing comport
#ser = serial.Serial(port_A, py pybaudrate=baud_A, timeout=1)  # open first serial port
#print ("Port opened: " + ser.portstr)       # check which port was really used
#ser.write("hello world".encode("utf-8"))      # write a string
#receive = ser.read(11)
#print (receive.decode("utf-8"))
#ser.close()             # close port