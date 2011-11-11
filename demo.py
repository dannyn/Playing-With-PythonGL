#!/usr/bin/python

import pygame
from pygame.locals import *

import math

from OpenGL.GL import *
from OpenGL.GLU import *

## framework files
from shader    import *
from glHelpers import *
from math3d    import *
from mesh      import *
from framework import *

''' implemented here as a 2d circle around the origin, 
    theta is the angle between r-> (of which self.r is the magnitude) and 
    the x axis.  this makes all rotations around the z axis.
'''
class Camera:
    

    def __init__(self):
        self.r = 1
        self.theta = 0

    def rotate(self, angle):
        self.theta += angle 

    def move(self, d):
        self.r += d

    def toCartesian(self):
        rad =  3.14159/180

        v = Vector3()
        v[0] = math.cos(rad * self.theta) * self.r
        v[2] = 0 # only 2d for now so x and z plane
        v[1] = math.sin(rad * self.theta) * self.r
        return v

    def point(self):
        v = self.toCartesian()

        glRotatef(self.theta +90 , 0, 1, 0)
        glTranslatef(v[0], -2, v[1])
     
        #print 'r', self.r, 'theta(deg)', self.theta, v

class Scene:

    def __init__(self):

        self.m = ObjMeshLoader('data/cube.obj')
        self.teddy = ObjMeshLoader('data/teddy.obj')
        self.m.createVertexIndex()
        self.m.createVertexNormals()
        self.teddy.createVertexIndex()
        self.teddy.createVertexNormals()
        self.light = [1.0, 0.0, 1.4, 0.0]
        self.program=compileProgram('data/shaders/toonf2.vert', 'data/shaders/toonf2.frag', True)
        glUseProgram(self.program)
        self.theta = 15
        self.t = TerrainMesh(20,20)
        self.rx = 0
        self.ry = 0
        self.pz = -18
        self.px = 0
        self.camera = Camera()

        self.celTexture = [0.95, 0.95, 0.95, 1.0,
                           0.7,  0.7,  0.7,  1.0,
                           0.4,  0.4,  0.4,  1.0, 
                           0.25, 0.25, 0.25, 1.0]
        self.texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_1D, self.texID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA, 4, 0, GL_RGBA, GL_FLOAT, self.celTexture)

    def update(self, dt):
        self.theta += 0.5

    def render(self):
        glLoadIdentity()
        glClearColor(0.5, 0.5, 0.5, 0.0)
        glClearDepth(1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light);
        
        self.camera.point()

        glPushMatrix()
        glTranslate(-10.0, 0.0, -10.0)
        self.t.render()
        self.t.renderOutline()
        glPopMatrix()

        '''glPushMatrix()
        glRotatef(25, 0.0, 0.0, 1.0)
        glRotatef(self.theta , 0.0, 1.0, 0.0)
        glTranslatef(0.0, 2.0, 0.0)
        self.m.render()
        self.m.renderOutline()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(5.0, 10.0, 0.0)
        glScalef(0.09, 0.09, 0.09)
        self.teddy.render(0.0, 2.0, 1.0)
        glPopMatrix()

        glPushMatrix()
        glTranslate(3.0, 0.0, 0.0)
        self.m.render(0.0, 0.0, 1.0)
        self.m.renderOutline()
        glPopMatrix()'''

        pygame.display.flip()

    def onKeyDown(self, e):
        key = e.key
        if key == pygame.K_UP:
            self.camera.move(5)
        if key == pygame.K_DOWN:   
            self.camera.move(-5)
        if key == pygame.K_LEFT:
            self.camera.rotate(-5)
        if key == pygame.K_RIGHT:
            self.camera.rotate(5)

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

    
