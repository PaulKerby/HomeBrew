import time

import Socket
import TempSensor

Socket.Initialise()

highest_temp = 0
lowest_temp = 100

while True:

	temp = TempSensor.read_temp(TempSensor.temp_sensor_blue)
	temp_top = TempSensor.read_temp(TempSensor.temp_sensor_black)

	if temp > highest_temp:
		highest_temp = temp

	if temp < lowest_temp:
		lowest_temp = temp

	print( 'Current: ' + str( temp ) + ' Highest: ' + str( highest_temp ) + ' Lowest: ' + str( lowest_temp ) )
	print( 'Current Top: ' + str( temp_top ) )
	
	if temp < 19:
		print('Socket On')
		Socket.SetSocket(Socket.socket_one_on)
		time.sleep(120)
		
	Socket.SetSocket(Socket.socket_one_off)
	
	time.sleep(180)
