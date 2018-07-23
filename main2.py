import time

import Socket
import TempSensor

import boto3

Socket.Initialise()

highest_temp = 0
lowest_temp = 100

TABLE_NAME = "HB_Fermentation"
REGION = "eu-west-2"

session = boto3.Session(region_name=REGION)
boto3_dynamo = session.resource('dynamodb', REGION)
f_table = boto3_dynamo.Table(TABLE_NAME)

while True:

	temp = TempSensor.read_temp(TempSensor.temp_sensor_blue)
	temp_top = TempSensor.read_temp(TempSensor.temp_sensor_black)

	if temp > highest_temp:
		highest_temp = temp

	if temp < lowest_temp:
		lowest_temp = temp

	print( 'Current: ' + str( temp ) + ' Highest: ' + str( highest_temp ) + ' Lowest: ' + str( lowest_temp ) )
	print( 'Current Top: ' + str( temp_top ) )
	
	socket_on = 'No'
	if temp < 19:
		print('Socket On')
		socket_on = 'Yes'
		Socket.SetSocket(Socket.socket_one_on)

	f_table.put_item(Item={'Time':int(time.time()), 'Ambient': int(temp*100), 'BrewID':0, 'Wort': int(temp_top*100), 'Heat': socket_on})

	time.sleep(120)
		
	Socket.SetSocket(Socket.socket_one_off)
	
	time.sleep(180)
