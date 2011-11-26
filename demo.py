#!/usr/bin/python2

import pygame
from pygame.locals import *

import math

from OpenGL.GL import *
from OpenGL.GLU import *

## framework files
from glHelpers import *
from math3d    import *
from mesh      import *
from framework import *
from renderer import *


class Scene:
    def __init__(self):
        self.light = [1.0, 0.0, 1.4, 0.0]
        self.celTexture = [0.95, 0.95, 0.95, 1.0,
                           0.7,  0.7,  0.7,  1.0,
                           0.4,  0.4,  0.4,  1.0, 
                           0.25, 0.25, 0.25, 1.0,
                           0.05, 0.05, 0.05, 1.0]
        '''self.celTexture = [0.9, 0.9, 0.9, 1.0,
                        0.8, 0.8, 0.8, 1.0,
                        0.7, 0.7, 0.7, 1.0,
                        0.6, 0.6, 0.6, 1.0,
                        0.5, 0.5, 0.5, 1.0,
                        0.4, 0.4, 0.4, 1.0,
                        0.3, 0.3, 0.3, 1.0,
                        0.2, 0.2, 0.2, 1.0]'''
        self.celTexture.reverse();
        self.m = loadMesh('data/pig.obj')
        self.programs = { 
                'toon'  : compileProgram('data/shaders/toon.vert', 'data/shaders/toon.frag', True),
                'black' : compileProgram('data/shaders/black.vert', 'data/shaders/black.frag',True)
        }
        self.camera = Camera()

        glUseProgram(0)

        #self.texID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_1D, 1)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA, 4, 0, GL_RGBA, GL_FLOAT, self.celTexture)

        self.clock = pygame.time.Clock()
        
        #self.texCoordOffsets = numpy.array((),dtype='f')
        self.texCoordOffsets = [0] * 18
        self.textureWidth = 640
        self.textureHeight = 480

        xInc = 1.0 / self.textureWidth
        yInc = 1.0 / self.textureHeight

        for i in range(3):
            for j in range(3):
                self.texCoordOffsets[(((i*3)+j)*2)+0] = (-1.0 * xInc) + (i * xInc)
                self.texCoordOffsets[(((i*3)+j)*2)+1] = (-1.0 * yInc) + (j * yInc)

    def update(self, dt):
        self.clock.tick()
        #print self.clock.get_fps()   

    def render(self):
        glLoadIdentity()
        glClearColor(0.5, 0.5, 0.5, 0.0)
        glClearDepth(1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light);
        
        self.camera.point()

        glUseProgram(self.programs['toon'])

        uniformLoc = glGetUniformLocation(self.programs['toon'], 'celTex')
        glUniform1i(uniformLoc, 1)
        glPushMatrix()
        glTranslatef(0.0, 2.0, 0.0)
        self.m.render()
        glPopMatrix()

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

    

if __name__ == "__main__":

    def cycle(info):
        scene.update(0)
        scene.render()

        
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

    
