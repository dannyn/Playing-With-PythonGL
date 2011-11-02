#########################
#
#
#########################
#
# Some points - 
#    * game coords are a grid WIDTH/UNIT accross and HEIGHT/UNIT down
#    * a box is a point in that grid, always references in game coord
#
#########################

import os, sys, random
import pygame
from pygame.locals import *
import pygame.font

import context



############ SUPPORTING STUFF #####################
# some constants
UNIT = 20     # number of pixels for a rect
WIDTH = 640   # screen width
HEIGHT = 480  # screen height
ROWS = HEIGHT /  UNIT  - 1  # rows in game coords
COLS = WIDTH  /  UNIT  - 1  # cols in game coords

# some colors
YELLOW = [255,255,0]
WHITE  = [255,255,255]
BLACK  = [0,0,0]
GREEN  = [0,255,0]
BLUE   = [0,0,255]
RED    = [255,0,0]


## draws in screen coords
def drawBox(surface, color, x, y):
    pygame.draw.rect(surface, color, pygame.Rect(x * UNIT, y * UNIT, UNIT, UNIT))    


################## THE SNAKE ####################
class Snake:

    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4
    
    # (x, y)
    #body = []
    #direction = RIGHT
    #growing = 0
    
    def __init__(self):
        # start out two long
        # this should maybe be random
        self.body = []
        self.body.append((COLS/2, ROWS/2))
        self.body.append((COLS/2-1, ROWS/2))
        self.isDead = False
        self.growing = 0
        self.direction = Snake.RIGHT

    def update(self, dt):
        # make a copy of the old one and start fresh
        oldBody = self.body
        self.body = []
       
        # append new head
        oldHead = oldBody[0] # make copy for cleaner code
        if self.direction == Snake.UP:
            if oldHead[1] == 0:   # wrap at edge of screen
                self.body.append (( oldHead[0], ROWS ))
                self.direction = Snake.UP
            else:
                self.body.append (( oldHead[0], oldHead[1] -1 ))
        elif self.direction == Snake.DOWN:
            if oldHead[1] == ROWS:
                self.body.append (( oldHead[0], 0 ))
                self.direction = Snake.DOWN
            else:
                self.body.append (( oldHead[0], oldHead[1] +1 ))
        elif self.direction == Snake.RIGHT:
            if oldHead[0] == COLS:
                self.body.append (( 0, oldHead[1] ))
                self.direction == Snake.LEFT
            else:
                self.body.append (( oldHead[0] + 1, oldHead[1] ))
        elif self.direction == Snake.LEFT:
            if oldHead[0] == 0:
                self.body.append (( COLS, oldHead[1] ))
                self.direction == Snake.RIGHT
            else:
                self.body.append (( oldHead[0] - 1, oldHead[1] ))

        # copy old list into new one behind the new head
        for x, y in oldBody:
            self.body.append((x, y))

        ########### need to fix this its so embarrassingly retarded
        # and delete the last element to make move
        # if its growing grow by not doing this
        if self.growing >= 1:
            self.growing -= 1
        else:
            del self.body[-1]

        # check for collision with self
        for x, y in self.body[1:]:
            if x == self.body[0][0] and y == self.body[0][1]:
                self.isDead = True

        return self.isDead

    def render(self, surface):
        for x, y in self.body:
            drawBox(surface, YELLOW, x,y)

    def changeDir(self, d):
        if (d == Snake.UP    and self.direction != Snake.DOWN) or \
           (d == Snake.DOWN  and self.direction != Snake.UP)   or \
           (d == Snake.RIGHT and self.direction != Snake.LEFT) or \
           (d == Snake.LEFT  and self.direction != Snake.RIGHT):
            self.direction = d

    def grow(self, length):
        self.growing += length

    def checkCollision(self, cX, cY):
        # actually only need to check the head for most things
        # but leaving like this because need to check whole thing
        # when new food is placed
        for x, y in self.body:
            if cX == x and cY == y:
                return True
        return False

###################  FOOD  #########################
class Food:
    
    def __init__(self):
        self.x = random.randint(0, COLS)
        self.y = random.randint(0, ROWS)
        self.color = RED

    def render(self, surface):
        drawBox(surface, RED, self.x, self.y)

    def newCoords(self):
        self.x = random.randint(0, COLS)
        self.y = random.randint(0, ROWS)

#################### THE GAME ######################
class Game:

    def __init__(self):

        # I do not know how I feel about this being here
        self.font = pygame.font.Font(None, 18)

        self.snake = Snake()
        self.food = [] 
        self.addFood()
        self.addFood()

        self.timeCounter = 0
        self.speed = 100 # milliseconds before updating 

        self.score = 0
        self.time  = 0 # time the game has been running

        self.mode = 'running'

        self.font = pygame.font.SysFont(None, 48)
        
    def reset(self):
        self.snake = Snake()
        self.food = []
        self.addFood()
        self.addFood()

        self.timeCounter = 0
        self.speed = 100

        self.score = 0
        self.time = 0
        self.mode = 'running'

    def render(self):
        surface = pygame.Surface((WIDTH,HEIGHT))
        surface  = surface.convert()
        surface.fill(BLACK)


        if self.mode == 'dead' or self.mode == 'running':

            self.snake.render(surface)

            for i in self.food:
                i.render(surface)
        
        if self.mode == 'dead':
            text = self.font.render('You Died!', True, WHITE)
            text_r = text.get_rect()
            text_r.centerx = WIDTH / 2
            text_r.top = HEIGHT / 3
            surface.blit(text, text_r)

            text = self.font.render('You played for ' + str(self.time /1000  ) + ' seconds.' , True, WHITE)
            text_r = text.get_rect()
            text_r.centerx = WIDTH / 2
            text_r.top = HEIGHT / 3 + 50
            surface.blit(text, text_r)

            text = self.font.render('You ate ' + str(self.score) + ' pieces of food.', True, WHITE)
            text_r = text.get_rect()
            text_r.centerx = WIDTH / 2
            text_r.top = HEIGHT / 3 + 100
            surface.blit(text, text_r)

            text = self.font.render('Press space bar to play again.', True, WHITE)
            text_r = text.get_rect()
            text_r.centerx = WIDTH /2
            text_r.top = HEIGHT / 3 + 150
            surface.blit(text, text_r)
            
        return surface

    def update(self, dt):
        self.timeCounter += dt

        if self.mode == 'running':
            self.time += dt
        if self.timeCounter >= self.speed:

            if self.mode == 'running':
                if(self.snake.update(dt)):
                    self.mode = 'dead' 
                else: 
                    for f in self.food[:]:
                        if self.snake.checkCollision(f.x, f.y):
                            self.food.remove(f)
                            self.snake.grow(2)
                            self.addFood()
                            self.score += 1
            elif self.mode == 'dead':
                return 0

            self.timeCounter = 0

    ##### events passed to here #####
    def onKeyDown(self, key):
        if self.mode == 'running':
            if key ==  pygame.K_UP:
                self.snake.changeDir (Snake.UP)
            if key == pygame.K_DOWN:
                self.snake.changeDir (Snake.DOWN)
            if key == pygame.K_RIGHT:
                self.snake.changeDir (Snake.RIGHT)
            if key == pygame.K_LEFT:
                self.snake.changeDir (Snake.LEFT)
            if key == pygame.K_SPACE:
                self.snake.grow(2)
        elif self.mode == 'dead':
            if key == pygame.K_SPACE:
                self.reset()
                
    def onKeyUp(self, key):
        return 1

    def addFood(self):
        f = Food()
        # check if it collides, if it does
        # keep getting new coords until it doesnt

        self.food.append(f)

class application:

    def __init__(self):
        self.c = context.Context("pySnake", (640,480))
        self.game = Game()

        self.c.bindFunction(USEREVENT, self.onUserEvent)
        self.c.bindFunction(KEYDOWN, self.onKeyDown)

        self.screen = self.c.getScreen()
        self.c.run()

    def update(self):
        self.game.update(self.c.getDeltaTime())
    
    def render(self):
        surface = self.game.render()
        self.screen.blit(surface, (0,0))
        pygame.display.flip()

    def onKeyDown(self, e):
        self.game.onKeyDown(e.key)

    def onUserEvent(self, e):
        if e.task == self.c.UPDATE:
            self.update()
        elif e.task == self.c.RENDER:
            self.render()


if __name__ == "__main__":
    app = application()   

