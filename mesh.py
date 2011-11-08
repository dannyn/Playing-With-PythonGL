#!/usr/bin/python

####
#
# Shooting for a complete implementation as outlined here http://paulbourke.net/dataformats/obj/
#
####

import re
import itertools
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
from math3d import *

class ObjMeshLoader:

    def __init__(self, filename=0):
        self.isLoaded = False

        self.vertices = []
        self.faces = []
        self.vertexNormals = []
        self.groups = []
    
        self.vao = 0

        if filename:
            self.load(filename)

    def load(self, filename):

        curMat   = None
        curGroup = None

        getVertex = lambda x: self.vertices.append (tuple (re.findall('-?[0-9]+\.?[0-9]*', x)))
        getTextureVertex = lambda x: 0
        getVertexNormal = lambda x: self.vertexNormals.append( re.findall('-?[0-9]+\.?[0-9]*', x))
        getParamSpaceVertex = lambda x: 0
        getCsType = lambda x: 0
        getDegree = lambda x: 0 
        getBasisMatrix = lambda x: 0 
        getStepSize = lambda x: 0 
        getPoint = lambda x: 0 
        getLine = lambda x: 0 
        getFace = lambda x: self.faces.append (tuple (re.findall('-?[0-9]/?[0-9]*/?/?[0-9]*', x)))
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
            if not re.match ('^#|^\s+$', line):
                tokens [ re.match('^\s*[a-z]+', line).group()](line)
        print "The file ", filename,"succesfully loaded."

    def loadMTLFile(self, filename):
        return 0

    def createVertexIndex(self):
        ### this needs to be modified to sort itself so that
        ### faces which share vertices end up next to each
        ### other as much as possible
        self.vertexIndex = []

        for face in self.faces:
            for vertex in face:
                v = re.findall('[0-9]+', vertex)
                self.vertexIndex.append(int(v[0])-1)

    def createVertexNormals(self):
        surfNormals = []
        trianglesIndexed = zip(*[self.vertexIndex[i::3] for i in range(3)]) 
        trianglesCoords  = [self.createTriangle(t) for t in trianglesIndexed]
        surfaceNormals   = [calcSurfaceNormal(t) for t in trianglesCoords]
 
        self.vertexAttrs = []
        for i,v in enumerate(self.vertices) :
            p = Vector3( (float(v[0]), float(v[1]), float(v[2])))
            # calculate vertex normal
            # this isnt weighted, and may not be neccessary as some obj
            # files have this calculated
            # although, because of the way vertex indices work in obj files
            # and the way opengl wants them i have half a mind to always do it myself
            n = Vector3()
            for j,t in enumerate(trianglesIndexed):
                # if i is in t
                if i in t:
                    n = n + surfaceNormals[j]
            n = n.normalize()
            self.vertexAttrs.append(VertexAttr(p, None, n))

    # takes 3 vertexIndices and outputs them to a tuple of 
    # coordinates
    def createTriangle(self, t):
        return Vector3( (floatTuple(self.vertices[t[0]]), \
            floatTuple(self.vertices[t[1]]), floatTuple(self.vertices[t[2]])))

    def render(self):
        glBegin(GL_TRIANGLES)
        for v in self.vertexIndex:
            va = self.vertexAttrs[v]
            glColor3f(1.0, 0.0, 0.0)
            glNormal3f(va.normal[0], va.normal[1], va.normal[2])
            glVertex3f(va.posistion[0], va.posistion[1], va.posistion[2])
        glEnd()

class VertexAttr:
    def __init__(self, p = Vector3(), c = Vector3(), n = Vector3()):
        self.posistion = p
        self.color     = c
        self.normal    = n

    def toList(self):
        return 1

    def __str__(self):
        return str(self.posistion) + str(self.color) + str(self.normal)
class Mesh:
    def __init__(self, filename=None):
        self.vertexAttrs = []
        self.vertexIndices = []

    def triangles(self):
        #http://code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples/ 
        return itertools.izip(*[itertools.islice(self.vertexIndices, i, None, 3) for i in range(3)])

if __name__ == "__main__":        
    m = ObjMeshLoader('data/cube.obj')

    m.createVertexIndex()
    m.createVertexNormals()
    m.render()
