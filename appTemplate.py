#!/usr/bin/env python2

'''
    This file is the documentation for and an example of how
    to use a Context.  
'''

import pygame

from framework import *

#from texDemo import *
from demo import *

class Template(Context):

    def __init__(self):
        Context.__init__(self, size=(640,480))
        glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
        glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    # Reset The Projection Matrix
        gluPerspective(45.0, float(320)/float(200), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        self.scene = Scene()

        self.bindFunction(KEYDOWN, self.scene.onKeyDown)


    def cycle(self):
        self.scene.update(0)
        self.scene.render() 

if __name__ == "__main__":  
    t = Template()
    t.run()


