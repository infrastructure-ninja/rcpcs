#!/usr/bin/python3

# Python3 Dependencies:
#  - paho-mqtt-client
#  $> sudo pip3 install paho-mqtt


# required positional arguments: 
#  - MQTT host
#  - puzzle ID
# optional parameter(s):
#  - always active (does not require activation phase)

import argparse
import paho.mqtt.client as mqtt
import time
import json
import curses
from curses import wrapper

parser = argparse.ArgumentParser(description='Simulate a puzzle in an MQTT ecosystem.')

parser.add_argument('mqttHost', metavar='<MQTT BROKER>', help='The IP/hostname of the MQTT broker to connect to.')
parser.add_argument('puzzleID', metavar='<PUZZLE ID>', help='The name of the puzzle. Will be used in all other places to reference this puzzle controller.')
parser.add_argument('--always-active', action='store_true', dest='alwaysActive', help='Puzzle will always be in active state (and will skip the AUTO state).')

args = parser.parse_args()

brokerIP         = args.mqttHost
brokerPort       = 1883
puzzleName       = args.puzzleID
flagAlwaysActive = args.alwaysActive


if flagAlwaysActive is True:
    puzzleState = 'ACTIVE'
else:
    puzzleState = 'AUTO'
#end if


def on_connect(client, userdata, flags, rc):
    client.subscribe('COPI/' + puzzleName + '/#')
#end def

def on_message(client, userdata, message):

    if ('COMMANDS' in message.topic):
        
        incomingCommand = message.payload.decode()

        if incomingCommand in ['RESET', 'ACTIVATE', 'SOLVE']:

            if incomingCommand == 'RESET':
                
                if flagAlwaysActive is True:
                    updatePuzzleState('ACTIVE')
                else:
                    updatePuzzleState('AUTO')
                #end if
            
            elif incomingCommand == 'ACTIVATE':
                updatePuzzleState('ACTIVE')

            elif incomingCommand == 'SOLVE':
                updatePuzzleState('SOLVED')
            #end if

        else:
            client.publish('CIPO/' + puzzleName + '/ERROR', 'Unknown COMMAND received: [{}]'.format(incomingCommand))
            client.publish('CIPO/' + puzzleName + '/STATE', puzzleState)

        #end if
    elif ('PONG' in message.topic):
        process_pong()
    #end if
#end def


def buildInterface():

    screen.clear()

    screen.addstr(0,0, '**************************************************')
    screen.addstr(1,0, '**     Simu-Puzzle for MQTT Ecosystem Demo      **')
    screen.addstr(2,0, '**    Joel Caturia <jcaturia@katratech.com>     **')
    screen.addstr(3,0, '**************************************************')
    screen.addstr(4,0, '*  MQTT BROKER   ->                              *')
    screen.addstr(5,0, '*  PUZZLE ID     ->                              *')
    screen.addstr(6,0, '*  ALWAYS ACTIVE ->                              *')
    screen.addstr(7,0, '**************************************************')
    screen.addstr(8,0, '*  HEARTBEAT: [  ]  *  PUZZLE STATE:             *')
    screen.addstr(9,0, '**************************************************')
    screen.addstr(10,0, '*  Press "s" to solve the puzzle                 *')
    screen.addstr(11,0, '*  Press "q" to quit Simu-Puzzle                 *')
    screen.addstr(12,0, '**************************************************')

    screen.addstr(4,21, '[{}]'.format(brokerIP) )
    screen.addstr(5,21, '[{}]'.format(puzzleName) )
    screen.addstr(6,21, '[{}]'.format(flagAlwaysActive) )

    screen.refresh()

#end def    


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds
#end def


def updatePuzzleState(newPuzzleState = None):
    global puzzleState

    if newPuzzleState is not None:
        puzzleState = newPuzzleState

    if puzzleState == 'AUTO':
        colorNumber = 1
    elif puzzleState == 'ACTIVE':
        colorNumber = 2
    elif puzzleState == 'SOLVED':
        colorNumber = 3
    #end if

    screen.addstr(8, 37, '[' + puzzleState + ']   ', curses.color_pair(colorNumber))
    screen.refresh()

    client.publish('CIPO/' + puzzleName + '/STATE', puzzleState)

#end def


#heartNumber = 0
#heartbeatIcons = ['/', '-', '\\', '|' ]

def process_pong():
    if pingPongFlash is True:
        screen.addstr(8, 16, 'K')

    else:
        screen.addstr(8, 16, 'k')
    #end if

    #screen.addstr(8, 16, 'K')
    screen.refresh()
#end def

pingPongFlash = True

def send_ping():
    #global heartNumber
    global pingPongFlash

    #screen.addstr(8, 15, heartbeatIcons[heartNumber])
    if pingPongFlash is True:
        screen.addstr(8, 15, 'O ')
        pingPongFlash = False

    else:
        pingPongFlash = True
        screen.addstr(8, 15, 'o ')
    #end if

    screen.refresh()

    #if heartNumber >= 3:
    #    heartNumber = 0
    #else:
    #    heartNumber += 1
    #end if

    data = {}
    data['timestamp'] = time.time()
    data['puzzleID'] = puzzleName
    data['ipAddress'] = '127.0.0.1'
    data['uptime'] = get_uptime()
    json_data = json.dumps(data)

    client.publish('CIPO/PING/' + puzzleName, json_data )

#end def




try:
    client = mqtt.Client()
    client.connect(brokerIP, brokerPort, 60)
    client.loop_start()

except:
    print('\r\nERROR: unable to communicate with MQTT broker. Exiting...')
#    curses.endwin()
    exit()

#end try


client.on_connect = on_connect
client.on_message = on_message


screen = curses.initscr()
screen.nodelay(1)
curses.curs_set(0)
curses.start_color()
curses.noecho()

curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)


buildInterface()
updatePuzzleState(None)

t = time.time()
send_ping()

try:
    while True:

        inChar = screen.getch() 
        if inChar == ord('q'):        # (q)uit
            curses.endwin()
            exit()

        elif inChar == ord('s'):      # (s)olve      
            updatePuzzleState('SOLVED')
        #end if 

        if time.time() - t > 2:        # send a controller ping every 10 seconds
            t=time.time()
            send_ping()
        #end if

        time.sleep(.1)

    #end while

except:
    curses.endwin()
#end try
