#!/usr/bin/python

####
#
# Shooting for a complete implementation as outlined here http://paulbourke.net/dataformats/obj/
#
####

import re

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

from glHelpers import *

class ObjMesh:

    def __init__(self, filename=0):
        self.isLoaded = False

        self.vertices = []
        self.faces = []
        self.textureVertices = []

        # groups['name'] = indices into face array
        self.groups = []
    
        self.vao = 0

        if filename:
            self.load(filename)

    def load(self, filename):

        curMat   = None
        curGroup = None

        getVertex = lambda x: self.vertices.append (tuple (re.findall('-?[0-9]+\.?[0-9]*', x)))
        getTextureVertex = lambda x: 0
        getVertexNormal = lambda x: 0
        getParamSpaceVertex = lambda x: 0
        getCsType = lambda x: 0
        getDegree = lambda x: 0 
        getBasisMatrix = lambda x: 0 
        getStepSize = lambda x: 0 
        getPoint = lambda x: 0 
        getLine = lambda x: 0 
        #getFace = lambda x: self.faces.append (tuple (re.findall('-?[0-9]/?[0-9]*/?/?[0-9]*', x)))
        # a little more complicated than just a regex
        def getFace(x):
            vertices = re.findall('[0-9]/?[0-9]*/?/?[0-9]*', x)
            for v in vertices:
                vertexData = re.findall('[0-9]+', v)
                if len(vertexData) == 1:
                    self.faces.append( (int(vertexData[0])-1,None, None,curMat,curGroup))
                elif len(vertexData) == 2:
                    self.faces.append( (int(vertexData[0])-1, None, int(vertexData[1])-1,curMat,curGroup))
                elif len(vertexData) == 3:
                    self.faces.append( (int(vertexData[0])-1, int(vertexData[1])-1, int(vertexData[2])-1,
                                        curMat,curGroup))
        
        getCurv = lambda x: 0
        get2dCurve = lambda x: 0
        getSurf = lambda x: 0 
        getParamValue = lambda x: 0
        getOuterTrim = lambda x: 0
        getInnerTrim = lambda x: 0 
        getSpecialCurve = lambda x: 0
        getSpecialPoint = lambda x: 0
        getEnd = lambda x: 0
        getConnect = lambda x: 0
        getGroupName = lambda x: 0
        getSmoothingGroup = lambda x: 0 
        getMergingGroup = lambda x: 0 
        getObjectName = lambda x: 0 
        getBevelInt = lambda x: 0 
        getColorInt = lambda x: 0 
        getDissolveInt = lambda x: 0 
        getLevelOfDetail = lambda x: 0
        getMaterialName = lambda x: 0 
        getMaterialLibrary = lambda x: 0 
        getShadowCasting = lambda x: 0 
        getRayTracing = lambda x: 0 
        getCurveApprox = lambda x: 0 
        getSurfaceApprox = lambda x: 0 

        tokens = {'v'          : getVertex,
                  'vt'         : getTextureVertex,
                  'vn'         : getVertexNormal,
                  'vp'         : getParamSpaceVertex,
                  'cstype'     : getCsType,
                  'deg'        : getDegree,
                  'bmat'       : getBasisMatrix,
                  'setp'       : getStepSize,
                  'p'          : getPoint,
                  'l'          : getLine,
                  'f'          : getFace,
                  'curv'       : getCurv,
                  'curv2'      : get2dCurve,
                  'surf'       : getSurf,
                  'param'      : getParamValue,
                  'trim'       : getOuterTrim,
                  'hole'       : getInnerTrim,
                  'scrv'       : getSpecialCurve,
                  'sp'         : getSpecialPoint,
                  'end'        : getEnd,
                  'con'        : getConnect,
                  'g'          : getGroupName,
                  's'          : getSmoothingGroup,
                  'mg'         : getMergingGroup,
                  'o'          : getObjectName,
                  'bevel'      : getBevelInt,
                  'c_interp'   : getColorInt,
                  'd_interp'   : getDissolveInt,
                  'lod'        : getLevelOfDetail,
                  'usemtl'     : getMaterialName,
                  'mtllib'     : getMaterialLibrary,
                  'shadow_obj' : getShadowCasting,
                  'trace_obj'  : getRayTracing,
                  'ctech'      : getCurveApprox,
                  'stech'      : getSurfaceApprox}

        try:
            fp = open(filename, 'r')
        except IOError:
            print "Unable to open ", filename
            sys.exit()

        for line in fp:
            if not re.match ('^#', line):
                tokens [ re.match('^\s*[a-z]+', line).group()](line)

        #print self.vertices
        #print self.faces
        print filename, " loaded."

    def createVertexArrayBuffer(self):

        # step 1: organize data in a way that opengl can use
        self.vertexData = []
        self.indices = []

        for p in self.vertices:
            for c in p:
                self.vertexData.append(float(c))
            self.vertexData.append(float(1.0))
        #######
        # when support for it is added, normals, colors, and textures will go here

        ######################

        for v in self.faces:
            self.indices.append(int(v[0]))


        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        array_type = (GLfloat * len(self.vertexData))
        glBufferData(GL_ARRAY_BUFFER, len(self.vertexData) * 4,  array_type(*self.vertexData), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        array_type = (GLint * len(self.indices))
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.indices) *4, array_type(*self.indices), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        print self.vertices
    def render(self):    
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,4,GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glDrawElements(GL_QUADS, len(self.indices),GL_UNSIGNED_INT, c_void_p(0) )

        #glBindBuffer(GL_ARRAY_BUFFER,0)

# for testing
if __name__ == "__main__":        
    pygame.init()
    screen = pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    m = ObjMesh('data/cube.obj')
    m.createVertexArrayBuffer()
