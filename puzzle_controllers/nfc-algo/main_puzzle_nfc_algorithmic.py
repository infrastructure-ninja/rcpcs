#!/usr/bin/python3

# Example Puzzle Controller :: NFC Algorithmic Solve
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


from class_puzzle_nfc_algorithmic import AlgorithmicPuzzleNFC

puzzle = AlgorithmicPuzzleNFC('tty:USB0:pn532', Debug = True)
#puzzle = AlgorithmicPuzzleNFC('tty:AMA0:pn532', Debug = True)

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
#end try    
