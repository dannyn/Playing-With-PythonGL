#!/usr/bin/python2

import pygame
from pygame.locals import *

import math

from OpenGL.GL import *
from OpenGL.GLU import *

#from Image import *
## framework files
from renderer  import *
from glHelpers import *
from math3d    import *
from mesh      import *
from framework import *
from renderer  import *

class Scene:
    def __init__(self):
        self.programs = { 
                'tex'  : compileProgram('data/shaders/texdemo.vert', 'data/shaders/texdemo.frag', True),
                'black' : compileProgram('data/shaders/black.vert', 'data/shaders/black.frag',True)
        }
        self.camera = Camera()

        glEnable(GL_TEXTURE_2D)
        glUseProgram(self.programs['tex'])
        texData = loadImage('data/tex.jpg')
        width = 512 #surface.size[0]
        height = 512 #surface.size[1]

        #self.texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture( GL_TEXTURE_2D,0);
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3,width, height, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, texData);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    

        self.clock = pygame.time.Clock()

    def update(self, dt):
        self.clock.tick()
        #print self.clock.get_fps()   

    def render(self):
        glLoadIdentity()
        glClearColor(0.5, 0.5, 0.5, 0.0)
        glClearDepth(1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.camera.point()

        uniformLoc = glGetUniformLocation(self.programs['tex'], 'colorMap')
        glUniform1i(uniformLoc, 1)

        glBegin(GL_QUADS)
        glTexCoord2f(1,1)
        glVertex2f(1.0, 1.0)
        glTexCoord2f(1,0)
        glVertex2f(1.0,-1.0)
        glTexCoord2f(0,0)
        glVertex2f(-1.0,-1.0)
        glTexCoord2f(0,1)
        glVertex2f(-1.0, 1.0)

   
        glEnd()
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
    #glEnable(GL_CULL_FACE)
    #glCullFace(GL_BACK)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
    gluPerspective(45.0, float(320)/float(200), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

    c.run()

    
