###############################################################################
#
# pye-motion - an open source diagnostic toolkit for BH E-bike systems
# This code is released under *TODO search suitable open source licence*
#
###############################################################################

class serconf:
	def __init(self):
		port_A = ""
		baud_A = ""
		bitcount_A = ""
		parity_A = ""
		stopbit_A = ""
	
		port_B = ""
		baud_B = ""
		bitcount_B = ""
		parity_B = ""
		stopbit_B = ""

def config(sc):
	sc.port_A = config['SERIAL-A']['port']
	sc.baud_A = config['SERIAL-A']['baudrate']
	sc.bitcount_A = config['SERIAL-A']['bitcount']
	sc.parity_A = config['SERIAL-A']['parity']
	sc.stopbit_A = config['SERIAL-A']['stopbit']
	
	sc.port_B = config['SERIAL-B']['port']
	sc.baud_B = config['SERIAL-B']['baudrate']
	sc.bitcount_B = config['SERIAL-B']['bitcount']
	sc.parity_B = config['SERIAL-B']['parity']
	sc.stopbit_B = config['SERIAL-B']['stopbit']
	
def open_A(ser_A, sc):
	ser_A = serial.Serial(sc.port_A, baudrate=sc.baud_A, timeout=1)  # open first serial port
	print ("Serial-A sucessfully openend: " + ser_A.portstr)
	return ser_A
	
def open_B(ser_B, sc):
	ser_B = serial.Serial(sc.port_B, baudrate=sc.baud_B, timeout=1)  # open first serial port
	print ("Serial-B sucessfully openend: " + ser_B.portstr)
	return ser_B
	
