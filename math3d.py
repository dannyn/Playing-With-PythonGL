import sys
import math

"""
    0  4 8   12
    1  5 9   13
    2  6 10  14
    3  7 11  15
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
        # for now just assume its another 4x4 matrix
        return self
    
    # copy old opengl functions
    # this is maybe not correct, might have to make a new one and multiply this 
    # one by this
    # also, this function here might suck, probably should be  part of matrix stack
    def translate(self, x, y, z):
        self[12] += x
        self[13] += y
        self[14] += z

    def rotate(self, theta, x, y, z):

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
        
def getProjectionMatrix(width, height, zFar, zNear):
    frustrumScale = 1.0

    pMatrix = Matrix4( [0] * 16)
    pMatrix[0] = frustrumScale  * (float(height) / float(width))
    pMatrix[5] = frustrumScale
    pMatrix[10] = (zFar * zNear) / (zNear - zFar)
    pMatrix[11] = -1.0
    pMatrix[14] = (2 * zFar * zNear) / (zNear - zFar)

    return pMatrix


class MatrixStack:

    def __init__ (self):
        self.stack = [] 

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

def getRotationMatrix(theta, x, y, z):
    m = getIdentityMatrix()

    return m

def getScalingMatrix(x,y,z):
    m = getIdentityMatrix()

    m[0]  = x
    m[5]  = y
    m[10] = z
 
    return m


if __name__ == "__main__":

    m =  getIdentityMatrix()

    print m

    m.translate(1, 2, 3)

    print m


    p = m.transformVertex( (0,0,0,1))

    print p
