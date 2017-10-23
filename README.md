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

- Download and install Python 3.6.X (https://www.python.org/downloads/)
- Download and install lib dependencies (navigate to the pye-motion folder 
  first): pye-motion.py -install
- Install driver for your serial-usb adapter(s) and plug them in
	
Windows:
- Open up device manager and note the com-port(s) your serial-usb adapter(s) use

Linux: 
- Open terminal and check available ports without adapter connected: 
  "$dmesg | grep tty"
- Connect adapter and repeat scan. New device should be your adapter. 
  Sample: /dev/TTyS2
  
MAC:
- I honestly have no idea. Please contact me if you know

- Go to pye-motion directory and open up py-motion.cfg with a texteditor and
  change the COM-Port Value of [SERIAL-A]/Port (and [SERIAL-B]/Port) according
  to the values you noted before. Don't forget to save.


--------------------------------------------------------------------------------
3. Usage

pye-motion is a command line tool. To use it open up your OS-terminal and 
navigate to the pye-motion folder. 
Start the tool by entering pye-motion.py with or without arguments. 
Stop the tool by pressing CTRL-C.


pye-motion 
			Starting pye-motion without any gives you the program version. It 
			also checks for python lib depencies and suggests using -help to get 
			additional information about usage

pye-motion -help
			lists all available command arguments and how to use them
			
pye-motion -install 
			installs lib dependencies via python pip
			
pye-motion -listen
			Passive listen modus. shows transfered raw messages as well as a 
			table of all scaled livemodus values.

pye-motion -plisten
			read all parameter values from memory and show them in a table
			
pye-motion -pquery
			read, modify and save single parameters. WARNING: highly 
			experimental! Might cause serious hardware damage!

pye-motion -speedlimit
			shows if 27.5 km/h software speed limit is activated. 
			CAREFUL: please note down the shown original P08 value before 
			delimiting!

pye-motion -speedlimit off
			deactivates software speed limit - allowing the bike to go faster
			than 27.5 km/h. CAREFUL: please note down the original P08 value 
			before delimiting!
			
pye-motion -speedlimit on
			activate software speed limit to 27,5 km/h by changing P08 to given 
			value.
