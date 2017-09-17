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

WAITFORREAD_MS = 100
MASCII = array.array('B',[ 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70 ])
PNAME = ["P00", "P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P11", "P12", "P13", "P14", "P15", "P16", "P17", "P18", "P19", "P20", "P21", "P22", "P23", "P24", "P25", "P26", "P27", "P28", "P29", "P30", "P31", "P32", "P33", "P34", "P35", "P36", "P37", "P38", "P39", "P40", "P41", "P42", "P43", "P44", "P45", "P46", "P47", "P48", "P49", "P50", "P51", "P52", "P53", "P54", "P55", "P56", "P57", "P58", "P59", "P60", "P61", "P62", "P63", "P64", "P65", "P66", "P67", "P68", "P69", "P70", "P71", "P72", "P73", "P74", "P75", "P76", "P77", "P78", "P79", "P80", "P81", "P82", "P83", "P84", "P85", "P86", "P87", "P88", "P89", "P90", "P91", "P92", "P93", "P94", "P95", "P96", "P97", "P98", "P99"]


################################################################################
# classes / structs

#MASCII = array.array('B',[ 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70 ])
#PNAME = ["P00", "P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P11", "P12", "P13", "P14", "P15", "P16", "P17", "P18", "P19", "P20", "P21", "P22", "P23", "P24", "P25", "P26", "P27", "P28", "P29", "P30", "P31", "P32", "P33", "P34", "P35", "P36", "P37", "P38", "P39", "P40", "P41", "P42", "P43", "P44", "P45", "P46", "P47", "P48", "P49", "P50", "P51", "P52", "P53", "P54", "P55", "P56", "P57", "P58", "P59", "P60", "P61", "P62", "P63", "P64", "P65", "P66", "P67", "P68", "P69", "P70", "P71", "P72", "P73", "P74", "P75", "P76", "P77", "P78", "P79", "P80", "P81", "P82", "P83", "P84", "P85", "P86", "P87", "P88", "P89", "P90", "P91", "P92", "P93", "P94", "P95", "P96", "P97", "P98", "P99"]

class smessage:
	def __init__(self):
		self.rawbuffer=array.array('B',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		#self.rawbuffer=array.array('B')
		self.slength=0
		self.readable=0
		self.header=""
		self.payload=""
		self.ecb=0


################################################################################
# Import external functions

import lib.message	as msg
import lib.config	as cfg
import lib.osys	as osy


################################################################################
# Functions

# function:	help()
# 	
# 	Input:	-
#	Output:	-
def help():
	print("Usage:")
	print()
	print("pye-motion [arg1] [arg2]") 
	print("	Starting pye-motion without any gives you the program version. It") 
	print("	also checks for python lib depencies and suggests using -help to get") 
	print("	additional information about usage")
	print()
	print("pye-motion -help")
	print("	lists all available command arguments and how to use them")
	print()		
	print("pye-motion -install")
	print("	installs lib dependencies via python pip")
	print()		
	print("pye-motion -listen")
	print("	Passive listen modus. shows transfered raw messages as well as a")
	print("	table of all scaled livemodus values")
	print()
	print("pye-motion -plisten")
	print("	read all parameter values from memory and show them in a table")
	print()		
	print("pye-motion -pquery")
	print("	read, modify and save single parameters. WARNING: highly")
	print("	experimental! Might cause serious hardware damage!")
	print()
	print("pye-motion -speedlimit")
	print("	shows if 27.5 km/h software speed limit is activated")
	print()		
	print("pye-motion -speedlimit off")
	print("	deactivates software speed limit - allowing the bike to go faster")
	print("	than 27.5 km/h")
	print()		
	print("pye-motion -speedlimit on")
	print("	activate software speed limit to 27,5 km/h by calculating a valid")
	print("	value for P08 based on current wheel diameter and magnet count")
	print()


# function:	listen()
# 	
# 	Input:	-
#	Output:	-
def listen(mondata):
	while 1:
		if mondata.viewmode==0:
			osy.cls()
			print("-------------------------------------------------------------------------------")
			print()
			print("pye-motion - listen modus")
			print()
			print("-------------------------------------------------------------------------------")
			print()
			print("Lights		SC1(Assist)	percAssist	AWD		@C?10")
			print("	%s 		%s 		%s 		%s 		%s " %(mondata.Lights, mondata.SC1TX, mondata.percAssist, mondata.AWD, mondata.C10))
			print()
			print()
			print("Voltage		Current		SC1(Assist)	SC2		Speed")
			print("	%s 		%s 		%s 		%s 		%s " %(mondata.Voltage, mondata.Current, mondata.SC1RX, mondata.SC2, mondata.Speed))
			print()
			print()
			print("@D16-18		@D19-21		@D22-24		@D25-27		Wheelsize")
			print("	%s 		%s 		%s 		%s 		%s " %(mondata.D1618, mondata.D1921, mondata.D2224, mondata.D2527, mondata.wsize))
			print()
			print()
			print("-------------------------------------------------------------------------------")
			print()
			print("TX: %s " %(mondata.TX))
			print("RX: %s " %(mondata.RX))
			print()
			
			rawrx = smessage()
			rawtx = smessage()
			tmpbreak = 0
			while rawrx.readable == 0:
				msg.serialReceive(rawrx, cfg.bhController)
				time.sleep(0.01)
				
			msg.parse(rawrx, mondata)
			
			timestamp = datetime.datetime.now()
			print('%s' % timestamp)
			time.sleep(0.01)

# function:	plisten()
# 	
# 	Input:	-
#	Output:	-
def plisten(mondata):
	frame = 0
	pindex=0
	while 1:
		if mondata.viewmode==0:
			rawtx = None
			rawtx = smessage()
			rawrx = None
			rawrx = smessage()
			
			# send via Serial A
			rawtx.payload = PNAME[pindex]
			msg.serialSend(rawtx, cfg.bhController)
			
			finaltx=""
			for i in range((rawtx.slength)):
				finaltx+=chr(rawtx.rawbuffer[i])
				
			# receive via Serial B
			while rawrx.readable == 0:
				msg.serialReceive(rawrx, cfg.bhController)
				
			finalrx=""
			for i in range(rawrx.slength-3-3-3):
				finalrx+=rawrx.payload[i+3]
			# print String
			
			mondata.PLIST[pindex] = finalrx
			
			pindex+=1
			if pindex >= 100:
				pindex=0
				#tmp=input("press Enter for new scan")
				
			osy.cls()
			print("-------------------------------------------------------------------------------")
			print()
			print("pye-motion - Parameter Listen modus")
			print()
			print("-------------------------------------------------------------------------------")
			print()
			print("P00: %s  P01: %s  P02: %s  P03: %s  P04: %s  P05: %s  P06: %s  P07: %s" %(mondata.PLIST[0], mondata.PLIST[1], mondata.PLIST[2], mondata.PLIST[3], mondata.PLIST[4], mondata.PLIST[5], mondata.PLIST[6], mondata.PLIST[7]))
			print("P08: %s  P09: %s  P10: %s  P11: %s  P12: %s  P13: %s  P14: %s  P15: %s" %(mondata.PLIST[8], mondata.PLIST[9], mondata.PLIST[10], mondata.PLIST[11], mondata.PLIST[12], mondata.PLIST[13], mondata.PLIST[14], mondata.PLIST[15]))
			print("P16: %s  P17: %s  P18: %s  P19: %s  P20: %s  P21: %s  P22: %s  P23: %s" %(mondata.PLIST[16], mondata.PLIST[17], mondata.PLIST[18], mondata.PLIST[19], mondata.PLIST[20], mondata.PLIST[21], mondata.PLIST[22], mondata.PLIST[23]))
			print("P24: %s  P25: %s  P26: %s  P27: %s  P28: %s  P29: %s  P30: %s  P31: %s" %(mondata.PLIST[24], mondata.PLIST[25], mondata.PLIST[26], mondata.PLIST[27], mondata.PLIST[28], mondata.PLIST[29], mondata.PLIST[30], mondata.PLIST[31]))
			print("P32: %s  P33: %s  P34: %s  P35: %s  P36: %s  P37: %s  P38: %s  P39: %s" %(mondata.PLIST[32], mondata.PLIST[33], mondata.PLIST[34], mondata.PLIST[35], mondata.PLIST[36], mondata.PLIST[37], mondata.PLIST[38], mondata.PLIST[39]))
			print("P40: %s  P41: %s  P42: %s  P43: %s  P44: %s  P45: %s  P46: %s  P47: %s" %(mondata.PLIST[40], mondata.PLIST[41], mondata.PLIST[42], mondata.PLIST[43], mondata.PLIST[44], mondata.PLIST[45], mondata.PLIST[46], mondata.PLIST[47]))
			print("P48: %s  P49: %s  P50: %s  P51: %s  P52: %s  P53: %s  P54: %s  P55: %s" %(mondata.PLIST[48], mondata.PLIST[49], mondata.PLIST[50], mondata.PLIST[51], mondata.PLIST[52], mondata.PLIST[53], mondata.PLIST[54], mondata.PLIST[55]))
			print("P56: %s  P57: %s  P58: %s  P59: %s  P60: %s  P61: %s  P62: %s  P63: %s" %(mondata.PLIST[56], mondata.PLIST[57], mondata.PLIST[58], mondata.PLIST[59], mondata.PLIST[60], mondata.PLIST[61], mondata.PLIST[62], mondata.PLIST[63]))
			print("P64: %s  P65: %s  P66: %s  P67: %s  P68: %s  P69: %s  P70: %s  P71: %s" %(mondata.PLIST[64], mondata.PLIST[65], mondata.PLIST[66], mondata.PLIST[67], mondata.PLIST[68], mondata.PLIST[69], mondata.PLIST[70], mondata.PLIST[71]))
			print("P72: %s  P73: %s  P74: %s  P75: %s  P76: %s  P77: %s  P78: %s  P79: %s" %(mondata.PLIST[72], mondata.PLIST[73], mondata.PLIST[74], mondata.PLIST[75], mondata.PLIST[76], mondata.PLIST[77], mondata.PLIST[78], mondata.PLIST[79]))
			print("P80: %s  P81: %s  P82: %s  P83: %s  P84: %s  P85: %s  P86: %s  P87: %s" %(mondata.PLIST[80], mondata.PLIST[81], mondata.PLIST[82], mondata.PLIST[83], mondata.PLIST[84], mondata.PLIST[85], mondata.PLIST[86], mondata.PLIST[87]))
			print("P88: %s  P89: %s  P90: %s  P91: %s  P92: %s  P93: %s  P94: %s  P95: %s" %(mondata.PLIST[88], mondata.PLIST[89], mondata.PLIST[90], mondata.PLIST[91], mondata.PLIST[92], mondata.PLIST[93], mondata.PLIST[94], mondata.PLIST[95]))
			print("P96: %s  P97: %s  P98: %s  P99: %s  " 								   %(mondata.PLIST[96], mondata.PLIST[97], mondata.PLIST[98], mondata.PLIST[99]))
			
			#print()
			#print("-------------------------------------------------------------------------------")
			#print()
			#print("TX: %s " %(mondata.TX))
			#print("RX: %s " %(mondata.RX))
			#print()
			#timestamp = datetime.datetime.now()
			#print('%s' % timestamp)
			#frame+=1
			time.sleep(0.01)	

# function:	pquery()
# 	
# 	Input:	-
#	Output:	-
def pquery(mondata):
	frame = 0
	while 1:
		osy.cls()
		rawtx = None
		rawtx = smessage()
		rawrx = None
		rawrx = smessage()
		print("-------------------------------------------------------------------------------")
		print()
		print("pye-motion - query modus")
		print("WARNING: highly experimental - might cause serious hardware damage!")
		print()
		print("-------------------------------------------------------------------------------")
		print()
		print()
		print()
		
		# send via Serial A
		rawtx.payload = input("query:      ")
		serialSend(rawtx, bhController)
		
		finaltx=""
		for i in range((rawtx.slength)):
				finaltx+=chr(rawtx.rawbuffer[i])
		
		# receive via Serial B
		while rawrx.readable == 0:
			msg.serialReceive(rawrx, cfg.bhController)
		
		finalrx=""
		for i in range(rawrx.slength):
				finalrx+=chr(rawrx.rawbuffer[i])
		# print String

		
		print()
		print()
		print("TX - raw:  ", finaltx)
		print("RX - raw:  ", finalrx)
		print()
		print("RX answer: ", rawrx.payload)
		print()
		rawtx = input("press enter to continue")