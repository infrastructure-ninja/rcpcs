#!/usr/bin/python3

# Puzzle Controller Class :: Algorithmic Contact Match
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
#  - gpiozero (It is very commonlyinstalled by default)
#  $> sudo pip3 install gpiozero


# TODO:
#  * Fix the places where I did not let you specify active LO/HI for inputs and outputs
#  * Add a failed state: contacts, callback, and an output, with an optional timer for reset



import gpiozero
import time

class AlgoMatchPuzzleContacts:

    def __init__(self, Debug = False, AlwaysActive = False):
    
        self.__debugFlag       = Debug
#        self.__delayAllowance  = DelayAllowance      # How much time is allowed to elapse (in milliseconds) between the different contact closures
        self.__callbacks       = {}        

        self.__puzzleInputPinObjects     = []   #FIXME: I need to let you define these as active LO/HI        
        self.__puzzleOutputPinObjects	 = []

        self.__puzzleActiveOutputObjects = []   #FIXME: I need to let you define these as active LO/HI
        self.__puzzleSolvedOutputObjects = []   #FIXME: I need to let you define these as active LO/HI
        self.__puzzleFailedOutputObjects = []
        
        self.__puzzlePatternPosition     = 0
        self.__puzzleAlwaysActive        = AlwaysActive
        self.__puzzleActive              = AlwaysActive
        self.__puzzleSolved              = False
        self.__puzzleFailed		 = False
        
    #end def
    
    
    def SetAlgorithmInputs(self, inputPins, FailPin = None):
    
        if self.__debugFlag is True:
            print('>> Added Puzzle Pattern Inputs #[{}], Fail Pin: [{}]'.format(inputPins, FailPin))
        #end if
    
        self.__puzzleInputPinObjects.clear()
        
        for individualPin in inputPins:
            tmpButtonObject = gpiozero.Button(individualPin, pull_up=True, active_state=None)   #FIXME - this is where we fix active HI/LO
            tmpButtonObject.when_pressed  = self.__handlerContactCallback 

            self.__puzzleInputPinObjects.append(tmpButtonObject)
        #end for

        if FailPin is not None:
            tmpButtonObject = gpiozero.Button(FailPin, pull_up=True, active_state=None)   #FIXME - this is where we fix active HI/LO
            tmpButtonObject.when_pressed  = self.__handlerContactCallback 
        #end if
                    
    #end def (SetAlgorithmInputs)

    
    def SetAlgorithmOutputs(self, outputPins):
        if self.__debugFlag is True:
            print('>> Added Puzzle Pattern Outputs #[{}]'.format(outputPins))
        #end if

        self.__puzzleOutputPinObjects.clear()
            
        for individualOutput in outputPins:
            tmpOutputObject = gpiozero.PWMLED(individualOutput)
            tmpOutputObject.off()
            
            self.__puzzleOutputPinObjects.append(tmpOutputObject)
        #end for
    
    #end def (SetAlgorithmOutputs)
    
    
    
    def AddActiveOutput(self, activeOutputPinNumber):
        if self.__debugFlag is True:
            print('>> Added Puzzle Active Output Pin #[{}]'.format(activeOutputPinNumber))
        #end if
        
#        tmpOutputObject = gpiozero.LED(activeOutputPinNumber)	#FIXME - this is where we'll add stuff about active HI/LO
        tmpOutputObject = gpiozero.PWMLED(activeOutputPinNumber)	#FIXME - this is where we'll add stuff about active HI/LO
        tmpOutputObject.off()
        self.__puzzleActiveOutputObjects.append(tmpOutputObject)
    #end def (AddActiveOutput)


    def AddSolvedOutput(self, solvedOutputPinNumber):
        if self.__debugFlag is True:
            print('>> Added Puzzle Solved Output Pin #[{}]'.format(solvedOutputPinNumber))
        #end if

        #tmpOutputObject = gpiozero.LED(solvedOutputPinNumber)	#FIXME - this is where we'll add stuff about active HI/LO
        tmpOutputObject = gpiozero.PWMLED(solvedOutputPinNumber)	#FIXME - this is where we'll add stuff about active HI/LO
        tmpOutputObject.off()
        self.__puzzleSolvedOutputObjects.append(tmpOutputObject)
    #end def (AddActiveOutput)


    def AddFailedOutput(self, activeOutputPinNumber):
        if self.__debugFlag is True:
            print('>> Added Puzzle Failed Output Pin #[{}]'.format(activeOutputPinNumber))
        #end if
        
#        tmpOutputObject = gpiozero.LED(activeOutputPinNumber)	#FIXME - this is where we'll add stuff about active HI/LO
        tmpOutputObject = gpiozero.PWMLED(activeOutputPinNumber)	#FIXME - this is where we'll add stuff about active HI/LO
        tmpOutputObject.off()
        self.__puzzleFailedOutputObjects.append(tmpOutputObject)
    #end def (AddFailedOutput)


    def __handlerContactCallback(self, btnObject):

        if self.__debugFlag is True:
            print('>> Input Contact Pin [{}] is ACTIVE: [{}]'.format(btnObject.pin, btnObject.is_active))
        #end if

        # We don't want to process any more events when we're in a solved state
        if  ( self.__puzzleActive is True ) and ( self.__puzzleSolved is False ):
            if btnObject.is_active is True:
                if ( btnObject.pin is self.__puzzleInputPinObjects[self.__puzzlePatternPosition].pin ):
                    self.__puzzleOutputPinObjects[self.__puzzlePatternPosition].pulse()

                    self.__puzzlePatternPosition += 1

                    self.__checkForSolve()

                else:
                    self.Fail()
                #end if            
    #end def (__handlerContactCallback)


    def __checkForSolve(self):

        if self.__puzzlePatternPosition == len(self.__puzzleInputPinObjects):
            self.Solve()
            return True
            
        else:
            return False
        #end if
        
    #end def (__checkForSolve)

    
    def RegisterCallback(self, callback, callbackFunction):
        self.__callbacks[callback] = callbackFunction
    #end def (RegisterCallbacks)


    def Activate(self):
        
        self.__puzzleActive = True

        if self.__debugFlag is True:
            print('>> PUZZLE IS ACTIVE: [{}]'.format(self.__puzzleActive))
        #end if

        for individualOutputObject in self.__puzzleActiveOutputObjects:
            individualOutputObject.on()            
        #end for

        try:
            self.__callbacks['activated']()
        except:
            pass
        #end try

    #end def (Activate)


    def Solve(self):

        self.__puzzleSolved = True
        
        if self.__debugFlag is True:
            print('>> PUZZLE SOLVED!')
        #end if

        for individualOutputObject in self.__puzzleActiveOutputObjects:
            individualOutputObject.off()            
        #end for

        for individualOutputObject in self.__puzzleSolvedOutputObjects:
            individualOutputObject.on()
        #end for

        try:
            self.__callbacks['solved']()
        except:
            pass
        #end try
    #end def (Solve)


    def Fail(self):
        self.__puzzleFailed = True
        self.__puzzleActive = False
        
        if self.__debugFlag is True:
            print('>> PUZZLE FAILED!')
        #end if

        for individualOutputObjects in self.__puzzleOutputPinObjects:
            individualOutputObjects.off()
        #end for

        for individualOutputObject in self.__puzzleActiveOutputObjects:
            individualOutputObject.off()            
        #end for

        for individualOutputObject in self.__puzzleFailedOutputObjects:
            individualOutputObject.on()
        #end for
            
        try:
            self.__callbacks['failed']()
        except:
            pass
        #end try
    
    #end def (Fail)


    def Reset(self):
        
        if self.__debugFlag is True:
            print('>> PUZZLE RESET')
        #end if

        self.__puzzlePatternPosition = 0                

        self.__puzzleSolved = False
        self.__puzzleActive = False
        self.__puzzleFailed = False


        for individualOutputObjects in self.__puzzleOutputPinObjects:
            individualOutputObjects.off()
        #end for
                
        for individualOutputObjects in self.__puzzleActiveOutputObjects:
            individualOutputObjects.off()
        #end for

        for individualOutputObjects in self.__puzzleSolvedOutputObjects:
            individualOutputObjects.off()
        #end for

        for individualOutputObjects in self.__puzzleFailedOutputObjects:
            individualOutputObjects.off()
        #end for

        try:
            self.__callbacks['reset']()
        except:
            pass
        #end try

        if self.__puzzleAlwaysActive is True:
            self.Activate()
        #end if

    #end def (Reset)


    def ProcessEvents(self):
        pass
    #end def (ProcessEvents)
    
        
    def Cleanup(self):
        pass
    #end def (Cleanup)


    def GetPuzzleSolved(self):
        return self.__puzzleSolved
    #end def (GetPuzzleSolved)

#end class
