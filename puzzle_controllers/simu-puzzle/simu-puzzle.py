#!/usr/bin/python3


# SIMU-PUZZLE Tool (Puzzle Protocol Simulation Tool)
# Part of the RCPCS project (Room Control and Puzle Coordination System)
# Copyright (C) 2019  Joel D. Caturia
#
#
# Required positional arguments: 
#  * MQTT host
#  * Puzzle ID
#
# Optional parameter(s):
#  * --always-active  ::  Always active (does not require activation phase)
#
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
#  - paho-mqtt-client
#  $> sudo pip3 install paho-mqtt


import argparse
import paho.mqtt.client as mqtt
import time
import json
import curses
from   curses import wrapper


__platform__ = 'Simu-Puzzle'
__version__  = '0.9'


parser = argparse.ArgumentParser(description='Simulate a puzzle in the RCPCS ecosystem.')

parser.add_argument('mqttHost', metavar='<MQTT BROKER>', help='The IP/hostname of the MQTT broker to connect to.')
parser.add_argument('puzzleID', metavar='<PUZZLE ID>', help='The ID of the puzzle to simulate. Will be used in all other places to reference this puzzle controller.')
parser.add_argument('--always-active', action='store_true', dest='alwaysActive', help='Puzzle will always be in active state (and will skip the AUTO state).')
#parser.add_argument('--fail-enabled', action='store_true', dest='failEnabled', help='Puzzle will interpret an incoming FAIL command, and a FAIL state can be generally localled via the keyboard.')
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

        if incomingCommand in ['RESET', 'ACTIVATE', 'SOLVE', 'REBOOT']:

            if incomingCommand == 'RESET':
                updatePuzzleState('AUTO')
                            
            elif incomingCommand == 'ACTIVATE':
                updatePuzzleState('ACTIVE')

            elif incomingCommand == 'SOLVE':
                updatePuzzleState('SOLVED')

            elif incomingCommand == 'REBOOT':
                updatePuzzleState('REBOOTING')
            
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

    screen.addstr(0,0,  '**************************************************')
    screen.addstr(1,0,  '**   Simu-Puzzle for RCPCS ecosystem v{}'.format(__version__))
    screen.addstr(1,48, '**')

    screen.addstr(2,0,  '**   by Joel Caturia <jcaturia@katratech.com>   **')
    screen.addstr(3,0,  '**************************************************')
    screen.addstr(4,0,  '*  MQTT BROKER   ->                              *')
    screen.addstr(5,0,  '*  PUZZLE ID     ->                              *')
    screen.addstr(6,0,  '*  ALWAYS ACTIVE ->                              *')
    screen.addstr(7,0,  '**************************************************')
    screen.addstr(8,0,  '* HEARTBEAT: [  ] * PUZZLE STATE:                *')
    screen.addstr(9,0,  '**************************************************')
    screen.addstr(10,0, '* COMMANDS:                                      *')
    screen.addstr(11,0, '*  - "r" to RESET the puzzle                     *')
    screen.addstr(12,0, '*  - "a" to ACTIVATE the puzzle                  *')
    screen.addstr(13,0, '*  - "f" to FAIL the puzzle                      *') 
    screen.addstr(14,0, '*  - "s" to SOLVE the puzzle                     *')
    screen.addstr(15,0, '*  - "z" to REBOOT the puzzle                    *')  
    screen.addstr(16,0, '*  - "q" to QUIT Simu-Puzzle                     *')
    screen.addstr(17,0, '**************************************************')

    screen.addstr(4,21, '[{}]'.format(brokerIP) )
    screen.addstr(5,21, '[{}]'.format(puzzleName) )
    screen.addstr(6,21, '[{}]'.format(flagAlwaysActive) )

    screen.refresh()

#end def    




def updatePuzzleState(newPuzzleState = None):
    global puzzleState

    if newPuzzleState is not None:
        if (flagAlwaysActive is True) and newPuzzleState == 'AUTO':
            puzzleState = 'ACTIVE'
        else:
            puzzleState = newPuzzleState
        #end if

    if puzzleState == 'AUTO':
        colorNumber = 1

    elif puzzleState == 'ACTIVE':
        colorNumber = 2

    elif puzzleState == 'SOLVED':
        colorNumber = 3

    elif puzzleState == 'FAILED':
        colorNumber = 4
    
    elif puzzleState == 'REBOOTING':
        colorNumber = 5
    #end if

    screen.addstr(8, 34, ' ' * 15, curses.color_pair(colorNumber) )
    screen.addstr(8, 34, '[' + puzzleState + ']   ', curses.color_pair(colorNumber) )
    screen.refresh()

    client.publish('CIPO/' + puzzleName + '/STATE', puzzleState)

    if puzzleState == 'REBOOTING':
        SimulateReboot()
        updatePuzzleState('AUTO')
    #end if

#end def

def SimulateReboot():

    # I admit this is a pretty clumsy way of doing this, but remember that when a puzzle controller reboots in the real world
    # it becomes totally unresponsible and unreachable. Seems like we are adequately simulating that here?
    # We even stop processing heartbeats coming in from the MQTT subscription! :P
    for x in range (300, 0, -1):
        pass

    for x in range (30, 0, -1):
        screen.addstr(8, 46, '{0:02d}'.format(x), curses.color_pair(2) )

        screen.addstr(8, 48, '/', curses.color_pair(2) )
        screen.refresh()
        time.sleep(.15)

        screen.addstr(8, 48, '-', curses.color_pair(2) )
        screen.refresh()
        time.sleep(.15)

        screen.addstr(8, 48, '\\', curses.color_pair(2) )
        screen.refresh()
        time.sleep(.15)
        
        screen.addstr(8, 48, '|', curses.color_pair(2) )
        screen.refresh()
        time.sleep(.15)

    #end for

#end def (SimulateReboot)


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds
#end def


def process_pong():
    if pingPongFlash is True:
        screen.addstr(8, 15, 'K')

    else:
        screen.addstr(8, 15, 'k')
    #end if

    screen.refresh()
#end def


pingPongFlash = True

def send_ping():
    global pingPongFlash

    if pingPongFlash is True:
        screen.addstr(8, 14, 'O ')
        pingPongFlash = False

    else:
        pingPongFlash = True
        screen.addstr(8, 14, 'o ')
    #end if

    screen.refresh()

    data = {}
    data['timestamp']    = time.time()
    data['puzzleID']     = puzzleName
    data['ipAddress']    = '127.0.0.1'
    data['uptime']       = get_uptime()
    data['platform']     = __platform__ + ' v' + __version__
    data['role']         = 'puzzle'
    data['temperature']  = 'n/a'
    data['currentState'] = puzzleState
    json_data = json.dumps(data)

    client.publish('CIPO/PING/' + puzzleName, json_data )

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


screen = curses.initscr()
screen.nodelay(1)
curses.curs_set(0)
curses.start_color()
curses.noecho()

curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


buildInterface()
updatePuzzleState(None)

t = time.time()
send_ping()

try:
    while True:

        inChar = screen.getch()

        if inChar > 0:
            menuSelection = chr(inChar)

            if  menuSelection in ['q', 'Q']:  # (q)uit
                curses.endwin()
                print('Simu-Puzzle terminating normally..\r\n')
                exit()

            elif menuSelection in ['a', 'A']: # (a)ctivate      
                updatePuzzleState('ACTIVE')

            elif menuSelection in ['r', 'R']: # (r)eset      
                updatePuzzleState('AUTO')

            elif menuSelection in ['f', 'F']: # (f)ailed      
                updatePuzzleState('FAILED')

            elif menuSelection in ['s', 'S']: # (s)olve      
                updatePuzzleState('SOLVED')

            elif menuSelection in ['z', 'Z']: # (s)olve      
                updatePuzzleState('REBOOTING')
            #end if 

        #end if


        if time.time() - t > 5:        # send a controller ping every 10 seconds
            t = time.time()
            send_ping()
        #end if

        time.sleep(.2)

    #end while

except KeyboardInterrupt:
    curses.endwin()
    print('\r\nCTRL+C detected, exiting..\r\n')

except Exception as e:
    curses.endwin()
    print(e)

finally:
    pass
#end try
