#!/usr/bin/python3

# Example Puzzle Controller :: NFC AND Solve
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