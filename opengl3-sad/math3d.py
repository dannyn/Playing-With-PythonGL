import sys

from math import *


degToRad = 3.14158 * 2.0 / 360.0

class Vector4:
    def __init (self, x = 0, y = 0, z =0, w = 1):
        self.data[0] = x
        self.data[1] = y
        self.data[2] = z
        self.data[3] = w

    def __str__(self):
        return 1
    def __repr__(self):
        return 1

    def normalize(self):
        return 1
    def __add__(self):
        return 1
    def __sub__(self):
        return 1
    
"""
    Matrix is collumn major and is a single array indexed like so:

   [ 0  4 8   12 ]
   [ 1  5 9   13 ]
   [ 2  6 10  14 ]
   [ 3  7 11  15 ]
"""
class Matrix4:

    def __init__ (self, n=[0] * 16):
        self.data = n

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key, value):
        self.data[key] = value

    # todo: justify collumns
    def __str__ (self):
        s = ''
        for y in range(4):
            s += '|'
            for x in range(4):
                s +=  ' ' + str(self.data[x * 4 +y]) + ' ' 
            s += '|\n'
        return s

    # probably should look nice and justified as well
    def __repr__ (self):
        s = '['
        for n in self.data:
            s += ' ' + str(n) + ' '
        s += ']'
        return s

    
    def __mul__(self, other):
        product = Matrix4()

        # might as well just write all 16 elements of the new one out 
        # as its simpler and this needs to be as fast as possible anyway
        #  (dunno if the speed thing is valid for python but w/e)

        product[0]  = (self[0]  * other[0]) + (self[4]  * other[1]) \
                    + (self[8]  * other[2]) + (self[12] * other[3]) 
        product[1]  = (self[1]  * other[0]) + (self[5]  * other[1]) \
                    + (self[9]  * other[2]) + (self[13] * other[3]) 
        product[2]  = (self[2]  * other[0]) + (self[6]  * other[1]) \
                    + (self[10] * other[2]) + (self[14] * other[3]) 
        product[3]  = (self[3]  * other[0]) + (self[7]  * other[1]) \
                    + (self[11] * other[2]) + (self[15] * other[3]) 

        product[4]  = (self[0]  * other[4]) + (self[4]  * other[5]) \
                    + (self[8]  * other[6]) + (self[12] * other[7])
        product[5]  = (self[1]  * other[4]) + (self[5]  * other[5]) \
                    + (self[9]  * other[6]) + (self[13] * other[7])
        product[6]  = (self[2]  * other[4]) + (self[6]  * other[5]) \
                    + (self[10] * other[6]) + (self[14] * other[7])
        product[7]  = (self[3]  * other[4]) + (self[7]  * other[5]) \
                    + (self[11] * other[6]) + (self[15] * other[7])

        product[8]  = (self[0]  * other[8])  + (self[4]  * other[9])  \
                    + (self[8]  * other[10]) + (self[12] * other[11])
        product[9]  = (self[1]  * other[8])  + (self[5]  * other[9])  \
                    + (self[9]  * other[10]) + (self[13] * other[11])
        product[10] = (self[2]  * other[8])  + (self[6]  * other[9])  \
                    + (self[10] * other[10]) + (self[14] * other[11])
        product[11] = (self[3]  * other[8])  + (self[7]  * other[9])  \
                    + (self[11] * other[10]) + (self[15] * other[11])

        product[12] = (self[0]  * other[12]) + (self[4]  * other[13]) \
                    + (self[8]  * other[14]) + (self[12] * other[15])
        product[13] = (self[1]  * other[12]) + (self[5]  * other[13]) \
                    + (self[9]  * other[14]) + (self[13] * other[15])
        product[14] = (self[2]  * other[12]) + (self[6]  * other[13]) \
                    + (self[10] * other[14]) + (self[14] * other[15])
        product[15] = (self[3]  * other[12]) + (self[7]  * other[13]) \
                    + (self[11] * other[14]) + (self[15] * other[15])


        return product
    
    # copy old opengl functions
    # this is maybe not correct, might have to make a new one and multiply this 
    # one by this
    # also, this function here might suck, probably should be  part of matrix stack
    def translate(self, x, y, z):
        self[12] += x
        self[13] += y
        self[14] += z

    def rotate(self, theta, x, y, z):
        return 1
    # v is a vertex of the form (x,y,z,w)
    def transformVertex(self,v):
        x = v[0]
        y = v[1]
        z = v[2]
        w = v[3]

        xT = (self[0] * x) + (self[4] * y) + (self[8] * z)  + (self[12] * w)
        yT = (self[1] * x) + (self[5] * y) + (self[9] * z)  + (self[13] * w)
        zT = (self[2] * x) + (self[6] * y) + (self[10] * z) + (self[14] * w) 
        wT = (self[3] * x) + (self[7] * y) + (self[11] * z) + (self[15] * w)

        return (xT, yT, zT, wT)
        
def getProjectionMatrix(fov, width, height, zFar, zNear):

    fFovRad = fov * degToRad
    frustrumScale = 1.0# / tan(fFovRad / 2.0)

    pMatrix = Matrix4( [0] * 16)
    pMatrix[0] = frustrumScale  * (float(height) / float(width))
    pMatrix[5] = frustrumScale
    pMatrix[10] = (zFar * zNear) / (zNear - zFar)
    pMatrix[11] = -1.0
    pMatrix[14] = (2 * zFar * zNear) / (zNear - zFar)
    pMatrix[15] = 0

    return pMatrix


class MatrixStack:

    def __init__ (self):
        self.stack = [] 
        self.curMatrix = getIdentityMatrix()

    def push(self):
        self.stack.append(self.curMatrix)

    def pop(self):
        curMatrix = self.stack.pop()

    def translate(self, x, y, z):
        m = getTranslationMatrix(x, y, z)
        self.curMatrix *= m

    def rotate(self, theta, x, y, z):
        m = getRotationMatrix(theta, x, y, z)
        self.curMatrix *= m

    def scale(self, x, y, z):
        m = getScalingMatrix(x,y,z)
        self.curMatrix *= m

def getIdentityMatrix():
    return Matrix4( [1, 0, 0, 0, 
                     0, 1, 0, 0, 
                     0, 0, 1, 0,
                     0, 0, 0, 1]) 

def getTranslationMatrix(x,y,z):
    m = getIdentityMatrix()

    m[12] = x
    m[13] = y
    m[14] = z

    return m

# rotate theta degrees (randians?) around arbitrary vector (x,y,z)
def getRotationMatrix(theta, x, y, z):
    m = getIdentityMatrix()

    
    return m
def getRotationMatrixX(theta):
    m = getIdentityMatrix()
    
    theta = theta * degToRad

    m[5]  = cos(theta)
    m[6]  = sin(theta)
    m[9]  = -sin(theta)
    m[10] = cos(theta)
    return m

def getRotationMatrixY(theta):
    m = getIdentityMatrix()

    theta = theta * degToRad

    m[0] = cos(theta)
    m[2] = -sin(theta)
    m[8] = sin(theta)
    m[10] = cos(theta)
    return m

def getRotationMatrixZ(theta):
    m = getIdentityMatrix()

    theta = theta * degToRad
    m[0] = cos(theta)
    m[1] = sin(theta)
    m[4] = -sin(theta)
    m[5] = cos(theta)
    return m

def getScalingMatrix(x,y,z):
    m = getIdentityMatrix()

    m[0]  = x
    m[5]  = y
    m[10] = z
 
    return m


if __name__ == "__main__":




    m = getIdentityMatrix()

    print getTranslationMatrix(1,2,3)


