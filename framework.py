#!/usr/bin/env python2

from ctypes import *
import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *


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

        self.key = [False] * 500 # need to get size
        self.mouseButton = [0] * 5
        self.mouseCoords = (0,0)
        self.mouseDelta  = (0,0) # how far mouse has moved since last frame

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
            self.cycle()

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
        elif e.type == KEYDOWN:
            self.key[e.key] = True
        elif e.type == KEYUP:
            self.key[e.key] = False

    def kill(self):
        self.running = False

    # meant to be overridden by anything subclassing this
    def cycle(self): 
        print "too"

