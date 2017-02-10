#!/usr/bin/python 
##########################################################
## Python code for Lift Operation Simulation using
## Beaglebone Black running Debian 7 Linux distribution
##########################################################
## Developed by MicroEmbedded Technologies
##########################################################
 
# Import standard python libraries
import sys
import time
import select

##############################################################
# GPIO Pin definitions for Lift Simulation Board 
# Please refer "MicroEmbedded_BBB_Interfacing Details_New.pdf" 
# for all the PIN details
##############################################################

LED_1	=	(0 * 32) + 3		
LED_2	=	(0 * 32) + 23		
LED_3	=	(0 * 32) + 2		
LED_4	=	(0 * 32) + 26		

LED_5	=	(1 * 32) + 17		
LED_6	=	(1 * 32) + 15		
LED_7	=	(0 * 32) + 15		
LED_8	=	(1 * 32) + 14		

LED_9	=	(0 * 32) + 30
LED_10	=	(2 * 32) + 2
LED_11	=	(1 * 32) + 28
LED_12	=	(2 * 32) + 3
LED_13	=	(0 * 32) + 31
LED_14	=	(2 * 32) + 5
LED_15	=	(1 * 32) + 18

SW_1	=	(0 * 32) + 14		
SW_2	=	(0 * 32) + 27		
SW_3	=	(0 * 32) + 22		
SW_4	=	(2 * 32) + 1	



# DIRECTIN LEDS: to represent lift direction (up or down) 
LIFT_DIR_1   =    LED_9
LIFT_DIR_2   =    LED_10
LIFT_DIR_3   =    LED_11
LIFT_DIR_4   =    LED_12
LIFT_DIR_5   =    LED_13
LIFT_DIR_6   =    LED_14
LIFT_DIR_7   =    LED_15


# POSITION LEDS: LEDs to indicate the current position of Lift 
LIFT_POS_0   =    LED_5
LIFT_POS_1   =    LED_6
LIFT_POS_2   =    LED_7
LIFT_POS_3   =    LED_8


# LIFT BUTTONS: corresponding to each floor of the Lift 
LIFT_BUTTON_0   =    SW_1
LIFT_BUTTON_1   =    SW_2
LIFT_BUTTON_2   =    SW_3
LIFT_BUTTON_3   =    SW_4

# LIFT LEDS: indication for BUTTON Press on each floor 
LIFT_LED_0   =    LED_1
LIFT_LED_1   =    LED_2
LIFT_LED_2   =    LED_3
LIFT_LED_3   =    LED_4


# An array of DIRECTIN LEDS 
dir_leds = [ 	LIFT_DIR_1,
		LIFT_DIR_2,
		LIFT_DIR_3,
		LIFT_DIR_4,
		LIFT_DIR_5,
		LIFT_DIR_6,
		LIFT_DIR_7
	   ]	

# An array of POSITION LEDS 
pos_leds = [
		LIFT_POS_0,
		LIFT_POS_1,
		LIFT_POS_2,
		LIFT_POS_3
	   ]

# An array of BUTTON PRESS LEDS
lift_leds = [
		LIFT_LED_0,
		LIFT_LED_1,
		LIFT_LED_2,
		LIFT_LED_3
	   ]

# An array of lift BUTTONs
lift_buttons = [
		 LIFT_BUTTON_0,
		 LIFT_BUTTON_1,
		 LIFT_BUTTON_2,
		 LIFT_BUTTON_3
	   ]


NO_OF_FLOORS	  =	4		# No of floors for Lift Simulation Operation
NO_OF_DIR_LEDS	  =	7		# No of LEDs used for the lift direction (on Board)
DEFAULT_LIFT_POS =	0		# The floor no where lift is positioned when program is executed


# Array associated with each floor having 4 elements; each again having 3 elements fd, button and led
floor_set = [
		{"fd":-1, "button":LIFT_BUTTON_0, "led":LIFT_LED_0},		# fd, Button and LED for 0th (Ground) Floor
		{"fd":-1, "button":LIFT_BUTTON_1, "led":LIFT_LED_1},		# fd, Button and LED for 1st Floor
		{"fd":-1, "button":LIFT_BUTTON_2, "led":LIFT_LED_2},		# fd, Button and LED for 2nd Floor        
		{"fd":-1, "button":LIFT_BUTTON_3, "led":LIFT_LED_3}		# fd, Button and LED for 3rd Floor

             ]
             
# PATH of a GPIO specific sysfs interfce directory on Linux system             
SYSFS_GPIO_DIR = "/sys/class/gpio"


             	
################################################################################
# Description 	: Write the GPIO PIN value on "/sys/class/gpio/export" file.
# 		 This will export (make visible) the directory associated
#		 with particular GPIO pin under sysfs interface.
#		 e.g. if value of GPIO PIN is "23" then "/sys/class/gpio/gpio23"
#		 directory will be exported (will become visible)
# Input   	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: Must be called for a particular GPIO PIN before using that PIN.
################################################################################
def gpioExport (gpio): 
	try:
   		fo = open(SYSFS_GPIO_DIR + "/export","w")  			
   		fo.write(gpio)
   		fo.close()
   		return
   	except IOError:
                return

#################################################################################
# Description : Exactly opposite of export() function above.
# 		 Write the GPIO PIN value on "/sys/class/gpio/unexport" file.
# 		 This will un-export (make invisible) the directory associated
#		 with particular GPIO pin under sysfs interface.
#		 e.g. if value of GPIO PIN is "23" then "/sys/class/gpio/gpio23"
#		 directory will be unexported (will become invisible)
# Input	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: Must be called for a particular GPIO PIN after it is used
# 		  This makes a PIN free from GPIO functionality
#################################################################################
def gpioUnexport (gpio):
	try: 
   		fo = open(SYSFS_GPIO_DIR + "/unexport","w")  
   		fo.write(gpio)
   		fo.close()
   		return
   	except IOError:
 		return


################################################################################################
# Description : Write the direction ("in"/"out") on "/sys/class/gpio/gpioN/direction"
#               where "gpioN" stands for the directory already exported.
# 		 This will configure a particular GPIO PIN as an input or output pin.
# Input	: @gpio = Value of GPIO PIN (in the form of string)
# 		  @flag  = Value of direction either "in" or "out"
# Return	: None
# Note		: Make sure to export a GPIO PIN (using gpioExport) before calling this function
#################################################################################################

def gpioSetDir (gpio, flag):
	try: 
	   	fo = open(SYSFS_GPIO_DIR + "/gpio" + gpio + "/direction" ,"w")  
	   	fo.write(flag)
	   	fo.close()
	   	return
 	except IOError:
                return

################################################################################################
# Description  : Write the value ("0"/"1") on "/sys/class/gpio/gpioN/value"
#                where "gpioN" stands for the directory already exported.
# 		  This will make particular GPIO PIN as LOW or HIGH (CLEAR or SET).
# Input   	: @gpio = Value of GPIO PIN (in the form of string)
# 		  @val  = Value of GPIO either "0" or "1"
# Return	: None
# Note		: Make sure to export a GPIO PIN (using gpioExport) and
# 		  set the direction as "out" (using gpioSetDir) before calling this function
#################################################################################################

def gpioSetVal (gpio, val):
	try: 
		fo = open(SYSFS_GPIO_DIR + "/gpio" + gpio + "/value" ,"w")  
		fo.write(val)
		fo.close()
		return
	except IOError:
                return


################################################################################################
# Description  : Write the Edge value on "/sys/class/gpio/gpioN/edge"
#                where "gpioN" stands for the directory already exported.
# 		 This will set the GPIO edge value.
# 		 Edge can be set to any of the 4 values
# 			"falling"	"rising" 	"both"		"none"
# Input		: @gpio = Value of GPIO PIN (in the form of string)
#		  @flag  = Value of GPIO edge
# Return	: None
# Note		: Make sure to export a GPIO PIN (using gpioExport) before calling this function
#################################################################################################

def gpioSetEdge (gpio, flag): 
	try:
		fo = open(SYSFS_GPIO_DIR + "/gpio" + gpio + "/edge" ,"w")  
		fo.write(flag)
		fo.close()
   		return
	except IOError:
                return

#################################################################################
# Description  : Function to clean up a particular liftLED
#		  Means Clear the LED and unexport the GPIO PIN
# Input        : @gpio = Value of GPIO PIN (in the form of string)
# Return       : None
# Note	       : This function is called for every LED on lift simulation board
#################################################################################
def liftLEDExit (gpio):
	gpioSetVal(gpio, val="0")
	gpioUnexport(gpio)
	return 


###################################################################################
# Description  : Function to initialize a particular liftLED
#		 Means export the GPIO PIN for LED, Set its direction as "out"
#		 and Clear the LED (Make it "OFF").
#		 Initially we keep all the LEDs in OFF status.
# Input 	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: This function is called for every liftLED
###################################################################################
	
def liftLEDInit (gpio):
	gpioExport(gpio)
	gpioSetDir(gpio, flag="out")
 	gpioSetVal(gpio, val="0")
 	return


###################################################################################
# Description  : Function to make a particular liftLED ON
#		  Means make the LED "ON", by writing "1" to it's GPIO PIN
# Input  	: @gpio = Value of GPIO PIN (in the form of string)
# Return   	: None
# Note		: Make sure to initialize a particular liftLED using
# 		  liftLEDInit() before calling this function
###################################################################################
 	
def liftLEDOn (gpio):
	gpioSetVal(gpio, val="1")
	return 


###################################################################################
# Description  : Function to make a particular liftLED OFF
#		  Means make the LED "OFF", by writing "0" to it's GPIO PIN
# Input   	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: Make sure to initialize a particular liftLED using
# 		  liftLEDInit() before calling this function
#####################################################################################
def liftLEDOff (gpio):
	gpioSetVal(gpio, val="0")
	return 

###############################################################################
# Description  : Function to clean up a particular lift button
#		 It will unexport the GPIO PIN associated with lift button
# Input   	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: This function is called for every lift button.
#################################################################################

def liftButtonExit (gpio):
	gpioUnexport(gpio)
	return 
	
###################################################################################
# Description  : Function to initialize a particular button
#		 Means export the GPIO PIN for button, Set its direction as "in"
#		 and set its edge as "falling".
# Input   	: @gpio = Value of GPIO PIN (in the form of string)
# Return	: None
# Note		: This function is called for every lift button.
#####################################################################################
def liftButtonInit (gpio):
	gpioExport(gpio)
	gpioSetDir(gpio, flag="in")
 	gpioSetEdge(gpio, flag="falling")
 	return



###################################################################################
# Description  : Initialize all the lift LEDs and BUTTONs one-by-one.
#		 Observe that each time liftLEDInit() or liftButtonInit() is called,
#		 LED/BUTTON value is converted from integer number to a string
#		 and then it is passed as a parameter.
# Input       	: None
# Return	: None
# Note		: This function should be called from the main() before starting
# 		  the lift simulation loop
#####################################################################################

def liftInitAll():
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDInit(str(dir_leds[i]))
			
	for i in range(0, NO_OF_FLOORS):
		liftLEDInit(str(pos_leds[i]))
		liftLEDInit(str(lift_leds[i]))
		liftButtonInit(str(lift_buttons[i]))
	return	


###################################################################################################
# Description  : Cleanup all the lift LEDs and BUTTONs one-by-one.
#		 Observe that each time liftLEDExit() or liftButtonExit is called,
#		 LED/BUTTON is converted from integer number to a string and then
#		 it is passed as a parameter.
# Input	: None
# Return	: None
# Note		: This function can be called,
# 				1) From main() after ending the liftLED simulation loop
# 				2) From signal handler of SIGINT to clean-up and restore the
# 				   LEDs, whenever CTRL+C is pressed (mostly from BBB shell prompt)
###################################################################################################
def liftExitAll():
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDExit(str(dir_leds[i]))
			
	for i in range(0, NO_OF_FLOORS):
		liftLEDExit(str(pos_leds[i]))
		liftLEDExit(str(lift_leds[i]))
		liftButtonExit(str(lift_buttons[i]))
	print "\n=== Demonstration END ===\n"
	return	

###################################################################################
# Description  : Set the default position of the lift,
#		 by glowing the position LED defined by DEFAULT_LIFT_POS
#		 (DEFAULT_LIFT_POS = 0th floor i.e. ground floor)
# Input	: None
# Return	: None
# Note		: This function must be called from main() after inititalization
#####################################################################################
def liftDefaultPos():
	liftLEDOn(str(pos_leds[DEFAULT_LIFT_POS]))
	return 


###################################################################################
# Description  : Glow the direction LEDs in upward direction.
#		 This indicates that lift is going to upper floor(s).
# Input	: None
# Return	: None
# Note		: This function is used when lift is called from upper
# 		  floor than the current position of the lift
#####################################################################################
def liftDirUp():
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDOn(str(dir_leds[i]))
		time.sleep(0.5)
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDOff(str(dir_leds[i]))
	return


###################################################################################
# Description  : Glow the direction LEDs in downward direction.
#		 This indicates that lift is going to lower floor(s).
# Input   	: None
# Return	: None
# Note		: This function is used when lift is called to lower
# 		  floor than the current position of the lift
#####################################################################################

def liftDirDown():
	for i in range(NO_OF_DIR_LEDS, 0, -1):
		liftLEDOn(str(dir_leds[i-1]))
		time.sleep(0.5)
	for i in range(0, NO_OF_DIR_LEDS):
		liftLEDOff(str(dir_leds[i]))
	return


####################################################################################################
# Description  : This function actually returns the floor number at which lift button is pressed.
# 		  It will prepare all the button FDs for select() call. As soon as select() returns; 
#		  it will retrun a list of FDs (in ex), so traverse ex and check for each fd 
# 		  if it present in ex list. If it is present then coresponding button is pressed 
#		  and so glow the corresponding LED and return i as a return value.	
# Input 	: None
# Return	: Floor Number of lift where button is pressed
####################################################################################################
def GetButtonVal(): 
	try:		
		fo0 = open(SYSFS_GPIO_DIR + "/gpio" + str(LIFT_BUTTON_0) + "/value" ,"r") # Open and get file descriptor of button file of 0th floor 
		fo0.read(2)								  # Make dummy read() call on it	
		floor_set[0]["fd"] = fo0						  # store fd in 0th element of floor_set array	
		
		fo1 = open(SYSFS_GPIO_DIR + "/gpio" + str(LIFT_BUTTON_1) + "/value" ,"r") # Open and get file descriptor of button file of 1st floor
		fo1.read(2)								  # Make dummy read() call on it   	
		floor_set[1]["fd"] = fo1						  # store fd in 1st element of floor_set array
		
		fo2 = open(SYSFS_GPIO_DIR + "/gpio" + str(LIFT_BUTTON_2) + "/value" ,"r") # Open and get file descriptor of button file of 2nd floor
		fo2.read(2)								  # Make dummy read() call on it	
		floor_set[2]["fd"] = fo2						  # store fd in 2nd element of floor_set array	
		
		fo3 = open(SYSFS_GPIO_DIR + "/gpio" + str(LIFT_BUTTON_3) + "/value" ,"r") # Open and get file descriptor of button file of 3rd floor
		fo3.read(2)								  # Make dummy read() call on it   	
		floor_set[3]["fd"] = fo3						  # store fd in 3rd element of floor_set array
		
		print "\nWaiting for button press ..."
		
		# Call to select(). Program will block for input and it will return once button is pressed.
		# We are passing three lists (read fds, write fds and exception fds) to select() function
		# It will retrun three lists as r, w and ex respectively
		# In this case first two lists are NULL, In third list fds associated with lift buttons are passed
		# select() will retrun NULL in r & w and list of fds on which data is available in ex    
		r, w, ex = select.select([], [], [fo0, fo1, fo2, fo3])			
						
		# Detect on which floor button is pressed						
		for i in range(len(floor_set)):						# Run a loop for all (4) floors				
			if floor_set[i]["fd"] in ex:					# Check current fd is present in ex (ex=list of fds on which data is available)  	
				print "LIFT button is pressed for floor #%d" % i	# Print the floor no indicated by i
				liftLEDOn(str(floor_set[i] ["led"]))			# Glow the corresponding LED for floor indicated by i to show button press event
				time.sleep(1)						# Wait for 1 second
				but = i							# Store value of i in but variable
				fo = floor_set[i]["fd"]					# Get the current fd from array 	
				fo.seek(0, 0);						# Call seek() so that fd will point at begining of the file
				str1 = fo.read(1)					# Make dummy read() call on it 
	
		fo0.close()								# Close fd for 0th floor
		fo1.close()								# Close fd for 1st floor
		fo2.close()								# Close fd for 2nd floor
		fo3.close()								# Close fd for 3rd floor
		return but
	
	except IOError:
                return


try:
	print "\nLift Operation Simulation using Python\n"
	print  "-----------------------------------------------\n" 	
	liftInitAll()							# Initialize all lift Buttons and LEDs	
	liftDefaultPos()						# Set dafault position of the lift (0th floor)

	cur_flr = DEFAULT_LIFT_POS					# Variable for current lift floor (initially 0)
	
	while True:
		new_flr = GetButtonVal()		# Get a new floor value by detecting a floor no to which button user calls the lift
		if new_flr > cur_flr:				# if (new floor > current floor) means lift is called to upper floor	
			tmp = cur_flr						# store current floor no into tmp variable
			print "LIFT going UP to floor #%d" %new_flr		# print destination floor
			while (tmp != new_flr):					# Use tmp value (incremental); till it becomes destination
				liftDirUp()					# Glow direction LEDs in upward direction
				time.sleep(0.01)				# sleep for 10 ms
				liftLEDOff(str(pos_leds[tmp]))			# Turn off position LED at the floor pointed by tmp
				tmp += 1					# Increment tmp value by 1
				liftLEDOn(str(pos_leds[tmp]))			# Turn ON position LED at the floor pointed by tmp. Lift is one floor UP
				time.sleep(0.5)					# Sleep for 0.5 second (500 ms)
		elif new_flr < cur_flr:				# if (new floor < current floor) means lift is called to lower floor
			tmp = cur_flr						# store current floor no into tmp variable
			print "LIFT going DOWN to floor #%d" %new_flr		# print destination floor
			while (tmp != new_flr):					# Use tmp value (decremental); till it becomes destination
				liftDirDown()					# Glow direction LEDs in downward direction
				time.sleep(0.01)				# Sleep for 10 ms
				liftLEDOff(str(pos_leds[tmp]))			# Turn off position LED at the floor pointed by tmp
				tmp -= 1					# Decrement tmp value by 1
				liftLEDOn(str(pos_leds[tmp]))			# Turn ON position LED at the floor pointed by tmp. Lift is one floor DOWN
				time.sleep(0.5)					# sleep for 0.5 second (500 ms)	
		
		cur_flr = new_flr			# Once lift reaches the destination; current floor points to destination floor no
		liftLEDOff(str(lift_leds[new_flr]))	# Turn OFF button press indication LED of the destinaton floor
		time.sleep(1)				# Sleep for 1 second
		 
	liftExitAll()					# Clean up all GPIOs	
	exit()						# Exit from Program
except KeyboardInterrupt:				# CTRL-C Exception Handler to cleanup and exit safely from program
	liftExitAll()	
	print "Program Exit due to CTRL-C"
	exit()
    	sys.exit(0)
