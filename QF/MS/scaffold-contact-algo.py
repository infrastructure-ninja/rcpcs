#!/usr/bin/python3

# Example Puzzle Controller :: Touchscreen Finger Pattern (Android Unlock Screen)
# Part of the RCPCS project (Room Control and Puzle Coordination System)
# Copyright (C) 2019  Joel D. Caturia
#
#
# This example code demonstrates how we bring together a puzzle controller
# class and the RCPCS communication controller class to provide bi-directional
# communications between the room controller and the physical puzzle.
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



# WHAT NEEDS TO HAPPEN:
#remember we're using GPIO.BCM in this project (at the moment)
# puzzle controller for two keys:
# (CONTROLLER TYPE: simultaneous activation of N inputs with a definable delay requirement)
#INPUT PINS ARE -> 8 and 25
#"PUZZLE ACTIVE" OUTPUT is -> 14

#(CONTROLLER TYPE: basic input and output. Not really any logic, but used for building larger systems)
#PATCH SOLVED INPUT -> pin 22
#PATCH SOLVED INDICATOR OUTPUT -> DOESN'T EXIST

#FUEL SOLVED INPUT -> pin 7
#FUEL SOLVED INDICATOR OUTPUT -> 6

#PRESSURE SOLVED INPUT -> pin 17
#PRESSURE SOLVED INDICATOR OUTPUT -> 21

#POWER SOLVED INPUT -> pin 27
#POWER SOLVED INDICATOR OUTPUT -> 5


import RPi.GPIO as GPIO
import os
import time

#from class_puzzle_contact_and import ANDMatchPuzzleContacts as ANDMatchPuzzleContactClass
from class_puzzle_contact_algo import AlgoMatchPuzzleContacts as AlgoMatchPuzzleContactClass
from controller_communications import ControllerCommunications

#FIXME - let's move this to a config file and/or command-line arguments someday
MQTTserver = '192.168.200.138'
DebugFlag  = True
#DebugFlag = False

######################################
## PUZZLE CONTROLLER -> FUEL PUZZLE ##
######################################
def handlerFuelPuzzleReset():
  print('PUBLISH -> PUZZLE WAS RESET')
#  FuelRoomController.PublishStatus('RESET')

#  time.sleep(2)
#  FuelPuzzle.Activate()
#end def

def handlerFuelPuzzleActivated():
  print('PUBLISH -> PUZZLE WAS ACTIVATED')
#  FuelRoomController.PublishStatus('ACTIVE')
#end def

def handlerFuelPuzzleSolved():
  print('PUBLISH -> PUZZLE WAS SOLVED')
  time.sleep(4)
  FuelPuzzle.Reset()
#  FuelRoomController.PublishStatus('SOLVED')
#end def

def handlerFuelPuzzleFailed():
  print('PUBLISH -> PUZZLE WAS FAILED')
  time.sleep(2)
  FuelPuzzle.Reset()
#  FuelRoomController.PublishStatus('FAILED')
#end def

#FuelPuzzle = ANDMatchPuzzleContactClass(Debug = DebugFlag, AlwaysActive=False)
FuelPuzzle = AlgoMatchPuzzleContactClass(Debug = DebugFlag, AlwaysActive = True)


#FuelPuzzle.SetAlgorithmInputs( [17,  27, 5, 6] )
FuelPuzzle.SetAlgorithmInputs( [17, 27, 5], FailPin = 6 )

FuelPuzzle.SetAlgorithmOutputs( [13, 19, 26, 20] )


#FuelPuzzle.AddFailedOutput(21)
FuelPuzzle.AddSolvedOutput(24)
FuelPuzzle.AddActiveOutput(23)

FuelPuzzle.RegisterCallback('activated', handlerFuelPuzzleActivated)
FuelPuzzle.RegisterCallback('solved',    handlerFuelPuzzleSolved)
FuelPuzzle.RegisterCallback('reset',     handlerFuelPuzzleReset)
FuelPuzzle.RegisterCallback('failed',    handlerFuelPuzzleFailed)
#####################################################
## (END) PUZZLE CONTROLLER -> FUEL PUZZLE ##
#####################################################

###############################################
## ROOM CONTROL COMMUNICATION -> FUEL PUZZLE ##
###############################################
def handlerFuelRoomControllerReboot():
  print('>> Processing a remote reboot command!')
  #os.system('sudo reboot')
#end def

def handlerFuelRoomControllerReset():
  FuelPuzzle.Reset()
#end def

def handlerFuelRoomControllerActivate():
  FuelPuzzle.Activate()
#end def

def handlerFuelRoomControllerSolve():
  FuelPuzzle.Solve()
#end def

def handlerFuelRoomControllerPing():
  pass
#end def

def handlerFuelRoomControllerPong():
  pass
#end def

FuelRoomController = ControllerCommunications('fuel', MQTTserver)

#FuelRoomController.RegisterCallback('command_reboot', handlerFuelRoomControllerReboot)
#FuelRoomController.RegisterCallback('command_reset', handlerFuelRoomControllerReset)
#FuelRoomController.RegisterCallback('command_activate', handlerFuelRoomControllerActivate)
#FuelRoomController.RegisterCallback('command_solve', handlerFuelRoomControllerSolve)
#FuelRoomController.RegisterCallback('ping', handlerFuelRoomControllerPing)
#FuelRoomController.RegisterCallback('pong', handlerFuelRoomControllerPong)
#####################################################
## (END) ROOM CONTROL COMMUNICATION -> FUEL PUZZLE ##
#####################################################




##################################################
####### MAIN PROGRAM EXECUTION BEGINS HERE #######
##################################################

try:

  FuelPuzzle.Reset()
  
  time.sleep(4)

  while True:
    FuelPuzzle.ProcessEvents()

#    FuelRoomController.ProcessEvents()
  #end while
  
except (KeyboardInterrupt, SystemExit):

  print("\r\nExiting..")
  quit()

except:
  #GPIO.cleanup()
  raise

#end try