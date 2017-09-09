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
	
