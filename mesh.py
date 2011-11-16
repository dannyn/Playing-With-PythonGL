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
import math
import random

import pygame
from pygame.locals import *

#  i dont remember where i stole this from
#  need to test on other platforms to see if its needed
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

#from OpenGL.GL import *
#from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray
#from OpenGL.GL.ARB import vertex_array_object

#import OpenGL
from glHelpers import *
from math3d import *


'''
    materials internally are a dictionary indexed by the material's name (newmtl)
'''
class ObjMaterials:
    def __init__(self, filename):
        self.loadMTLFile(filename)

    def __getitem__(self,key):
        return self.materials[key]

    def loadMTLFile(self, filename):

        def newMaterial(x):
            # this is a really, really, stupid way to do this
            # but i cant find a better way
            self.materials[self.curMat['Name']] = self.curMat
            self.curMat = self.getDefaultMat()
            name =  re.split('newmtl ',x)[1:]
            self.curMat['Name'] = name[0].rstrip()

        def getKs (x):
            l = re.findall('[0-9]+\.?[0-9]*',x)
            values = tuple([float(v) for v in l]) # convert all to float
            self.curMat['Ks'] =  values

        def getKd (x):
            l = re.findall('[0-9]+\.?[0-9]*',x)
            values = tuple([float(v) for v in l]) # convert all to float
            self.curMat['Kd'] =  values
        def getKa (x):
            l = re.findall('[0-9]+\.?[0-9]*',x)
            values = tuple([float(v) for v in l]) # convert all to float
            self.curMat['Ka'] =  values
        def getKe (x):
            l = re.findall('[0-9]+\.?[0-9]*',x)
            values =tuple([float(v) for v in l]) # convert all to float
            self.curMat['Ke'] =  values

        notImplemented = lambda x: 0


        self.materials = {}
        self.curMat = self.getDefaultMat()

        tokens = {'newmtl': newMaterial,
                  'Ns':     notImplemented,
                  'd' :     notImplemented,
                  'illum':  notImplemented,
                  'Kd':     getKd,
                  'Ka':     getKa,
                  'Ks':     getKs,
                  'Ke':     getKe}
        try:
            fp = open (filename, 'r')
        except:
            print "Unablge to open", filename
            sys.exit()

        for line in fp:
            if not re.match ('^#|^\s+$', line):
                tokens [ re.match('^\s*[A-Za-z]+', line).group()](line)

        self.materials[self.curMat['Name']] = self.curMat
        print 'Material file', filename, 'loaded.'

    ''' returns a default material to use
        think of it like a template '''
    def getDefaultMat(self):
        return { 'Name':  'Default',
                 'Ns':    100.0,
                 'd':     1.0,
                 'illum': 2,
                 'Kd':    (1.0, 1.0, 1.0),
                 'Ka':    (1.0, 1.0, 1.0),
                 'Ks':    (1.0, 1.0, 1.0),
                 'Ke':    (1.0, 1.0, 1.0)}  

    def __str__(self):
        s = '' 
        for m in self.materials:
            s += '------------\n' + m + '\n'
            for e in self[m]:
                s += e + ':'  + str(self[m][e]) + '\n'
        return s

class ObjGroup:

    def __init__(self, name):
        self.faces = []
        self.name = name
        self.materials = None

    # expects a face in v/t/n form
    def addFace(self, f):
        face = [re.split('/', vertex)  for vertex in f]
        # convert to int, not good, wont do texture v[1]
        # also subtract 1 because obj indices start at 
        # zero
        face = [[int(v[0])-1, v[1], int(v[2])-1]      for v in face] 
        self.faces.append(face)

    def setMaterial(self, matName):
        self.material = matName

    def __str__(self):
        s = ''
        s += self.name + '\n'
        for f in self.faces:
            s += str(f)
        return s

class ObjMeshLoader:

    def __init__(self, filename=0):
        self.isLoaded = False

        self.vertices = []
        self.faces = []
        self.vertexNormals = []
        self.groups = {}
    
        self.vao = 0

        if filename:
            self.load(filename)

    def load(self, filename):

        self.curMat  = None
        self.curGroup = None
    
        getVertex = lambda x: self.vertices.append (tuple([float(v)
            for v in re.findall('-?[0-9]+\.?[0-9]*e?-?[0-9]*', x)]))

        def getVertexNormal(x):
            n = re.findall('-?[0-9]+\.?[0-9]*e?-?[0-9]*', x)
            n = tuple([float(v) for v in n])
            self.vertexNormals.append(n)

        def getFace(x):
            f = re.findall('-?[0-9]/?[0-9]*/?/?[0-9]*', x)
            self.curGroup.addFace(f)
        getObjectName = lambda x: 0 

        def getMaterialName(x):
            matName = re.split('usemtl ',x)[-1].rstrip()
            self.curGroup.setMaterial(matName)
            
        def getMaterialLibrary(x):
            filename = re.split('mtllib ',x)[-1].rstrip()
            self.materials = ObjMaterials(filename)
            self.curMat = 'Default'      

        def setGroup(x):
            if self.curGroup:
                self.groups[self.curGroup.name] = self.curGroup
            name = re.split('g ', x)[-1].rstrip()
            self.curGroup = ObjGroup(name)

        notImplemented = lambda x: 0

        tokens = {'v'          : getVertex,
                  'vt'         : notImplemented,
                  'vn'         : getVertexNormal,
                  'vp'         : notImplemented,
                  'cstype'     : notImplemented,
                  'deg'        : notImplemented,
                  'bmat'       : notImplemented,
                  'setp'       : notImplemented,
                  'p'          : notImplemented,
                  'l'          : notImplemented,
                  'f'          : getFace,
                  'curv'       : notImplemented,
                  'curv2'      : notImplemented,
                  'surf'       : notImplemented,
                  'param'      : notImplemented,
                  'trim'       : notImplemented,
                  'hole'       : notImplemented,
                  'scrv'       : notImplemented,
                  'sp'         : notImplemented,
                  'end'        : notImplemented,
                  'con'        : notImplemented,
                  'g'          : setGroup,
                  's'          : notImplemented,
                  'mg'         : notImplemented,
                  'o'          : getObjectName,
                  'bevel'      : notImplemented,
                  'c_interp'   : notImplemented,
                  'd_interp'   : notImplemented,
                  'lod'        : notImplemented,
                  'usemtl'     : getMaterialName,
                  'mtllib'     : getMaterialLibrary,
                  'shadow_obj' : notImplemented,
                  'trace_obj'  : notImplemented,
                  'ctech'      : notImplemented,
                  'stech'      : notImplemented}

        try:
            fp = open(filename, 'r')
        except IOError:
            print "Unable to open ", filename
            sys.exit()

        for line in fp:
            if not re.match ('^#|^\s+$', line):
                tokens [ re.match('^\s*[a-z]+', line).group()](line)

        if self.curGroup:                
            self.groups[self.curGroup.name] = self.curGroup

        print "The file ", filename,"succesfully loaded."


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
        # i am using enumerate to know the index of the thing i am working on
        for i,v in enumerate(self.vertices) :
            p = Vector3( (float(v[0]), float(v[1]), float(v[2])))
            # calculate vertex normal
            # this isnt weighted, and may not be neccessary as some obj
            # files have this calculated
            # although, because of the way vertex indices work in obj files

            # and the way opengl wants them i have half a mind to always do it myself
            n = Vector3()
            for j,t in enumerate(trianglesIndexed):
                if i in t:
                    n = n + surfaceNormals[j]
            n = n.normalize()
            self.vertexAttrs.append(VertexAttr(p, None, n))

    # takes 3 vertexIndices and outputs them to a tuple of 
    # coordinates
    def createTriangle(self, t):
        return Vector3( (floatTuple(self.vertices[t[0]]), \
            floatTuple(self.vertices[t[1]]), floatTuple(self.vertices[t[2]])))

    def createMesh(self):
        m = Mesh()

        attrs = []
        indices = []
        
        for name, g in self.groups.iteritems():
            self.createArraysFromGroup(g)

    def createArraysFromGroup(self, groupObj):
        attrs = []
        indices = []
        # get color 
        # this is a huge for now, adding features off of materials goes here
        mat = self.materials[groupObj.material]
        color = list(mat['Kd'])
        print 'starting', color
        curIndex = 0
        indices = []
        for f in groupObj.faces:
            for v in f:    
                vIndex = v[0]
                nIndex = v[2]
                a = VertexAttr(Vector3(self.vertices[vIndex]),
                               Vector3(color),
                               Vector3(self.vertexNormals[nIndex]))
                # RIGHT HERE ******
                # need to check if a is already in attrs
                # if it is then just add another (appropriate)
                # index instead of creating another attr
                for i, t in enumerate(attrs):
                    if t == a:
                        indices.append(i)
                else:
                    attrs.append(a)
                    indices.append(curIndex)
                    curIndex += 1
                print a, indices

'''
    internal representation of a mesh that works well with opengl VBOs

    a loader should have a function that returns one of these
'''
class VertexAttr:
    def __init__(self, p = Vector3(), c = Vector3(), n = Vector3()):
        # should probably be try and then if it cant assume its already 
        # vector and just assign
        self.posistion = Vector3(p)
        self.color     = Vector3(c)
        self.normal    = Vector3(n)
    def __str__(self):
        return str(self.posistion) + str(self.color) + str(self.normal)
    def __eq__(self, other):
        # BUG 
        # if you do this != it doesnt call _eq_ on Vector3
        if self.posistion == other.posistion\
           and  self.color == other.color\
           and  self.normal == other.normal:
            return True
        return False

class Mesh:
    def __init__(self, filename=None):
        self.vertexAttrs = []
        self.vertexIndices = []


if __name__ == "__main__":        
    o = ObjMeshLoader('data/colorcube.obj')
    o.createMesh()
