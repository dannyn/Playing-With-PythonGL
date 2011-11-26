#!/usr/bin/env python2



from ctypes import *
import sys
import math

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

from math3d import *

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



''' implemented here as a 2d circle around the origin, 
    theta is the angle between r-> (of which self.r is the magnitude) and 
    the x axis.  this makes all rotations around the z axis.
'''
class Camera:
    def __init__(self):
        self.r = 5
        self.theta = 90

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
        glTranslatef(v[0], 0, v[1])

'''
    A scene handles all objects, is responsible for for updating them 
    and passing them off to the renderer. While it updates it builds a list
    of what to render and then ships it all off along with a camera 
    tranosformation.  

    Function to control the player will probably be linked into here. My inital
    idea is a list of commands that can be sent to a recievePlayerCmnd sort
    of function, this list can then get executed during an update.

    A game is resoponsible for dealing directly with any input.

    Starting to feel this might be redundant, and that there should be no 
    intermediary between the renderer (which draws) and the game (which 
    controls logic, updates, physics, etc...)
'''
class Scene():
    def __init__(self):
        self.rndr = Renderer()

     
class Renderable:

    def __init__(self): 0
    def render(self):   0

'''
    The 'physics' portion on an object
'''
class Entity:
    def __init__(self):
        rndrObj = Renderable()



'''
    Functions dealing with the loading, reading from disk,
    and compilation of shaders.
'''
def compileShader(source, shader_type):
    shader = glCreateShader(shader_type)
    source = c_char_p(source)
    length = c_int(-1)
    glShaderSource(shader, 1, byref(source), byref(length))
    glCompileShader(shader)
    status = c_int()
    glGetShaderiv(shader, GL_COMPILE_STATUS, byref(status))
    if not status.value:
        print_log(shader)
        glDeleteShader(shader)
        raise ValueError, 'Shader compilation failed'
    return shader

def compileProgram(vertexLocation, fragmentLocation, fromFile=False):
    vertex_shader = None
    fragment_shader = None
    program = glCreateProgram()
    if fromFile:
        if vertexLocation:
            vertexFile = open(vertexLocation, 'r')
            vertex_source = vertexFile.read()
            vertexFile.close()
        if fragmentLocation:
            fragmentFile = open(fragmentLocation, 'r')
            fragment_source = fragmentFile.read()
            fragmentFile.close()
    else:
        vertex_source = vertexLocation
        fragment_source = fragmentLocation
    if vertex_source:
        vertex_shader = compileShader(vertex_source, GL_VERTEX_SHADER)
        glAttachShader(program, vertex_shader)
        print 'Shader program', vertexLocation, 'succesfully compiled.'
    if fragment_source:
        fragment_shader = compileShader(fragment_source, GL_FRAGMENT_SHADER)
        glAttachShader(program, fragment_shader)
        print 'Shader program', fragmentLocation, 'succesfully compiled.'
    glLinkProgram(program)
    if vertex_shader:
        glDeleteShader(vertex_shader)
    if fragment_shader:
        glDeleteShader(fragment_shader)
    return program

# needs to be renamed
def print_log(shader):
    length = c_int()
    glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(length))

    if length.value > 0:
        log = create_string_buffer(length.value)
        glGetShaderInfoLog(shader, length, byref(length), log)
        print >> sys.stderr, log.value

