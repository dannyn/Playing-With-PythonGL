
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
from OpenGL.GLU import *
from OpenGL.GLUT import *

glCreateShader = gl.glCreateShader
glShaderSource = gl.glShaderSource
glShaderSource.argtypes = [c_int, c_int, POINTER(c_char_p), POINTER(c_int)]
glCompileShader = gl.glCompileShader
glGetShaderiv = gl.glGetShaderiv
glGetShaderiv.argtypes = [c_int, c_int, POINTER(c_int)]
glGetShaderInfoLog = gl.glGetShaderInfoLog
glGetShaderInfoLog.argtypes = [c_int, c_int, POINTER(c_int), c_char_p]
glDeleteShader = gl.glDeleteShader
glCreateProgram = gl.glCreateProgram
glAttachShader = gl.glAttachShader
glLinkProgram = gl.glLinkProgram
glGetError = gl.glGetError
glUseProgram = gl.glUseProgram
 
GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER = 0x8B31
GL_COMPILE_STATUS = 0x8B81
GL_LINK_STATUS = 0x8B82
GL_INFO_LOG_LENGTH = 0x8B84

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

            pygame.display.flip()

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


"""
    'Reverse' FPS Camera
"""
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

class Scene:

    def __init__(self):
        self.level = Level()
        self.snake = Snake()

        self.camera = Camera()

    def update(self, dt):
        return 1

    def render(self):
        glLoadIdentity()
        self.camera.point()
        self.level.render()
        self.snake.render()

class Level:

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        
        self.heightMap = [ [0 for x in range(self.width)] for y in range(self.height) ]
        glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
        glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
        glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
        gluPerspective(45.0, float(320)/float(200), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)


    def render(self):
        self.renderWireFrame()

    def renderWireFrame(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 1.0)

        for x in range(self.height-1):
            for y in range(self.height-1):
                glVertex3f(x,self.heightMap[x][y], y)
                glVertex3f(x+1,self.heightMap[x+1][y], y)
                glVertex3f(x+1,self.heightMap[x+1][y+1], y+1)
                glVertex3f(x,self.heightMap[x][y+1], y+1)

        glEnd()

class Snake:

    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4

    def __init__(self):
        self.body = []
        self.body.append((4,4))
    
    def render(self):
        for x, y in self.body:
            self.drawSegment(x, y)

    def drawSegment(self, x, y):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(x,  0,y)
        glVertex3f(x+1,0,y)
        glVertex3f(x+1,0,y+1)
        glVertex3f(x,  0,y+1)    
        glEnd()


"""          DEMO                """

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    source = c_char_p(source)
    length = c_int(-1)
    #buff = create_string_buffer(source) 
    #c_text = cast(pointer(pointer(buff)), POINTER(POINTER(GLchar)))
    #glShaderSource(shader,  c_text)
    glShaderSource(shader, 1, byref(source), byref(length))
    glCompileShader(shader)
    
    status = c_int()
    glGetShaderiv(shader, GL_COMPILE_STATUS, byref(status))
    if not status.value:
        print_log(shader)
        glDeleteShader(shader)
        raise ValueError, 'Shader compilation failed'
    return shader
 
def compile_program(vertex_source, fragment_source):
    vertex_shader = None
    fragment_shader = None
    program = glCreateProgram()
 
    if vertex_source:
        vertex_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
        glAttachShader(program, vertex_shader)
    if fragment_source:
        fragment_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
        glAttachShader(program, fragment_shader)
 
    glLinkProgram(program)
 
    if vertex_shader:
        glDeleteShader(vertex_shader)
    if fragment_shader:
        glDeleteShader(fragment_shader)
 
    return program
 
def print_log(shader):
    length = c_int()
    glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(length))
 
    if length.value > 0:
        log = create_string_buffer(length.value)
        glGetShaderInfoLog(shader, length, byref(length), log)
        print >> sys.stderr, log.value

scene = Scene()

def cycle(info):
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    scene.render()
    

if __name__ == "__main__":
    c = Context("demo", (640, 480))
    level = Level()

    c.bindFunction(USEREVENT, cycle)

    c.run()
    
