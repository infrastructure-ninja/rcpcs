#!/usr/bin/python3


# DMX Lighting Controller Component
# Part of the RCPCS project (Room Control and Puzle Coordination System)
# Copyright (C) 2019  Joel D. Caturia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Python3 Dependencies:
#  - PyDMX (included in source control)
#     [http://pydmx.sourceforge.net/]
#
#   - paho-mqtt-client
#   $> sudo pip3 install paho-mqtt
#

import argparse
import paho.mqtt.client as mqtt
import time
import json

from PyDMX import *

parser = argparse.ArgumentParser(description='Provide DMX lighting support in an MQTT ecosystem.')

parser.add_argument('mqttHost', metavar='<MQTT BROKER>', help='The IP/hostname of the MQTT broker to connect to.')
parser.add_argument('puzzleID', metavar='<PUZZLE ID>', help='The name of the puzzle. Will be used in all other places to reference this puzzle controller.')
parser.add_argument('serialPort', metavar='<SERIAL PORT>', help='The serial port that your DMX data will be sent out of.')

args = parser.parse_args()

brokerIP         = args.mqttHost
brokerPort       = 1883
puzzleName       = args.puzzleID
serialPort	 = args.serialPort

def on_connect(client, userdata, flags, rc):
    client.subscribe('COLI/' + puzzleName + '/ACTIVATE_CUE')
#end def

REDchan   = 0
GREENchan = 0
BLUEchan  = 0

def on_message(client, userdata, message):

	global REDchan, GREENchan, BLUEchan

	print('INCOMING TOPIC ->' + message.topic)

	if 'ACTIVATE_CUE' in message.topic:
        
		incomingCommand = message.payload.decode()

		if incomingCommand == '1':
			print('CMD 1')
			REDchan   = 0
			GREENchan = 0
			BLUEchan  = 255

		elif incomingCommand == '2':
			print('CMD 2')
			REDchan   = 255
			GREENchan = 0
			BLUEchan  = 0

		elif incomingCommand == '3':
			print('CMD 3')
			REDchan   = 0
			GREENchan = 255
			BLUEchan  = 0
		else:
			print('UNHANDLED INCOMING COMMAND -> [' + incomingCommand + ']')
  
		dmx.set_data(2, REDchan)
		dmx.set_data(3, GREENchan)
		dmx.set_data(4, BLUEchan)
		dmx.send()

	else:
		client.publish('CILO/' + puzzleName + '/ERROR', 'Unrecognized data received: [TOPIC: {}, PAYLOAD: {}]'.format(message.topic, message.payload.decode() ))

        #end if
    #end if
#end def


try:
  client = mqtt.Client()
  client.connect(brokerIP, brokerPort, 60)
  client.loop_start()

except:
  print('\r\nERROR: unable to communicate with MQTT broker. Exiting...')
  exit()

#end try
client.on_connect = on_connect
client.on_message = on_message

dmx = PyDMX(serialPort)

dmx.set_data(1, 255)
dmx.set_data(2, REDchan)
dmx.set_data(3, GREENchan)
dmx.set_data(4, BLUEchan)

while True:
	dmx.send()
	#time.sleep(.10)
