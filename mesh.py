#!/usr/bin/python2

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
import array
import numpy

import pygame
from pygame.locals import *

#  i dont remember where i stole this from
#  need to test on other platforms to see if its needed
'''try:
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
'''
from OpenGL.GL import *
from OpenGL.raw import GL
from OpenGL.arrays import ArrayDatatype as ADT

# todo: get rid of *'s
from glHelpers import *
from math3d import *
 
import util


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
                  'Ke':     getKe,
                  'map_Kd': notImplemented}
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

        if filename:
            self.load(filename)

    '''
        loads by state
        a group is a state
        faces loaded under a group belong to a state


        TODO:
            load faces with no group, no material, or any combination 
            thereof

            figure out what to do about the '0.0000000e' hack, why are 
            objs limited to that level or precision?

            some error checking and handling would also be nice, have it
            exit gracefully on bad data and not choke and crash like it
            does now.
    '''
    def load(self, filename):

        self.curMat  = None
        self.curGroup = None
    
        def getVertex(x): 
            
            data = re.findall('-?[0-9]+\.?[0-9]*e?-?[0-9]*', x)
            vertex = []
            for i,v in enumerate(data):
                if v == '0.0000000e':
                    vertex.append(0.0)
                else:
                    vertex.append(float(v))
            self.vertices.append(tuple(vertex))

        def getVertexNormal(x):
            data = re.findall('-?[0-9]+\.?[0-9]*e?-?[0-9]*', x)
            normal = []
            for i, n in enumerate(data):
                if n == '0.0000000e':
                    normal.append(0.0)
                else:
                    normal.append(float(n))
            self.vertexNormals.append(tuple(normal))

        def getVertexTex(x):
            0

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
                  'vt'         : getVertexTex,
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

    # here for debugging and because why not
    def renderImmediate(self):
        glBegin(GL_TRIANGLES)
        for name, g in self.groups.iteritems():
            color = list(self.materials[g.material]['Kd'])
            glColor3f(color[0], color[1], color[2])
            for f in g.faces:
                for v in f:
                    vIndex = v[0]
                    nIndex = v[2]
                    p = self.vertices[vIndex]
                    n = self.vertexNormals[nIndex]
                    glNormal3f(n[0],n[1],n[2])
                    glVertex3f(p[0],p[1],p[2])
        glEnd()


    # creates a Mesh object out of data loaded from an obj file
    def createMesh(self):
        m = Mesh()

        attrs = []
        indices = []
        
        for name, g in self.groups.iteritems():
            offset = len(attrs)
            gArray = self.createArraysFromGroup(g)
            gAttr = gArray[0]
            gInd  = [i + offset for i in gArray[1]]

            indices += gInd
            attrs   += gAttr
        return Mesh(attrs, indices)

    ''' 
        the real guts of the createMesh function are here

        go through each group and create all the vertex attributes
        used by that group along with a index list of all the vertices.

        the index list is meant to be GL_TRIANGLES

        the real trick of this function is that it keeps a list of the 
        attributes already created so if two vertices share the
        same attribute 
    '''
    def createArraysFromGroup(self, groupObj):
        attrs = []
        indices = []
        mat = self.materials[groupObj.material]
        color = list(mat['Kd'])
        curIndex = 0  
        indices = []
        # list of already created attrs
        createdAttrs = {}

        for f in groupObj.faces:
            for v in f:    
                vIndex = v[0]
                nIndex = v[2]
                a = VertexAttr(Vector3(self.vertices[vIndex]),
                               Vector3(color),
                               Vector3(self.vertexNormals[nIndex]))
                if vIndex in createdAttrs:
                    indices.append(createdAttrs[vIndex])
                else:
                    attrs.append(a)
                    indices.append(curIndex)
                    createdAttrs[vIndex] = curIndex
                    curIndex += 1

        return (attrs, indices)
'''
    internal representation of a mesh that works well with opengl VBOs

    a loader should have a function that returns one of these

    A mesh is made up of two parts, vertex attributes and a list of indices
    into them.  the indices are organzied so every three are a trianble.
'''
class VertexAttr:
    def __init__(self, p = Vector3(), c = Vector3(), n = Vector3()):
        self.posistion = Vector3(p)
        self.color     = Vector3(c)
        self.normal    = Vector3(n)
    def __str__(self):
        return str(self.posistion) + str(self.color) + str(self.normal)
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        # BUG 
        # if you do this != it doesnt call _eq_ on Vector3
        if self.posistion == other.posistion\
           and  self.color == other.color\
           and  self.normal == other.normal:
            return True
        return False

class Mesh:
    def __init__(self, attrs=None, indices=None):
        self.vertexAttrs = attrs
        self.vertexIndices = indices


    # for debugging
    def printToScreen(self):
        print '----------------------------------------------'
        for i in self.vertexIndices:
            print self.vertexAttrs[i].posistion, i

    def renderImmediate(self):
        glDisable(GL_CULL_FACE)
        glBegin(GL_TRIANGLES)

        for i in self.vertexIndices:
            # for conveincence
            c = self.vertexAttrs[i].color
            n = self.vertexAttrs[i].normal
            p = self.vertexAttrs[i].posistion
            glColor3f(c[0],c[1],c[2])
            glNormal3f(n[0],n[1],n[2])
            glVertex3f(p[0],p[1],p[2])
        glEnd()
    
    '''
        TODO: 
            interleaved arrays

            once VBOs are made and anything is processed out of it that is
            needed all that data loaded from the OBJ files has got to go
    '''
    def createVBO(self):

        flatten = lambda x: list(itertools.chain(*x))

        def makeBuffer(target, data):
            temp = glGenBuffers(1)
            glBindBuffer(target, temp)
            glBufferData(target, ADT.arrayByteCount(data), ADT.voidDataPointer(data), GL_STATIC_DRAW)
            glBindBuffer(target, 0)
            return temp
        

        #vertices = numpy.array([list(self.vertexAttrs[v].posistion) for v in self.vertexIndices],dtype = 'f')
        #normals  = numpy.array([list(self.vertexAttrs[v].normal) for v in self.vertexIndices],dtype = 'f')
        #colors   = numpy.array([list(self.vertexAttrs[v].color)  for v in self.vertexIndices],dtype = 'f')


        length = len(self.vertexAttrs)
        indices = numpy.array(self.vertexIndices, dtype='i')
        iVertices = numpy.array([list(self.vertexAttrs[v].posistion) for v in xrange(length)], dtype='f')
        iNormals  = numpy.array([list(self.vertexAttrs[v].normal) for v in xrange(length)], dtype='f')
        iColors   = numpy.array([list(self.vertexAttrs[v].color) for v in xrange(length)], dtype='f')

        self.vertexVBO = makeBuffer(GL_ARRAY_BUFFER, iVertices)
        self.normalVBO = makeBuffer(GL_ARRAY_BUFFER, iNormals)
        self.colorVBO  = makeBuffer(GL_ARRAY_BUFFER, iColors)

        self.indexVBO  = makeBuffer(GL_ELEMENT_ARRAY_BUFFER, indices)

    def render(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glBindBuffer(GL_ARRAY_BUFFER, self.vertexVBO)
        glVertexPointerf(None) 

        glBindBuffer(GL_ARRAY_BUFFER, self.normalVBO)
        glNormalPointer(GL_FLOAT, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.colorVBO)
        glColorPointerf(None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indexVBO)
        glDrawElements(GL_TRIANGLES, len(self.vertexIndices), GL_UNSIGNED_INT, None)

        #glDrawArrays(GL_TRIANGLES, 0, len(self.vertexIndices))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDisable(GL_VERTEX_ARRAY)
        glDisable(GL_NORMAL_ARRAY)
        glDisable(GL_COLOR_ARRAY)



# this is the prefered entry point into any of this 
def loadMesh(filename):
    mesh = ObjMeshLoader(filename).createMesh()

    mesh.createVBO()

    return mesh

if __name__ == "__main__":        
    mesh = ObjMeshLoader('data/colorcube.obj').createMesh()


