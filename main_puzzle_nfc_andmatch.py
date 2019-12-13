#!/usr/bin/python3

from class_puzzle_nfc_andmatch import ANDMatchPuzzleNFC

puzzle = ANDMatchPuzzleNFC(Debug = True)

puzzle.AddPuzzleElement('tty:AMA0:pn532', 'R1C1', 'shoreline.nt.altar.bible')
puzzle.AddPuzzleElement('tty:USB0:pn532', 'R1C2', 'shoreline.nt.altar.koran')


try:

    while puzzle.GetPuzzleSolved() is False:
        puzzle.ProcessEvents()
        puzzle.CheckForSolved()
    #end while
                
    puzzle.SpillYourGuts()

    #puzzle.Cleanup()

except KeyboardInterrupt:
    print('\r\nCTRL+C Received! Exiting..\r\n')

except Exception as e:
    print(e)

finally:
    puzzle.Cleanup()

#end try