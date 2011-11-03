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


class ObjVertex:
    # expects a tuple or a list
    # [x,y,z] or (x,y,z)
    def __init__(self, v):
        self.x = float(v[0])
        self.y = float(v[1])
        self.z = float(v[2])

    def vector4(self):
        return [self.x,self.y,self.z,1]

    def __str__(self):
        return '(' + self.x + ','+self.y+','+self.z+')'

class ObjFace:
    
    # expects vertices sent as a a list of lists or tupples
    # either (v), (v,t) (v,n,t) depending on whats available
    def __init__(self, face):
        self.vertexIndices = []
        self.normalIndices = []
        self.textureIndices =[]
            
        for point in face:
            v = re.findall('[0-9]+', point)
            self.vertexIndices.append(int(v[0]) - 1)
            if len(v) > 1:
                if len(v) == 3:
                    self.normalIndices.append(int(v[1]))
                    self.textureIndices.append(int(v[2]))
                else:
                    self.normalIndices.append(None)
                    self.textureIndices.append(int(v[1]))
        
        self.numVertices = len(self.vertexIndices)

        print self.vertexIndices , self.normalIndices, self.textureIndices

class ObjMesh:

    def __init__(self, filename=0):
        self.isLoaded = False

        self.vertices = []
        self.faces = []
        self.textureVertices = []
        self.groups = []
    
        self.vao = 0

        if filename:
            self.load(filename)

        self.colors = [ [1.0, 0.0, 1.0, 1.0],
                        [0.0, 1.0, 0.0, 1.0],
                        [0.0, 0.0, 1.0, 1.0],
                        [1.0, 1.0, 0.0, 1.0],
                        [0.0, 1.0, 1.0, 1.0],
                        [1.0, 0.0, 1.0, 1.0]]
    def load(self, filename):

        curMat   = None
        curGroup = None

        #getVertex = lambda x: self.vertices.append (tuple (re.findall('-?[0-9]+\.?[0-9]*', x)))
        def getVertex(x):
            v = tuple (re.findall('-?[0-9]+\.?[0-9]*', x))
            self.vertices.append(ObjVertex(v))
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
            f = re.findall('[0-9]/?[0-9]*/?/?[0-9]*', x)
            self.faces.append(ObjFace(f))
            #print vertices
            '''for v in vertices:
                vertexData = re.findall('[0-9]+', v)
                if len(vertexData) == 1:
                    self.faces.append( (int(vertexData[0])-1,None, None,curMat,curGroup))
                elif len(vertexData) == 2:
                    self.faces.append( (int(vertexData[0])-1, None, int(vertexData[1])-1,curMat,curGroup))
                elif len(vertexData) == 3:
                    self.faces.append( (int(vertexData[0])-1, int(vertexData[1])-1, int(vertexData[2])-1,
                                        curMat,curGroup))'''
             
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

        #for v in self.vertices:
        #    print v

        print filename, " loaded."

    def createVertexArrayBuffer(self):

        # step 1: organize data in a way that opengl can use
        self.vertexData = []
        self.indices = []

        for p in self.vertices:
            for c in p:
                self.vertexData.append(float(c))
            self.vertexData.append(float(1.0))
        for r,g,b,a in self.colors:
            self.vertexData.append(float(r))
            self.vertexData.append(float(g))
            self.vertexData.append(float(b))
            self.vertexData.append(float(a))
        self.vertexData.append(0.5)
        self.vertexData.append(0.5)
        self.vertexData.append(0.0) 
        self.vertexData.append(1.0)
        self.vertexData.append(0.0)
        self.vertexData.append(0.5) 
        self.vertexData.append(1.0) 
        self.vertexData.append(1.0)

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

        #print self.vertices
        #print self.indices
    def getVertexArray(self):

        # i think maybe this should be in its own function
        vertexData = []
        for face in self.faces:
            for i in range(face.numVertices):
                #print face.vertexIndices[i], self.vertices[face.vertexIndices[i]]
                vertexData.append(self.vertices[face.vertexIndices[i]].x)
                vertexData.append(self.vertices[face.vertexIndices[i]].y)
                vertexData.append(self.vertices[face.vertexIndices[i]].z)
                vertexData.append(1.0)

        print len(vertexData)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        array_type = (GLfloat * len(vertexData))
        glBufferData(GL_ARRAY_BUFFER, len(vertexData) ,  array_type(*vertexData), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def render(self):    
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,4,GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glDrawArrays(GL_TRIANGLES,0,36)

        glBindBuffer(GL_ARRAY_BUFFER,0)

# for testing
if __name__ == "__main__":        
    #pygame.init()
    #screen = pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    m = ObjMesh('data/cube.obj')
    m.getVertexArray()
    #m.createVertexArrayBuffer()
