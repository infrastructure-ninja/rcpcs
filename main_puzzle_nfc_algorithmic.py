#!/usr/bin/python3

from class_puzzle_nfc_algorithmic import AlgorithmicPuzzleNFC

puzzle = AlgorithmicPuzzleNFC('tty:USB0:pn532', Debug = True)

puzzle.AppendToSolutionPattern('shoreline.nt.altar.bible')
puzzle.AppendToSolutionPattern('shoreline.nt.altar.torah')
puzzle.AppendToSolutionPattern('shoreline.nt.altar.koran')
puzzle.AppendToSolutionPattern('shoreline.nt.altar.torah')

puzzle.SpillYourGuts()
print('>> Waiting for NFC tag..')

try:

    while puzzle.GetPuzzleSolved() is False:
        tempInput = puzzle.ProcessEvents()
        
        if tempInput is not None:
            puzzle.EnterNewElement(tempInput)
       
            puzzle.SpillYourGuts()

            print('>> Waiting for NFC tag..')
        #end if
    #end while

    puzzle.Cleanup()

except KeyboardInterrupt:
    print('\r\nCTRL+C Received! Exiting..\r\n')
    
except Exception as e:
    print(e)

finally:
    puzzle.Cleanup()
    
