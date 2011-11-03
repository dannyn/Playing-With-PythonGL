#!/usr/bin/python

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

## framework files
from shader    import *
from glHelpers import *
from math3d    import *
from mesh      import *
from framework import *

class Scene:

    def __init__(self):

        self.m = ObjMesh('data/cube.obj')
        self.light = [1.0, 0.0, 1.0, 0.0]
        self.rot = 0
        self.program=compileProgram('data/toonf2.vert', 'data/toonf2.frag', True)
        glUseProgram(self.program)
    def update(self, dt):

        self.rot += 0.15
        return 1

    def render(self):
        glLoadIdentity()
        glClearColor(0.5, 0.5, 0.5, 0.0)
        glClearDepth(1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light);
        glTranslatef(0.0, 0.0, -10.0 )
        glRotatef(self.rot, 1.0, 0.0, 1.0)
        self.m.renderImmediateMode()

        pygame.display.flip()


scene = 0

def cycle(info):
    scene.update(0)
    scene.render()
    

if __name__ == "__main__":
    c = Context("demo", (640, 480))
    scene = Scene()
    c.bindFunction(USEREVENT, cycle)

    glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
    glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
# Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(320)/float(200), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

    c.run()

    
