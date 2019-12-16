#!/usr/bin/python3

# Example Puzzle Controller :: Touchscreen Finger Pattern (Android Unlock Screen)
# Part of the RCPCS project (Room Control and Puzle Coordination System)
# Copyright (C) 2019  Joel D. Caturia
# <based on portions of code presumed to be in the public domain>
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


import RPi.GPIO as GPIO
import os
import time

from puzzle_controller import PuzzleClass as PuzzleClass
from controller_communications import ControllerCommunications

chan_list = [11, 13]
resetPin = 15
heartbeatPin = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


GPIO.setup(heartbeatPin, GPIO.OUT)
GPIO.output(heartbeatPin, GPIO.LOW)

GPIO.setup(chan_list, GPIO.OUT)
GPIO.output(chan_list, GPIO.LOW)
GPIO.setup(resetPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 


puzzle = PuzzleClass(DebugMode = False)

def handlerPuzzleFailed():
  roomController.PublishStatus('FAILED')
#end def

def handlerPuzzleSolved():
  roomController.PublishStatus('SOLVED')

  # What the heck is this for?
  # Need to look at the way the puzzle is physically built to be able to tell
  pin_st = GPIO.input(chan_list[0])
  pin_st = int(not pin_st)
  GPIO.output(chan_list[0], pin_st)

  # Activate our relay/unlock our maglock!
  GPIO.output(chan_list[1], GPIO.HIGH)
#end def

def handlerPuzzleReset():
  roomController.PublishStatus('ACTIVE')
  GPIO.output(chan_list, GPIO.LOW)
#end def

puzzle.RegisterCallback('fail', handlerPuzzleFailed)
puzzle.RegisterCallback('solve', handlerPuzzleSolved)
puzzle.RegisterCallback('reset', handlerPuzzleReset)



roomController = ControllerCommunications('reactor', '192.168.200.138')

def handlerRoomControllerReboot():
  print('>> Processing a remote reboot command!')
#  time.sleep(3)
  os.system('sudo reboot')
#end def

def handlerRoomControllerReset():
  puzzle.reset()
#end def

def handlerRoomControllerSolve():
  puzzle.solve()
#end def


def handlerRoomControllerPing():
  GPIO.output(heartbeatPin, GPIO.HIGH)
#end def

def handlerRoomControllerPong():
  GPIO.output(heartbeatPin, GPIO.LOW)
#end def


roomController.RegisterCallback('command_reboot', handlerRoomControllerReboot)
roomController.RegisterCallback('command_reset', handlerRoomControllerReset)
roomController.RegisterCallback('command_activate', handlerRoomControllerReset)
roomController.RegisterCallback('command_solve', handlerRoomControllerSolve)
roomController.RegisterCallback('ping', handlerRoomControllerPing)
roomController.RegisterCallback('pong', handlerRoomControllerPong)


def handlerResetButton(channel):
  puzzle.reset()
#end def

GPIO.add_event_detect(resetPin, GPIO.FALLING, callback=handlerResetButton)

try:

  puzzle.reset()

  while True:
    puzzle.ProcessEvents()
    roomController.ProcessEvents()
  #end while
  
except (KeyboardInterrupt, SystemExit):
  GPIO.cleanup()
  print("Exiting..")
  quit()

except:
  GPIO.cleanup()
  raise

#end try
