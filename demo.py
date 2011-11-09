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


class Camera:

    def __init__(self):
        self.v = Vector3()

    def rotateClockwise(self, r):
        return 1
    def rotateCounterClockwise(self, r):
        return 1

     
class Scene:

    def __init__(self):

        self.m = ObjMeshLoader('data/cube.obj')
        self.m.createVertexIndex()
        self.m.createVertexNormals()
        self.light = [1.0, 0.0, 1.4, 0.0]
        self.program=compileProgram('data/shaders/toonf2.vert', 'data/shaders/toonf2.frag', True)
        glUseProgram(self.program)
        self.theta = 15
        self.t = TerrainMesh(20,20)
        self.rx = 0
        self.ry = 0
        self.pz = -18
        self.px = 0
    def update(self, dt):
        self.theta += 0.05

    def render(self):
        glLoadIdentity()
        glClearColor(0.5, 0.5, 0.5, 0.0)
        glClearDepth(1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light);
        glRotatef(self.ry, 0.0, 1.0, 0.0)
        glRotatef(self.rx, 1.0, 0.0, 0.0)
        glTranslatef(self.px, -3.0 ,self.pz )

        glPushMatrix()
        glTranslate(-5.0, 0.0, 0.0)
        self.t.render()
        self.t.renderOutline()
        glPopMatrix()

        glPushMatrix()
        glRotatef(25, 0.0, 0.0, 1.0)
        glRotatef(self.theta , 0.0, 1.0, 0.0)
        self.m.render()
        self.m.renderOutline()
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(3.0, 0.0, 0.0)
        self.m.render(0.0, 0.0, 1.0)
        self.m.renderOutline()
        glPopMatrix()

        pygame.display.flip()

    def onKeyDown(self, e):
        key = e.key
        if key == pygame.K_UP:
            self.rx -= 5
        if key == pygame.K_DOWN:   
            self.rx += 5
        if key == pygame.K_LEFT:
            self.ry -= 5
        if key == pygame.K_RIGHT:
            self.ry += 5
        if key == pygame.K_w:
            self.pz += 2
        if key == pygame.K_s:
            self.pz -= 2
        if key == pygame.K_a:
            self.px += 2
        if key == pygame.K_d:
            self.px -= 2

scene = 0

def cycle(info):
    scene.update(0)
    scene.render()
    

if __name__ == "__main__":
    c = Context("demo", (640, 480))
    scene = Scene()
    c.bindFunction(USEREVENT, cycle)
    c.bindFunction(KEYDOWN, scene.onKeyDown)

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

    c.run()

    
