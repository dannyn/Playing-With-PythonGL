
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
from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray
from OpenGL.GL.ARB import vertex_array_object

## framework files
from shader    import *
from glHelpers import *
from math3d    import *


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



class Scene:

    def __init__(self):
        self.vertexData = [
         0.25,  0.25, -1.25, 1.0,
         0.25, -0.25, -1.25, 1.0,
        -0.25,  0.25, -1.25, 1.0,

         0.25, -0.25, -1.25, 1.0,
        -0.25, -0.25, -1.25, 1.0,
        -0.25,  0.25, -1.25, 1.0,

         0.25,  0.25, -2.75, 1.0,
        -0.25,  0.25, -2.75, 1.0,
         0.25, -0.25, -2.75, 1.0,

         0.25, -0.25, -2.75, 1.0,
        -0.25,  0.25, -2.75, 1.0,
        -0.25, -0.25, -2.75, 1.0,

        -0.25,  0.25, -1.25, 1.0,
        -0.25, -0.25, -1.25, 1.0,
        -0.25, -0.25, -2.75, 1.0,

        -0.25,  0.25, -1.25, 1.0,
        -0.25, -0.25, -2.75, 1.0,
        -0.25,  0.25, -2.75, 1.0,

         0.25,  0.25, -1.25, 1.0,
         0.25, -0.25, -2.75, 1.0,
         0.25, -0.25, -1.25, 1.0,

         0.25,  0.25, -1.25, 1.0,
         0.25,  0.25, -2.75, 1.0,
         0.25, -0.25, -2.75, 1.0,

         0.25,  0.25, -2.75, 1.0,
         0.25,  0.25, -1.25, 1.0,
        -0.25,  0.25, -1.25, 1.0,

         0.25,  0.25, -2.75, 1.0,
        -0.25,  0.25, -1.25, 1.0,
        -0.25,  0.25, -2.75, 1.0,

         0.25, -0.25, -2.75, 1.0,
        -0.25, -0.25, -1.25, 1.0,
         0.25, -0.25, -1.25, 1.0,

         0.25, -0.25, -2.75, 1.0,
        -0.25, -0.25, -2.75, 1.0,
        -0.25, -0.25, -1.25, 1.0,

        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,


        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,


        0.8, 0.8, 0.8, 1.0,
        0.8, 0.8, 0.8, 1.0,
        0.8, 0.8, 0.8, 1.0,
        0.8, 0.8, 0.8, 1.0,
        0.8, 0.8, 0.8, 1.0,
        0.8, 0.8, 0.8, 1.0,
        



        0.0, 1.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,

        0.5, 0.5, 0.0, 1.0,
        0.5, 0.5, 0.0, 1.0,
        0.5, 0.5, 0.0, 1.0,

        0.5, 0.5, 0.0, 1.0,
        0.5, 0.5, 0.0, 1.0,
        0.5, 0.5, 0.0, 1.0,

        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,

        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,

        0.0, 1.0, 1.0, 1.0,
        0.0, 1.0, 1.0, 1.0,
        0.0, 1.0, 1.0, 1.0,

        0.0, 1.0, 1.0, 1.0,
        0.0, 1.0, 1.0, 1.0,
        0.0, 1.0, 1.0, 1.0]

        self.program = compileProgram('data/MatrixPerspective.vert', 'data/StandardColors.frag', True)

        self.pMatrixUnif = glGetUniformLocation(self.program, "perspectiveMatrix")
        self.mMatrixUnif = glGetUniformLocation(self.program, "modelMatrix")

        self.vbo = createVertexArrayBuffer(self.vertexData)

        #self.vao_id = GLuint(0)
        #vertex_array_object.glGenVertexArrays(1, self.vao_id)
        #glBindVertexArray(self.vao_id.value)


        self.pMatrix = getProjectionMatrix(45,640, 480, 30.0, 0.5)
        self.mMatrix = getIdentityMatrix()

        self.rot = 15.0

        glUseProgram(self.program)
        glUniformMatrix4fv(self.pMatrixUnif, 1, GL_FALSE, self.pMatrix.data)
        glUseProgram(0)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)

        glViewport(0,0,640,480)
    def update(self, dt):
        self.mMatrix = getIdentityMatrix()
        self.mMatrix = self.mMatrix * getTranslationMatrix(0.0, 1.0, -5.0)
        self.mMatrix = self.mMatrix * getRotationMatrixY(self.rot)
        #self.rot += 0.05
        return 1

    def render(self):
        glClearColor(0.5, 0.5, 0.5, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.program)

         
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glUniformMatrix4fv(self.mMatrixUnif, 1, GL_FALSE, self.mMatrix.data)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(0, 4, GL_FLOAT, False, 0, c_void_p(0))
        glVertexAttribPointer(1, 4, GL_FLOAT, False, 0, c_void_p(144))
        glDrawArrays(GL_TRIANGLES, 0, 36)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glUseProgram(0)
        
        pygame.display.flip()


scene = 0

def cycle(info):
    scene.update(0)
    scene.render()
    

if __name__ == "__main__":
    c = Context("demo", (640, 480))
    scene = Scene()
    c.bindFunction(USEREVENT, cycle)

    c.run()

    
