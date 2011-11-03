
from ctypes import *
import sys


import pygame
from pygame.locals import *

try:
    # For OpenGL-ctypes
    from OpenGL import platform
    gl = platform.OpenGL
except ImportError:
    try:
        # For PyOpenGL
        gl = cdll.LoadLibrary('libGL.so')
    except OSError:
        # Load for Mac
        from ctypes.util import find_library
        # finds the absolute path to the framework
        path = find_library('OpenGL')
        gl = cdll.LoadLibrary(path)
 
from OpenGL.GL import *

## framework files
from shader    import *
from glHelpers import *
from math3d    import *
from mesh      import *


"""
    * The pygame.USEREVENT event is used to bind a function for each cycle of the game.  
         It gets 'info' passed to it.
         - info.deltaTime - time in millseconds passed since last frame
"""
class Context:


    def __init__(self, title="Default", size=(320,200), fs=False):
        pygame.init()
        pygame.display.set_caption(title)
        fsmode = FULLSCREEN if fs else 0
        self.screen = pygame.display.set_mode(size, OPENGL|DOUBLEBUF|fsmode)
        self.callbacks = {}
        self.running = False
        self.timer = pygame.time.Clock()
        self.dt = 0
        self.fps = 0

    def getDeltaTime(self):
        return self.dt
    def getFPS(self):
        return self.fps
    def getScreen(self):
        return self.screen

    def run(self):
        self.running = True
        while self.running:
            for e in pygame.event.get():
                self.dispatch(e)
            self.dt = self.timer.tick(self.fps)
            self.generateEvent(self.dt)


    def bindFunction(self, event, func):
        self.callbacks[event] = func
    def unbindFunction(self, event):
        self.callbacks.pop(event)
    def clearFunctions(self):
        self.callbacks.clear()

    def generateEvent(self, name):
        self.dispatch(pygame.event.Event(USEREVENT, deltaTime=name))
    def dispatch(self, e):
        if self.callbacks.has_key(e.type):
            self.callbacks[e.type](e)
        elif e.type == QUIT:   ## this should maybe not be here
            self.kill()

    def kill(self):
        self.running = False


class Camera:
    r = 0      # circular 
    theta = 0  # up and down
    d = 0      # distance from origin

    def __init__(self):
        a = 1
    def point(self):

        glTranslatef(-5.0,-2.5,-22.0)      # Move Right And Into The Screen
        glRotatef(10.0, 1.0, 0.0, 0.0)

        #glRotatef(self.r, 0.0, 1.0, 0.0)
        #glRotatef(self.theta, 1.0, 0.0, 0.0)

    def reset(self):
        r = 0
        theta = 0

    """def moveUp(self, theta):
    def moveDown(self, theta):
    def rotateClockwise(self, r):
    def roteteCounterClockwise(self, r):
    def moveTo(self, r, theta):"""

