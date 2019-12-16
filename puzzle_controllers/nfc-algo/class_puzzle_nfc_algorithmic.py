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

import nfc
import ndef
from nfc.clf import RemoteTarget

class AlgorithmicPuzzleNFC:

    def __init__(self, ReaderPort, Debug = False):
    
        self.__debugFlag = Debug
        self.__readerPort = ReaderPort	## LOOKS LIKE: tty:USB0:pn532
        
        self.__callbacks      = {}        
        self.__userPattern    = []
        self.__correctPattern = []
        self.__patternLength  = 0
        self.__puzzleSolved   = False
        self.__cardPresent    = False

        # FIXME - we need way better error checking (callbacks?) here
        # when/if we cannot communicate with our NFC readers
        # this is especially bad when we're buried deep inside a puzzle
        # I suspect we'll want to engineer some sort of hard reset
        # mechanism - perhaps even using the powered USB hub to our advantage
        self.__clf = nfc.ContactlessFrontend(self.__readerPort)

    #end def
    
    
    def AppendToSolutionPattern(self, solutionText):
        self.__correctPattern.append(solutionText)
        self.__patternLength = len(self.__correctPattern)
        
        # Ensure that our pattern storage list is exactly the same
        # size as our "correct pattern" exemplar list we are maintaining above
        self.__userPattern = [None] * self.__patternLength
    #end def

    
    def EnterNewElement(self, enteredElement):

        # Slide everything in our user pattern list of once to the left
        self.__userPattern = self.__userPattern[1:]

        # Add the newest element into our pattern storage list
        self.__userPattern.append(enteredElement)    
 
        self.CheckForSolve()
    #end def (EnterNewElement)
    

    def SpillYourGuts(self):
        print('===================')
        print('INTERNAL STATE DUMP')
        print('===================')
        print('PATTERN LENGTH: [{}]'.format(self.__patternLength))
        print('CORRECT PATTERN:')
        print(self.__correctPattern)
        print('\r\n')
        
        print('USER PATTERN:')
        print(self.__userPattern)
        print('\r\n')
        print('SOLVED STATE: [{}]'.format(self.__puzzleSolved))
        print('===================')
    #end def (SpillYourGuts)        


    def CheckForSolve(self):
        
        if self.__correctPattern == self.__userPattern:
            
            if self.__debugFlag is True:
                print('>> PUZZLE SOLVED!')
            #end if
            
            self.__puzzleSolved = True

            try:            
                self.__callbacks['Solved']()
            except:
                pass
            #end try
    #end def (CheckForSolve)

    
    def RegisterCallbacks(self, callback, callbackFunction):
        pass
    #end def (RegisterCallbacks)

    
    def Reset(self):
        self.__userPattern = []
        self.__puzzleSolved = False
    #end def (Reset)


    def ProcessEvents(self):

        target = self.__clf.sense(RemoteTarget("106A"))

        if target is None:
            self.__cardPresent = False
            return None
        #end if
                   
            
        # We don't want to be in here if we are reading the same card as last cycle
        if self.__cardPresent is True:
            return None
        #end if


        # If we get here, we should be reading a good tag *and* we can
        # consider it to be the first read of this tag    
        tag = nfc.tag.activate(self.__clf, target)

        try:
            if tag.ndef:
                if len(tag.ndef.records) > 0:
                    record = tag.ndef.records[0]

                    self.__cardPresent = True
                    
                    return (record.text)
                    
                else:
                    return None
                #end if
                
            else:
                return None
            #end if

        # This is likely to be triggered when we get weird card reads,
        # like when you move the card right in the middle of a read cycle,
        # or the card is sitting in the magnetic field enough to confuse the
        # reader but not enough to get good data.
        except:
            return None
        #end try
        
        
        # We should never get down to here! Fallthrough protection..
        return None
    #end def (ProcessEvents)
    
        
    def Cleanup(self):
        self.__clf.close()
    #end def (Cleanup)


    def GetPuzzleSolved(self):
        return self.__puzzleSolved
    #end def (GetPuzzleSolved)

#end class
