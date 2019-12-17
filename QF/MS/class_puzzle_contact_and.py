#!/usr/bin/python3

# Puzzle Controller Class :: NFC Algorithmic Solve
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

import RPi.GPIO as GPIO


class ANDMatchPuzzleContacts:

    def __init__(self, Debug = False, AlwaysActive = False):
    
        self.__contactBounceTime = 300

        self.__debugFlag = Debug
        self.__delayAllowance  = 0      # How much time is allowed to elapse (in milliseconds) between the different contact closures
        self.__callbacks       = {}        
        self.__puzzleInputPins = []
        self.__puzzleActiveOutputPins = []   #FIXME: I'm not letting you define these as active LO - shame on me
        self.__puzzleSolvedOutputPins = []   #FIXME: I'm not letting you define these as active LO - shame on me
        
        self.__puzzleAlwaysActive     = AlwaysActive
        self.__puzzleActive           = AlwaysActive
        self.__puzzleSolved           = False


        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    #end def
    

    def SetDelay(self, delay = 0):
        self.__delayAllowance = delay
    #end def (SetDelay)

    
    def AddActiveOutput(self, activeOutputPinNumber):
        if self.__debugFlag is True:
            print('>> Added Puzzle Active Output Pin #[{}]'.format(activeOutputPinNumber))
        #end if

        GPIO.setup(activeOutputPinNumber, GPIO.OUT)
        GPIO.output(activeOutputPinNumber, GPIO.HIGH)
        self.__puzzleActiveOutputPins.append(activeOutputPinNumber)
    #end def (AddActiveOutput)


    def AddSolvedOutput(self, solvedOutputPinNumber):
        if self.__debugFlag is True:
            print('>> Added Puzzle Solved Output Pin #[{}]'.format(solvedOutputPinNumber))
        #end if

        GPIO.setup(solvedOutputPinNumber, GPIO.OUT)
        GPIO.output(solvedOutputPinNumber, GPIO.HIGH)
        self.__puzzleSolvedOutputPins.append(solvedOutputPinNumber)
    #end def (AddActiveOutput)


    def AddContact(self, inputContactPinNumber):
        if self.__debugFlag is True:
            print('>> Added Input Contact Pin #[{}]'.format(inputContactPinNumber))
        #end if

        self.__puzzleInputPins.append(inputContactPinNumber)

        GPIO.setup(inputContactPinNumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(inputContactPinNumber, GPIO.RISING, callback=self.__handlerContactCallback, bouncetime=self.__contactBounceTime)
    #end def (AddContact)


    def __handlerContactCallback(self, channel):
        # We don't want to process any more events when we're in a solved state
        if ( self.__puzzleActive is True ) and ( self.__puzzleSolved is False ):
            print('OOH! GOT A THING! -> [CHANNEL: {}, STATE: {}]'.format(channel, GPIO.input(channel) ))        
            self.__checkForSolve()
    #end def (__handlerContactCallback)
    

    def __checkForSolve(self):
        #FIXME - we'll add the delay stuff later, let's just make normal AND work first
        # I would also point out that this is hard-coded for ACTIVE-HIGH inputs at the moment ..

        for pinToCheck in self.__puzzleInputPins:
            tmpInput = GPIO.input(pinToCheck)
            if tmpInput != GPIO.HIGH:
                print('NOPE')
                return False
            #end if
        #end for

        # If we get down to here, we're presuming that we are indeed solved.
        self.Solve()

    #end def (__checkForSolve)

    
    def RegisterCallback(self, callback, callbackFunction):
        self.__callbacks[callback] = callbackFunction
    #end def (RegisterCallbacks)


    def Activate(self):
        
        if self.__debugFlag is True:
            print('>> PUZZLE ACTIVATED')
        #end if

        self.__puzzleActive = True

        for individualOutput in self.__puzzleActiveOutputPins:
            GPIO.output(individualOutput, GPIO.LOW)
        #end for

        try:
            self.__callbacks['activated']()
        except:
            pass
        #end try
    #end def (Solve)


    def Solve(self):
        
        if self.__debugFlag is True:
            print('>> PUZZLE SOLVED!')
        #end if

        self.__puzzleSolved = True

        for individualOutput in self.__puzzleSolvedOutputPins:
            GPIO.output(individualOutput, GPIO.LOW)
        #end for

        try:
            self.__callbacks['solved']()
        except:
            pass
        #end try
    #end def (Solve)


    def Reset(self):
        
        if self.__debugFlag is True:
            print('>> PUZZLE RESET')
        #end if

        self.__puzzleSolved = False
        
        for individualOutput in self.__puzzleActiveOutputPins:
            GPIO.output(individualOutput, GPIO.HIGH)
        #end for

        for individualOutput in self.__puzzleSolvedOutputPins:
            GPIO.output(individualOutput, GPIO.HIGH)
        #end for

        try:
            self.__callbacks['reset']()
        except:
            pass
        #end try

        if self.__puzzleAlwaysActive is True:
            self.Activate()
        else:
            self.__puzzleActive = False
        #end if

    #end def (Reset)


    def ProcessEvents(self):
        pass
    #end def (ProcessEvents)
    
        
    def Cleanup(self):
        GPIO.cleanup()
    #end def (Cleanup)


    def GetPuzzleSolved(self):
        return self.__puzzleSolved
    #end def (GetPuzzleSolved)

#end class
