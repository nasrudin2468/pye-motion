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

# function:	read(message)
# 	-
# 	Input:	name of array
#	Output:	modifies input
def read(arrcfg):
	# create new Parser and read file
	config = configparser.ConfigParser()
	config.read('pye-motion.cfg')
	
	# Save values from file into given array
	arrcfg.hwconfig = config['MAIN']['hwconfig']

	arrcfg.port_A = config['SERIAL-A']['port']
	arrcfg.baud_A = config['SERIAL-A']['baudrate']
	arrcfg.bitcount_A = config['SERIAL-A']['bitcount']
	arrcfg.parity_A = config['SERIAL-A']['parity']
	arrcfg.stopbit_A = config['SERIAL-A']['stopbit']

	arrcfg.port_B = config['SERIAL-B']['port']
	arrcfg.baud_B = config['SERIAL-B']['baudrate']
	arrcfg.bitcount_B = config['SERIAL-B']['bitcount']
	arrcfg.parity_B = config['SERIAL-B']['parity']
	arrcfg.stopbit_B = config['SERIAL-B']['stopbit']
	return
	