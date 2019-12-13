#!/usr/bin/python3

import nfc
import ndef
from nfc.clf import RemoteTarget

class ANDMatchPuzzleNFC:

    def __init__(self, Debug = False):

        self.__debugFlag             = Debug
        self.__puzzleReaderElements  = {}
        self.__puzzleMatchElements   = {}
        self.__readerStorageDict     = {}
        self.__callbacks             = {}
        self.__puzzleSolved          = False
      

    #end def (__init__)
    
    def AddPuzzleElement(self, ReaderPort, FriendlyName, MatchingText):

        # FIXME - we need way better error checking (callbacks?) here
        # when/if we cannot communicate with our NFC readers
        # this is especially bad when we're buried deep inside a puzzle
        # I suspect we'll want to engineer some sort of hard reset
        # mechanism - perhaps even using the powered USB hub to our advantage

        if self.__debugFlag is True:
            print('>> Attempting to add NFC reader: [NAME:{}] [PORT:{}]'.format(FriendlyName, ReaderPort))
        #end if
       
        ## LOOKS LIKE: tty:USB0:pn532 (on Linux)
        self.__puzzleReaderElements[FriendlyName] = nfc.ContactlessFrontend(ReaderPort)  
    
        if self.__puzzleReaderElements[FriendlyName]:
            if self.__debugFlag is True: print('  >> SUCCESS!')

            self.__puzzleMatchElements[FriendlyName] = MatchingText            
    
    #end def (AddPuzzleElement)


    def SpillYourGuts(self):
        print('===================')
        print('INTERNAL STATE DUMP')
        print('===================')
#        print('PATTERN LENGTH: [{}]'.format(self.__patternLength))
        print('MATCH DICTIONARY:')
        print(self.__puzzleMatchElements)
        print('\r\n')

        print('REAL-TIME DICTIONARY:')
        print(self.__readerStorageDict)
        print('\r\n')
        print('SOLVED STATE: [{}]'.format(self.__puzzleSolved))
        print('===================')
    #end def (SpillYourGuts)        

    
    def ProcessEvents(self):
        for friendlyName, objReader in self.__puzzleReaderElements.items():
            print(' >>> SERVICE -> [{}]'.format(friendlyName))

            target = objReader.sense(RemoteTarget("106A"))

            if target is None:
                self.__readerStorageDict[friendlyName] = None
                continue
                
            try:
                tag = nfc.tag.activate(objReader, target)

                if tag.ndef:
                    if len(tag.ndef.records) > 0:
                        record = tag.ndef.records[0]

                        self.__readerStorageDict[friendlyName] = record.text
                        
                        #self.CheckForSolve()
                        
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


        #end for
    
    
    #end def (ProcessEvents)

    
    def CheckForSolved(self):
    
        tmpPuzzleSolved = True
        for friendlyName, textToMatch in self.__puzzleMatchElements.items():
            try:
                if self.__readerStorageDict[friendlyName] == textToMatch:
                    if self.__debugFlag is True:
                        print('>> [{}] - MATCH - [{}]'.format(friendlyName, textToMatch))

                    next
                
                else:
                    self.__puzzleSolved = False
                    return False
                #end if
              
           # I could see us hitting an exception here if we try and get into a dictionary key that doesn't
           # exist - technically that would mean the puzzle was not solved so that's how we'll handle it
           # for the time being.  
            except:
                print('EXCEPTION!')
                self.__puzzleSolved = False
                return False
            #end try
        #end for
        
        if tmpPuzzleSolved is True:

            self.__puzzleSolved = tmpPuzzleSolved
    
            try:
                self.__callbacks['Solved']()
                
            except:
                pass
            #end try
            
            return True
        
        else:
            return False
        
        #end if
    
    
    #end def (CheckForSolve)    

    def Cleanup(self):
        for friendlyName, objReader in self.__puzzleReaderElements.items():
            print('CLEANUP -> [{}]'.format(friendlyName))
            objReader.close()
        #end for
    #end def (Cleanup)


    def GetPuzzleSolved(self):
        return self.__puzzleSolved
    #end def (GetPuzzleSolved)


#end class (ANDMatchPuzzleNFC)
