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
            print line

        print self.faces
        print self.vertices

class VertexAttr:
    def __init__(self, p = Vector3(), c = Vector3(), n = Vector3()):
        self.posistion = p
        self.color     = c
        self.normal    = n

    def toList(self):
        return 1

class Mesh:
    def __init__(self, filename=None):
        self.vertexAttrs = []
        self.vertexIndices = []

    def triangles(self):
        #http://code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples/ 
        return itertools.izip(*[itertools.islice(self.vertexIndices, i, None, 3) for i in range(3)])

if __name__ == "__main__":        
    m = ObjMeshLoader('data/cube.obj')
