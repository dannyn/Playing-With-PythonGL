"""
    OpenGL helper functions

    Mostly wrappers around series of opengl calls which will get called
    over and over again and are called to acheive some common purpose.

    Also functions to deal with some of the ugly issues in using an API
    which relies on ctypes.
"""
from ctypes import *
import sys

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray
from OpenGL.GL.ARB import vertex_array_object

def createVertexArrayBuffer(vertexData):
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    array_type = (GLfloat * len(vertexData))
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4,  array_type(*vertexData), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo
