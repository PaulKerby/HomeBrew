#sudo apt-get install python-rpi.gpio

#import the required modules
import RPi.GPIO as GPIO
import time

def Initialise():
	# set the pins numbering mode
	GPIO.setmode(GPIO.BOARD)
	# Select the GPIO pins used for the encoder K0-K3 data inputs
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(15, GPIO.OUT)
	GPIO.setup(16, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)
	# Select the signal used to select ASK/FSK
	GPIO.setup(18, GPIO.OUT)
	# Select the signal used to enable/disable the modulator
	GPIO.setup(22, GPIO.OUT)

	# Disable the modulator by setting CE pin lo
	GPIO.output (22, False)
	# Set the modulator to ASK for On Off Keying
	# by setting MODSEL pin lo
	GPIO.output (18, False)
	# Initialise K0-K3 inputs of the encoder to 0000
	GPIO.output (11, False)
	GPIO.output (13, False)
	GPIO.output (15, False)
	GPIO.output (16, False)

	
def SetModulator():
	# let it settle, encoder requires this
	time.sleep(0.1)
	# Enable the modulator
	GPIO.output (22, True)
	# keep enabled for a period
	time.sleep(0.25)
	# Disable the modulator
	GPIO.output (22, False)


# The On/Off code pairs correspond to the hand controller codes.
# True = '1', False ='0'
# 0011 and 1011 all ON and OFF
# 1111 and 0111 socket 1
# 1110 and 0110 socket 2
# 1101 and 0101 socket 3
# 1100 and 0100 socket 4

try:
	# We will just loop round switching the unit on and off
	while True:
		raw_input('hit return key to send socket 1 ON code')
		# Set K0-K3
		print "sending code 1111 socket 1 on"
		GPIO.output (11, True)
		GPIO.output (15, True)
		GPIO.output (16, True)
		GPIO.output (13, True)
		SetModulator()
		raw_input('hit return key to send socket 1 OFF code')
		# Set K0-K3
		print "sending code 0111 Socket 1 off"
		GPIO.output (11, True)
		GPIO.output (15, True)
		GPIO.output (16, True)
		GPIO.output (13, False)
		SetModulator()
		raw_input('hit return key to send ALL ON code')
		# Set K0-K3
		print "sending code 1011 ALL on"
		GPIO.output (11, True)
		GPIO.output (15, True)
		GPIO.output (16, False)
		GPIO.output (13, True)
		SetModulator()
		raw_input('hit return key to send ALL OFF code')
		# Set K0-K3
		print "sending code 0011 All off"
		GPIO.output (11, True)
		GPIO.output (15, True)
		GPIO.output (16, False)
		GPIO.output (13, False)
		SetModulator()
	
	except KeyboardInterrupt:
		GPIO.cleanup()