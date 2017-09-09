# pye-motion

--------------------------------------------------------------------------------
1. Description

pye-motion is a cross-platform python tool for BH EVO E-Bike drivetrains. It 
simplifies reading messages between controller and display by parsing the data 
and displaying them in a more human readable way.
while changing paramters or sending manual messages pye-motion takes care about 
calcuation and transfer of checksum values.


--------------------------------------------------------------------------------
2. Installation

- download and install Python 3.6.X (https://www.python.org/downloads/)
- download and install pyserial module:
	py -m pip download pyserial
	py -m pip install pyserial
- install driver for your serial-usb adapter(s) and plug them in
	
Windows:
- open up device manager and note the com-port(s) your serial-usb adapter(s) use
- go to pye-motion directory and open up py-motion.cfg with a texteditor and
  change the COM-Port Value of [SERIAL-A]/Port (and [SERIAL-B]/Port) according
  to the values you got from the device manager. Don't forget to save


--------------------------------------------------------------------------------
3. Usage

Open up your OS-terminal and navigate to the pye-motion folder. start the tool 
by entering pye-motion.py

TODO: menues



