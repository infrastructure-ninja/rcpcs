#!/usr/bin/python3

# Puzzle Controller Class :: Touchscreen Finger Pattern (Android Unlock Screen)
# Part of the RCPCS project (Room Control and Puzle Coordination System)
# Copyright (C) 2019  Joel D. Caturia
# <based on portions of code presumed to be in the public domain>
#
#
# NOTE: This code was found in the wild, and was presumed to be public domain.
# It was updated to run on Python3, was cleaned up, more comments were added, 
# and was significantly re-factored to work inside a publisher/subscriber ecosystem
# that leverages callbacks.
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


import pygame
from pygame.locals import *

import time

class PuzzleClass:

    def __init__(self, DebugMode = False):

        print('Puzzle Initialization Beginning..')

        # When we're in "Debug Mode" we want the screen to be smaller,
        #   the window to be resizeable, and not lose our mouse cursor
        if DebugMode is True:
            self.hh = 400
            self.ww = 400       
            screenMode = pygame.RESIZABLE

            pygame.init()
            self.screen = pygame.display.set_mode((self.ww, self.hh), screenMode)
            pygame.display.set_caption('Touchscreen - Bank Safe [DEBUG MODE]') 

        else:
            self.hh = 600
            self.ww = 1024
            screenMode = pygame.FULLSCREEN

            pygame.init()
            self.screen = pygame.display.set_mode((self.ww, self.hh), screenMode)
            pygame.display.set_caption('Touchscreen - Bank Safe') 

            pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        #end if (DebugMode is True)

        
        
        self.callbacks = {}		# Holds our event callbacks

        self.stateSolved = False	# Holds our winning state
        
        # Define some colors in a dictionary (RGB values as a tuple)
        self.COLORS = {}
        self.COLORS['red']      = (255, 0, 0)
        self.COLORS['green']    = (0, 255, 0)
        self.COLORS['blue']     = (0, 0, 255)
        self.COLORS['darkBlue'] = (0, 0, 128)
        self.COLORS['white']    = (255, 255, 255)
        self.COLORS['black']    = (0, 0, 0)
        self.COLORS['pink']     = (255, 200, 200)

        self.stp = self.hh / 6		# 
        self.mid = self.ww / 2		# Middle column position

        self.line_x = [0, 0]
        self.line_y = [0, 0]
        self.line_width = 10		# Width of the line to draw when connecting circles
        self.pos = 'start'

        # These calculations are wrapped in an int(), otherwise they will return floats
        # (lots of decimal points of precision that we do not need, and cause problems with other methods/functions)
        self.center_x = [int(self.mid - 2 * self.stp), int(self.mid), int(self.mid + 2 * self.stp)]
        self.center_y = [int(self.stp), int(3 * self.stp), int(5 * self.stp)]

        self.running = True

        self.cnt = 0			# State .. Where we are at the pattern
        self.cnt_max = 9		# How many turns until we reset

        self.last_xx = 0
        self.last_yy = 0
        
        self.last_x = 0
        self.last_y = 0

        self.last_xx, self.last_yy = pygame.mouse.get_pos()

        self.last_x = self.last_xx
        self.last_y = self.last_yy

        self.rad1 = 60

        self.coord_to_num = [
            [self.center_x[0], self.center_y[0]],
            [self.center_x[1], self.center_y[0]],
            [self.center_x[2], self.center_y[0]],
            [self.center_x[0], self.center_y[1]],
            [self.center_x[1], self.center_y[1]],
            [self.center_x[2], self.center_y[1]],
            [self.center_x[0], self.center_y[2]],
            [self.center_x[1], self.center_y[2]],
            [self.center_x[2], self.center_y[2]]]

        self.current_combo = []

        self.right_combo = [
            [self.center_x[1], self.center_y[0]],
            [self.center_x[0], self.center_y[0]],
            [self.center_x[1], self.center_y[1]],
            [self.center_x[2], self.center_y[0]],
            [self.center_x[2], self.center_y[1]],
            [self.center_x[1], self.center_y[2]],
            [self.center_x[0], self.center_y[1]],
            [self.center_x[0], self.center_y[2]],
            [self.center_x[1], self.center_y[2]],
            [self.center_x[2], self.center_y[2]]]

        self.reset()
    #end def (__init__)


    def reset(self):

        self.current_combo = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]]
    
        self.screen.fill(self.COLORS['black'])

        # Draw our nine fabulous circles!
        rad2 = 10
        
        for xSubscript in range(0,3):
            for ySubscript in range(0,3):
                pygame.draw.circle( self.screen, self.COLORS['green'],
                                    (self.center_x[xSubscript], self.center_y[ySubscript]), self.rad1, rad2)
            #end for
        #end for
        
        pygame.display.update()

        self.cnt = 0
        self.pos = 'start'

        self.stateSolved = False
        
        print('[PUZZLE] > Resetting..')

        if 'reset' in self.callbacks.keys():
            self.callbacks['reset']()
        #end if

    #end def (reset)


    def IsSolved(self):
        return self.stateSolved
    #end def

    def solve(self):
        self.stateSolved = True

        if 'solve' in self.callbacks.keys():
            self.callbacks['solve']()
        #end if

        self.__showSolvedText()
        print('[PUZZLE] > Solved!!')
    #end def (solve)
        

    def ProcessEvents(self):
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if self.stateSolved == False:
                    self.__drawLineByMouseMove()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
                running = False
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            #end if (event types)
        #end for (check pygame events)
    #end def (do)


    
    # These are the callbacks we will support at the moment
    # - RESET : when the board is reset
    # - SOLVE : when the board fills up with lines, and you DID enter the correct combination
    # - FAIL  : when the board fills up with lines, and you did not enter the correct combination
    def RegisterCallback(self, eventName, callbackFunction):
    
        if  eventName in ['reset', 'Reset']:
            self.callbacks['reset'] = callbackFunction

        elif eventName in ['solve', 'Solve']:
            self.callbacks['solve'] = callbackFunction

        elif eventName in ['fail', 'Fail']:
            self.callbacks['fail'] = callbackFunction

        #end if
    
    #end def 


    def __check_area(self, x, y, radius):
        for k in range(0, 3):
            for j in range(0, 3):
                rad3 = (x - self.center_x[j]) ** 2 + (y - self.center_y[k]) ** 2
                rad4 = radius ** 2
                if rad3 < rad4:
                    return (self.center_x[j], self.center_y[k])
                #end if
            #end for
        #end for
        
        return (-1, -1)
    #end def (__checkarea)


    def __checkForSolved(self):

        tmpSolvedState = True
        for x in range(0, 10):
            print('[PUZZLE] > [{0}] WANTED: [x={1} y={2}]'.format(x, self.right_combo[x][0], self.right_combo[x][1]), end='')
            print(' -> GOT: [x={1} y={2}]'.format(x, self.current_combo[x][0], self.current_combo[x][1]), end='')
            
            if self.right_combo[x][0] != self.current_combo[x][0] or self.right_combo[x][1] != self.current_combo[x][1]:
                tmpSolvedState = False
                print(' -> Incorrect')
            else:
                print(' -> OK!')
            #end if
        #end for
        
        return tmpSolvedState
    #end def (__checkForSolved)



    def __drawLineByMouseMove(self):

        x, y = pygame.mouse.get_pos()
    
        if x != self.last_x and y != self.last_y:
            self.last_x = x
            self.last_y = y
        
            if self.pos == 'start':
                xx, yy = self.__check_area(x, y, 40)
                if xx >= 0 and yy >= 0 and (xx != self.last_xx or yy != self.last_yy):
                    print('[PUZZLE] > dot coordinate: {0}x{1}'.format(xx, yy) )
                    self.last_xx = xx
                    self.last_yy = yy
                    self.cnt += 1
                    self.line_x[0] = xx
                    self.line_y[0] = yy
                    self.pos = 'end'

                    pygame.draw.circle(self.screen, self.COLORS['white'], (self.line_x[0], self.line_y[0]), 10)
                    pygame.display.update()

                    self.current_combo[0][0] = xx
                    self.current_combo[0][1] = yy
                #end if
                
            elif self.pos == 'end':
                xx, yy = self.__check_area(x, y, 40)
                
                if xx >= 0 and yy >= 0 and (xx != self.last_xx or yy != self.last_yy):
                    print('[PUZZLE] > dot coordinate: {0}x{1}'.format(xx, yy) )
                    self.last_xx = xx
                    self.last_yy = yy
                    self.current_combo[self.cnt][0] = xx
                    self.current_combo[self.cnt][1] = yy
                    self.line_x[1] = xx
                    self.line_y[1] = yy
                    self.pos = 'end'
                    
                    pygame.draw.circle(self.screen, self.COLORS['white'], (self.line_x[1], self.line_y[1]), 10)
                    pygame.draw.line(self.screen, self.COLORS['white'], [self.line_x[0], self.line_y[0]], [self.line_x[1], self.line_y[1]], self.line_width)
                    pygame.display.update()
                    
                    self.line_x[0] = self.line_x[1]
                    self.line_y[0] = self.line_y[1]
                    self.cnt += 1
                #end if
            #end if
            
            if self.cnt > self.cnt_max:
                if self.__checkForSolved():
                    self.solve()
                
                else:
                    self.stateSolved = False
                    
                    if 'fail' in self.callbacks.keys():
                        self.callbacks['fail']()
                    #end if
                    
                    self.__showFailedText()    
                    print('[PUZZLE] > PUZZLE FAILED')
                    
                    time.sleep(3)
                
                    self.reset()
                    
                #end if
                
            #end if
                
        #end if
    #end def (__drawLineByMouseMove)


    def __showSolvedText(self):
        font = pygame.font.Font(None, 100)
        text1 = font.render('ACCESS', True, self.COLORS['black'], self.COLORS['green'])
        text2 = font.render('GRANTED', True, self.COLORS['black'], self.COLORS['green'])
        
        textRect1 = text1.get_rect()
        textRect1.center = (self.ww // 2, (self.hh // 2) - 50) 

        textRect2 = text2.get_rect()
        textRect2.center = (self.ww // 2, (self.hh // 2) + 50) 

        self.screen.fill(self.COLORS['green']) 
                  
        self.screen.blit(text1, textRect1)
        self.screen.blit(text2, textRect2)

        pygame.display.update()
    #end def


    def __showFailedText(self):
        font = pygame.font.Font(None, 100)
        text1 = font.render('ACCESS', True, self.COLORS['white'], self.COLORS['red'])
        text2 = font.render('DENIED', True, self.COLORS['white'], self.COLORS['red'])
        
        textRect1 = text1.get_rect()
        textRect1.center = (self.ww // 2, (self.hh // 2) - 50) 

        textRect2 = text2.get_rect()
        textRect2.center = (self.ww // 2, (self.hh // 2) + 50) 

        self.screen.fill(self.COLORS['red']) 
                  
        self.screen.blit(text1, textRect1)
        self.screen.blit(text2, textRect2)

        pygame.display.update()
    #end def
    


#end class (PuzzleClass)
'''
################################################################################
## THIS FUNCTION DOES NOT APPEAR TO BE USED IN THE CURRENT VERSION OF THE PUZZLE
## JOEL C - NOV 29, 2019
################################################################################
def line_by_mouse_btn():
    global line_x
    global line_y
    if pos == 'start':
        line_x[0], line_y[0] = pygame.mouse.get_pos()
        xx, yy = check_area(line_x[0], line_y[0], rad1)
        if xx >= 0 & yy >= 0:
            line_x[0] = xx
            line_y[0] = yy
            pos = 'end'
            pygame.draw.circle(screen, white, (line_x[0], line_y[0]), 10)
            pygame.display.update()
    elif pos == 'end':
        line_x[1], line_y[1] = pygame.mouse.get_pos()
        xx, yy = check_area(line_x[1], line_y[1], rad1)
        if xx >= 0 & yy >= 0:
            line_x[1] = xx
            line_y[1] = yy
            pos = 'end'
            pygame.draw.circle(screen, white, (line_x[1], line_y[1]), 10)
            pygame.draw.line(screen, white, [line_x[0], line_y[0]], [line_x[1], line_y[1]], line_wide)
            pygame.display.update()
            line_x[0] = line_x[1]
            line_y[0] = line_y[1]
    cnt += 1
    if cnt > cnt_max:
        cnt = 0
        pos = 'start'
        screen.fill(black)
        draw_circles()

'''
