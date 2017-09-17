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
#Import external functions

import lib.message	as msg
import lib.config	as cfg
import lib.osys		as osy
import lib.arg		as arg


#	TODO:
#	- TX RX Handlers
#	- TX RX Parsers
#	- Basic Logging
#	- Basic TX Construction mode (Parameter Reading P00 P59)
#	- PDCURSES?

################################################################################
# classes / structs

MASCII = array.array('B',[ 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70 ])
PNAME = [ 	"P00", "P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P11", "P12", "P13", "P14", "P15", "P16", "P17", "P18", "P19", "P20", "P21", "P22", "P23", "P24", "P25", "P26", "P27", "P28", "P29", "P30", "P31", "P32", "P33", "P34", "P35", "P36", "P37", "P38", "P39", "P40", "P41", "P42", "P43", "P44", "P45", "P46", "P47", "P48", "P49", "P50", "P51", "P52", "P53", "P54", "P55", "P56", "P57", "P58", "P59", "P60", "P61", "P62", "P63", "P64", "P65", "P66", "P67", "P68", "P69", "P70", "P71", "P72", "P73", "P74", "P75", "P76", "P77", "P78", "P79", "P80", "P81", "P82", "P83", "P84", "P85", "P86", "P87", "P88", "P89", "P90", "P91", "P92", "P93", "P94", "P95", "P96", "P97", "P98", "P99"]

class smessage:
	def __init__(self):
		self.rawbuffer=array.array('B',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		#self.rawbuffer=array.array('B')
		self.slength=0
		self.readable=0
		self.header=""
		self.payload=""
		self.ecb=0
		
class bhdata:
	def __init__(self):
		self.mtype=""
		self.pnumber=""
		self.pvalue=""
		
	
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
# Constants

WAITFORREAD_MS = 100
MAIN = 1

################################################################################
# Functions



################################################################################
# beginn main

# init global vars
data_A = smessage()
bhdata_A = bhdata()
monitordata= mondata()
mondata.viewmode=0

cfg.read(cfg)

if len(sys.argv) == 1:
	print(' No command line argument given. type pye-motion - help for valid arguments')
	
else:
	if (sys.argv[1] in ( "-help")):
		print("not implemented.")
		return
		
	elif (sys.argv[1] in ( "-install")):
		print("not implemented.")
		return
		
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
		return
		
	else: 
		print('Invalid command line argument given. type pye-motion - help for valid arguments')



# sample code for opening, sending, receiving and closing comport
#ser = serial.Serial(port_A, py pybaudrate=baud_A, timeout=1)  # open first serial port
#print ("Port opened: " + ser.portstr)       # check which port was really used
#ser.write("hello world".encode("utf-8"))      # write a string
#receive = ser.read(11)
#print (receive.decode("utf-8"))
#ser.close()             # close port