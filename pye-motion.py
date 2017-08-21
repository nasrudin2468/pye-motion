###############################################################################
#
# pye-motion - an open source diagnostic toolkit for BH E-bike systems
# This code is released under *TODO search suitable open source licence*
#
###############################################################################

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

#Import external functions



#	TODO:
#	- TX RX Handlers
#	- TX RX Parsers
#	- Basic Logging
#	- Basic TX Construction mode (Parameter Reading P00 P59)
#	- PDCURSES?


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
		
		

# Functions
def saddecb(message):
	if (message.readable == 1):
		return -1
		
	messagesum=0
	for i in (range(message.bufferrindex)-3):
		messagesum+=message.rawbuffer(i)
		

def scheckecb(message):
	return

def sget(message, ser):
	while True:
		temp = 0
		temp = int.from_bytes(ser.read(),byteorder='little')
		
		if  temp != 0:
			# write into objbuffer
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
	
def ssend(message, ser):
	#calc size of payload
	message.slength = len(message.payload) + 6
	
	if message.slength <= 8:
		print("bad message.")
	
	#convert payload, add header and footer
	message.rawbuffer[0] = 64
	message.rawbuffer[1] = 48
	message.rawbuffer[2] = 49
	
	for i in range(message.slength-6):
		message.rawbuffer[i+3]=ord(message.payload[i])
	
	#calc and add ecb
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
	
	#send
	ser.write(message.rawbuffer)
	
	return

def bhparser(message, bhdata):
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
		
		
		

# clear console
def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def main_listen(mondata):
	frame = 0
	rawrx = smessage()
	rawtx = smessage()
	while 1:
		rawrx = smessage()
		rawtx = smessage()
		while rawrx.readable == 0:
			sget(rawrx, ser_A)
		bhparser(rawrx, mondata)
		
		if mondata.viewmode==0:
			cls()
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
			timestamp = datetime.datetime.now()
			print('%s' % timestamp)
			#frame+=1
			time.sleep(0.01)	
			
def p_listen(mondata):
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
			ssend(rawtx, ser_A)
		
			finaltx=""
			for i in range((rawtx.slength)):
				finaltx+=chr(rawtx.rawbuffer[i])
		
			# receive via Serial B
			while rawrx.readable == 0:
				sget(rawrx, ser_A)
		
			finalrx=""
			for i in range(rawrx.slength-3-3-3):
				finalrx+=rawrx.payload[i+3]
			# print String
			
			mondata.PLIST[pindex] = finalrx
			
			pindex+=1
			if pindex >= 100:
				pindex=0
				#tmp=input("press Enter for new scan")
				
			cls()
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



#beginn main

# init global vars
data_A = smessage()
bhdata_A = bhdata()

def query(mondata):
	frame = 0
	while 1:
		cls()
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
		ssend(rawtx, ser_A)
		
		finaltx=""
		for i in range((rawtx.slength)):
				finaltx+=chr(rawtx.rawbuffer[i])
		
		# receive via Serial B
		while rawrx.readable == 0:
			sget(rawrx, ser_A)
		
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
		

#welcome screen
cls()	
print("-------------------------------------------------------------------------------")
print()
print("pye-motion V0.0.1 - an open source diagnostic toolkit for BH E-bike systems")
print()
print("-------------------------------------------------------------------------------")
print()

print("configuration:")
print()



config = configparser.ConfigParser()
config.read('pye-motion.cfg')
usagemode = config['MAIN']['usagemode']

port_A = config['SERIAL-A']['port']
baud_A = config['SERIAL-A']['baudrate']
bitcount_A = config['SERIAL-A']['bitcount']
parity_A = config['SERIAL-A']['parity']
stopbit_A = config['SERIAL-A']['stopbit']

port_B = config['SERIAL-B']['port']
baud_B = config['SERIAL-B']['baudrate']
bitcount_B = config['SERIAL-B']['bitcount']
parity_B = config['SERIAL-B']['parity']
stopbit_B = config['SERIAL-B']['stopbit']

if len(sys.argv) == 1:
	print('No command line argument given. using Main Settings:')
	print(' usagemode = '+ usagemode)
else:
	if (sys.argv[1] in ( "listen", "plisten", "query", "cb-B")):
		print ("usagemode from cmd-arg: "+ str(sys.argv[1]))
		usagemode = str(sys.argv[1])
	else: 
		print('invalid command line argument given. using Main Settings:')
		print(' usagemode = '+ usagemode)

print()
print('Serial-A')
print(' port = '+ port_A)
print(' baudrate = '+ baud_A)
print(' busconfig = '+bitcount_A+parity_A+stopbit_A);
print()
print('Serial-B')
print(' port = '+ port_B)
print(' baudrate = '+ baud_B)
print(' busconfig = '+bitcount_B+parity_B+stopbit_B);
print()

# Fire up configured serial adapters
ser_A = serial.Serial(port_A, baudrate=baud_A, timeout=1)  # open first serial port
print ("Serial-A sucessfully openend: " + ser_A.portstr)
  
#ser_B = serial.Serial(port_B, baudrate=baud_B, timeout=1)  # open second serial port
#print ("Serial-B sucessfully openend: " + ser_B.portstr)

#print (ser_A.in_waiting)
#receive = ser_A.read(11)
#print (receive.decode("utf-8"))

#while data_A.readable == 0:
#	sget(data_A, ser_A)
#bhparser(data_A, bhdata_A)
time.sleep(1)

monitordata= mondata()
#mondata_init(monitordata)
mondata.viewmode=0

if usagemode == "listen":
	main_listen(monitordata)
elif usagemode == "plisten":
	p_listen(monitordata)
elif usagemode == "query":
	query(monitordata)
elif usagemode == "cb-B":
	main_sim("A")

#cls();

#ser = serial.Serial(port_A, py pybaudrate=baud_A, timeout=1)  # open first serial port
#print ("Port opened: " + ser.portstr)       # check which port was really used
#ser.write("hello world".encode("utf-8"))      # write a string
#receive = ser.read(11)
#print (receive.decode("utf-8"))
#ser.close()             # close port