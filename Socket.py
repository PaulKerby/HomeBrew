#sudo apt-get install python-rpi.gpio

#import the required modules
import RPi.GPIO as GPIO
import time

# D3 = 13, D2 = 16, D1 = 15, D0 = 11

#D3 D2 D1 D0 Meaning D3 D2 D1 D0 Meaning
#1 0 1 1 All      on 0 0 1 1 All off
#1 1 1 1 socket 1 on 0 1 1 1 socket 1 off
#1 1 1 0 socket 2 on 0 1 1 0 socket 2 off
#1 1 0 1 socket 3 on 0 1 0 1 socket 3 off
#1 1 0 0 socket 4 on 0 1 0 0 socket 4 off

socket_clear = 		{ 13: False, 	16:False, 	15:False, 	11:False }

socket_one_on = 	{ 13: True, 	16:True, 	15:True, 	11:True }
socket_one_off = 	{ 13: False, 	16:True, 	15:True, 	11:True }

socket_two_on = 	{ 13: True, 	16:True, 	15:True, 	11:False }
socket_two_off = 	{ 13: False, 	16:True, 	15:True, 	11:False }

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
	SetSocket( socket_clear )

	
def SetSocket( bits ):
	for key, val in bits.items():
		GPIO.output(key, val)
	
	SetModulator()
	
def SetModulator():
	# let it settle, encoder requires this
	time.sleep(0.1)
	# Enable the modulator
	GPIO.output (22, True)
	# keep enabled for a period
	time.sleep(0.25)
	# Disable the modulator
	GPIO.output (22, False)


#try:
#	# We will just loop round switching the unit on and off
#	while True:
#		raw_input('hit return key to send socket 1 ON code')
#		# Set K0-K3
#		print "sending code 1111 socket 1 on"
#		GPIO.output (11, True)
#		GPIO.output (15, True)
#		GPIO.output (16, True)
#		GPIO.output (13, True)
#		SetModulator()
#		raw_input('hit return key to send socket 1 OFF code')
#		# Set K0-K3
#		print "sending code 0111 Socket 1 off"
#		GPIO.output (11, True)
#		GPIO.output (15, True)
#		GPIO.output (16, True)
#		GPIO.output (13, False)
#		SetModulator()
#		raw_input('hit return key to send ALL ON code')
#		# Set K0-K3
#		print "sending code 1011 ALL on"
#		GPIO.output (11, True)
#		GPIO.output (15, True)
#		GPIO.output (16, False)
#		GPIO.output (13, True)
#		SetModulator()
#		raw_input('hit return key to send ALL OFF code')
#		# Set K0-K3
#		print "sending code 0011 All off"
#		GPIO.output (11, True)
#		GPIO.output (15, True)
#		GPIO.output (16, False)
#		GPIO.output (13, False)
#		SetModulator()
#	
#	except KeyboardInterrupt:
#		GPIO.cleanup()