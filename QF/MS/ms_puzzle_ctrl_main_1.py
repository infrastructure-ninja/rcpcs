#!/usr/bin/python3

# Amalgum Puzzle Controller :: Demonstrates multiple puzzle classes and room communication happening in one file
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


#import RPi.GPIO as GPIO
import os
import time

from class_puzzle_contact_and import ANDMatchPuzzleContacts as ANDMatchPuzzleContactClass
from controller_communications import ControllerCommunications

#FIXME - let's move this to a config file and/or command-line arguments someday
#MQTTserver = '192.168.1.220'
MQTTserver = '192.168.200.138'
DebugFlag  = True

######################################
## PUZZLE CONTROLLER -> FUEL PUZZLE ##
######################################
def handlerFuelPuzzleReset():
  FuelRoomController.PublishStatus('RESET')
#end def

def handlerFuelPuzzleActivated():
  FuelRoomController.PublishStatus('ACTIVE')
#end def

def handlerFuelPuzzleSolved():
  FuelRoomController.PublishStatus('SOLVED')
#end def

FuelPuzzle = ANDMatchPuzzleContactClass(Debug = DebugFlag, AlwaysActive = True)
FuelPuzzle.AddContact(7)
FuelPuzzle.AddSolvedOutput(6)

FuelPuzzle.RegisterCallback('activated', handlerFuelPuzzleActivated)
FuelPuzzle.RegisterCallback('solved',    handlerFuelPuzzleSolved)
FuelPuzzle.RegisterCallback('reset',     handlerFuelPuzzleReset)
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

FuelRoomController.RegisterCallback('command_reboot',   handlerFuelRoomControllerReboot)
FuelRoomController.RegisterCallback('command_reset',    handlerFuelRoomControllerReset)
FuelRoomController.RegisterCallback('command_activate', handlerFuelRoomControllerActivate)
FuelRoomController.RegisterCallback('command_solve',    handlerFuelRoomControllerSolve)
FuelRoomController.RegisterCallback('ping',             handlerFuelRoomControllerPing)
FuelRoomController.RegisterCallback('pong',             handlerFuelRoomControllerPong)
#####################################################
## (END) ROOM CONTROL COMMUNICATION -> FUEL PUZZLE ##
#####################################################





######################################
## PUZZLE CONTROLLER -> POWER PUZZLE ##
######################################
def handlerPowerPuzzleReset():
  PowerRoomController.PublishStatus('RESET')
#end def

def handlerPowerPuzzleActivated():
  PowerRoomController.PublishStatus('ACTIVE')
#end def

def handlerPowerPuzzleSolved():
  PowerRoomController.PublishStatus('SOLVED')
#end def

PowerPuzzle = ANDMatchPuzzleContactClass(Debug = DebugFlag, AlwaysActive = True)
PowerPuzzle.AddContact(27)
PowerPuzzle.AddSolvedOutput(5)

PowerPuzzle.RegisterCallback('activated', handlerPowerPuzzleActivated)
PowerPuzzle.RegisterCallback('solved',    handlerPowerPuzzleSolved)
PowerPuzzle.RegisterCallback('reset',     handlerPowerPuzzleReset)
#####################################################
## (END) PUZZLE CONTROLLER -> POWER PUZZLE ##
#####################################################

###############################################
## ROOM CONTROL COMMUNICATION -> POWER PUZZLE ##
###############################################
def handlerPowerRoomControllerReboot():
  print('>> Processing a remote reboot command!')
  #os.system('sudo reboot')
#end def

def handlerPowerRoomControllerReset():
  PowerPuzzle.Reset()
#end def

def handlerPowerRoomControllerActivate():
  PowerPuzzle.Activate()
#end def

def handlerPowerRoomControllerSolve():
  PowerPuzzle.Solve()
#end def

def handlerPowerRoomControllerPing():
  pass
#end def

def handlerPowerRoomControllerPong():
  pass
#end def

PowerRoomController = ControllerCommunications('power', MQTTserver)

PowerRoomController.RegisterCallback('command_reboot',   handlerPowerRoomControllerReboot)
PowerRoomController.RegisterCallback('command_reset',    handlerPowerRoomControllerReset)
PowerRoomController.RegisterCallback('command_activate', handlerPowerRoomControllerActivate)
PowerRoomController.RegisterCallback('command_solve',    handlerPowerRoomControllerSolve)
PowerRoomController.RegisterCallback('ping',             handlerPowerRoomControllerPing)
PowerRoomController.RegisterCallback('pong',             handlerPowerRoomControllerPong)
#####################################################
## (END) ROOM CONTROL COMMUNICATION -> POWER PUZZLE ##
#####################################################





##########################################
## PUZZLE CONTROLLER -> PRESSURE PUZZLE ##
##########################################
def handlerPressurePuzzleReset():
  PressureRoomController.PublishStatus('RESET')
#end def

def handlerPressurePuzzleActivated():
  PressureRoomController.PublishStatus('ACTIVE')
#end def

def handlerPressurePuzzleSolved():
  PressureRoomController.PublishStatus('SOLVED')
#end def

PressurePuzzle = ANDMatchPuzzleContactClass(Debug = DebugFlag, AlwaysActive = True)
PressurePuzzle.AddContact(17)
#PressurePuzzle.AddSolvedOutput(21)

PressurePuzzle.RegisterCallback('activated', handlerPressurePuzzleActivated)
PressurePuzzle.RegisterCallback('solved',    handlerPressurePuzzleSolved)
PressurePuzzle.RegisterCallback('reset',     handlerPressurePuzzleReset)
################################################
## (END) PUZZLE CONTROLLER -> PRESSURE PUZZLE ##
################################################

###################################################
## ROOM CONTROL COMMUNICATION -> PRESSURE PUZZLE ##
###################################################
def handlerPressureRoomControllerReboot():
  print('>> Processing a remote reboot command!')
  #os.system('sudo reboot')
#end def

def handlerPressureRoomControllerReset():
  PressurePuzzle.Reset()
#end def

def handlerPressureRoomControllerActivate():
  PressurePuzzle.Activate()
#end def

def handlerPressureRoomControllerSolve():
  PressurePuzzle.Solve()
#end def

def handlerPressureRoomControllerPing():
  pass
#end def

def handlerPressureRoomControllerPong():
  pass
#end def

PressureRoomController = ControllerCommunications('pressure', MQTTserver)

PressureRoomController.RegisterCallback('command_reboot',   handlerPressureRoomControllerReboot)
PressureRoomController.RegisterCallback('command_reset',    handlerPressureRoomControllerReset)
PressureRoomController.RegisterCallback('command_activate', handlerPressureRoomControllerActivate)
PressureRoomController.RegisterCallback('command_solve',    handlerPressureRoomControllerSolve)
PressureRoomController.RegisterCallback('ping',             handlerPressureRoomControllerPing)
PressureRoomController.RegisterCallback('pong',             handlerPressureRoomControllerPong)
#########################################################
## (END) ROOM CONTROL COMMUNICATION -> PRESSURE PUZZLE ##
#########################################################





######################################
## PUZZLE CONTROLLER -> PATCH PUZZLE ##
######################################
def handlerPatchPuzzleReset():
  PatchRoomController.PublishStatus('RESET')
#end def

def handlerPatchPuzzleActivated():
  PatchRoomController.PublishStatus('ACTIVE')
#end def

def handlerPatchPuzzleSolved():
  PatchRoomController.PublishStatus('SOLVED')
#end def

PatchPuzzle = ANDMatchPuzzleContactClass(Debug = DebugFlag, AlwaysActive = True)
PatchPuzzle.AddContact(22)
#PatchPuzzle.AddActiveOutput()
#PatchPuzzle.AddSolvedOutput()

PatchPuzzle.RegisterCallback('activated', handlerPatchPuzzleActivated)
PatchPuzzle.RegisterCallback('solved',    handlerPatchPuzzleSolved)
PatchPuzzle.RegisterCallback('reset',     handlerPatchPuzzleReset)
#####################################################
## (END) PUZZLE CONTROLLER -> PATCH PUZZLE ##
#####################################################

###############################################
## ROOM CONTROL COMMUNICATION -> PATCH PUZZLE ##
###############################################
def handlerPatchRoomControllerReboot():
  print('>> Processing a remote reboot command!')
  #os.system('sudo reboot')
#end def

def handlerPatchRoomControllerReset():
  PatchPuzzle.Reset()
#end def

def handlerPatchRoomControllerActivate():
  PatchPuzzle.Activate()
#end def

def handlerPatchRoomControllerSolve():
  PatchPuzzle.Solve()
#end def

def handlerPatchRoomControllerPing():
  pass
#end def

def handlerPatchRoomControllerPong():
  pass
#end def

PatchRoomController = ControllerCommunications('patch', MQTTserver)

PatchRoomController.RegisterCallback('command_reboot',   handlerPatchRoomControllerReboot)
PatchRoomController.RegisterCallback('command_reset',    handlerPatchRoomControllerReset)
PatchRoomController.RegisterCallback('command_activate', handlerPatchRoomControllerActivate)
PatchRoomController.RegisterCallback('command_solve',    handlerPatchRoomControllerSolve)
PatchRoomController.RegisterCallback('ping',             handlerPatchRoomControllerPing)
PatchRoomController.RegisterCallback('pong',             handlerPatchRoomControllerPong)
#####################################################
## (END) ROOM CONTROL COMMUNICATION -> PATCH PUZZLE ##
#####################################################





######################################
## PUZZLE CONTROLLER -> KEYS PUZZLE ##
######################################
def handlerKeysPuzzleReset():
  KeysRoomController.PublishStatus('RESET')
#end def

def handlerKeysPuzzleActivated():
  KeysRoomController.PublishStatus('ACTIVE')
#end def

def handlerKeysPuzzleSolved():
  KeysRoomController.PublishStatus('SOLVED')
#end def

KeysPuzzle = ANDMatchPuzzleContactClass(Debug = DebugFlag, AlwaysActive = False)
KeysPuzzle.AddContact(8)
#KeysPuzzle.AddContact(25)   #FIXME - Add this when we're ready for the full puzzle

KeysPuzzle.AddActiveOutput(14)
KeysPuzzle.SetDelay(2000)

KeysPuzzle.RegisterCallback('activated', handlerKeysPuzzleActivated)
KeysPuzzle.RegisterCallback('solved',    handlerKeysPuzzleSolved)
KeysPuzzle.RegisterCallback('reset',     handlerKeysPuzzleReset)
#####################################################
## (END) PUZZLE CONTROLLER -> KEYS PUZZLE ##
#####################################################

###############################################
## ROOM CONTROL COMMUNICATION -> KEYS PUZZLE ##
###############################################
def handlerKeysRoomControllerReboot():
  print('>> Processing a remote reboot command!')
  #os.system('sudo reboot')
#end def

def handlerKeysRoomControllerReset():
  KeysPuzzle.Reset()
#end def

def handlerKeysRoomControllerActivate():
  KeysPuzzle.Activate()
#end def

def handlerKeysRoomControllerSolve():
  KeysPuzzle.Solve()
#end def

def handlerKeysRoomControllerPing():
  pass
#end def

def handlerKeysRoomControllerPong():
  pass
#end def

KeysRoomController = ControllerCommunications('keys', MQTTserver)

KeysRoomController.RegisterCallback('command_reboot',   handlerKeysRoomControllerReboot)
KeysRoomController.RegisterCallback('command_reset',    handlerKeysRoomControllerReset)
KeysRoomController.RegisterCallback('command_activate', handlerKeysRoomControllerActivate)
KeysRoomController.RegisterCallback('command_solve',    handlerKeysRoomControllerSolve)
KeysRoomController.RegisterCallback('ping',             handlerKeysRoomControllerPing)
KeysRoomController.RegisterCallback('pong',             handlerKeysRoomControllerPong)
#####################################################
## (END) ROOM CONTROL COMMUNICATION -> KEYS PUZZLE ##
#####################################################





##################################################
####### MAIN PROGRAM EXECUTION BEGINS HERE #######
##################################################

try:

  FuelPuzzle.Reset()
  PowerPuzzle.Reset()
  PressurePuzzle.Reset()
  PatchPuzzle.Reset()
  KeysPuzzle.Reset()


  while True:
    FuelPuzzle.ProcessEvents()
    PowerPuzzle.ProcessEvents()
    PressurePuzzle.ProcessEvents()
    PatchPuzzle.ProcessEvents()
    KeysPuzzle.ProcessEvents()

    FuelRoomController.ProcessEvents()
    PowerRoomController.ProcessEvents()
    PressureRoomController.ProcessEvents()
    PatchRoomController.ProcessEvents()
    KeysRoomController.ProcessEvents()
  #end while
  
except (KeyboardInterrupt, SystemExit):
  print("\r\nExiting..")
  quit()

except:
  raise

#end try