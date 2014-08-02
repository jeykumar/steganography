#!/usr/bin/env python
import Image
from random import randrange
from math import floor

def openImage(f):
    img = Image.open(f)
    return img

def saveImage(img,f):
    img.save(f)
    
def openText(textFile):
    """Returns the contents of a text file as a string"""
    f = open(textFile, 'rU')
    string = f.read()
    return string

def getOrd(string):
    """Returns a list of ord(char) for char in string"""
    strList = list(string)
    ordList = [ord(x) for x in strList]
    return ordList

def binList(decList):
    binList = [list(bin(i)[2:].zfill(8)) for i in decList]
    for i in binList:
            i[:] = [int(j) for j in i]            
    return binList

def getImage():
    img = Image.new('RGB', (18,1), 'black')
    imgPixels = img.load()
    for j in range(img.size[1]):
        for i in range(img.size[0]):
            imgPixels[i,j] = (randrange(0,256),randrange(0,256),randrange(0,256))
    return img

def setLSB(n,bit):
    offMask = 0b11111110
    onMask = 0b1
    if bit == 0:
        return n & offMask
    else:
        return n | onMask
    
def getLSB(n):
    return int(bin(n)[-1])


def encode(img,string):
    img1 = img
    #img1.save('img6.png')
    img2 = img
    img2 = img2.convert("RGB")
    #print list(img2.getdata())
    imgPixels = img2.load()
    bList = binList(getOrd(string))
    RGB = []
    for j in range(img2.size[1]):
        for i in range(img2.size[0]):
            px = (img2.size[0]*(j+1)) - (img2.size[0]-(i+1)) - 1
            num = int(floor(px/3))
            for k in range(0,3):
                value = imgPixels[i,j][k]
                bit = 3*(px%3) + k
                if bit == 8:
                    if num == len(bList) - 1:
                        value = setLSB(value,0)
                        RGB.append(value)
                        RGB = [tuple(RGB[x:x+3]) for x in range(0,len(RGB),3)]
                        img2.putdata(RGB)
                        return img2
                    else:
                        value = setLSB(value,1)
                        RGB.append(value)
                else:
                    value = setLSB(value,bList[num][bit])
                    RGB.append(value)
                #print "Pixel %d's %d's value contain the %d character's %d bit" % (px, k, num, bit)
                
def decode(image):
    """Decodes a PNG image to a string"""
    img = Image.open(image)
    imgPixels = img.load()
    #Creates a nested list of RGB value tuples from the image pixel array
    sublists = []
    for j in range(img.size[1]):
        for i in range(img.size[0]):
            sublists.append(imgPixels[i,j])

    #Flattens the list of RGB value tuples
    values=[]
    for i in sublists:
        for j in i:
            values.append(j)

    #Remove END markers
    ordList = []
    for i in xrange(len(values)):
        if (i+1)%9==0 and getLSB(values[i]) == 0:
            break
        elif (i+1)%9!=0:
            ordList.append(values[i])
    ordList = [str(getLSB(i)) for i in ordList]
    ordList = ["".join(ordList[i:(i+8)]) for i in xrange(0,len(ordList),8)]
    ordList = [int(n,2) for n in ordList]
    
    #Creates a list with chr(num) for num (ASCII value) in ordList
    strList = [chr(x) for x in ordList]
    #Joins the list of characters to form encoded string
    string = "".join(strList)
    return string


if __name__ == '__main__':
    #img = getImage()
    #img.save('image.png')
    #encode(getImage(),'Python')
    #saveImage(encode(openImage('squirrel.jpg'),openText('invictus.txt')),'squirrel_enc.png')
    #saveImage(encode(openImage('squirrel.jpg'),"Hello World"),'squirrel_enc.png')
    #print binList([10,49,232])
    print decode('squirrel_enc.png')
    #print getLSB(11)
    print "Done"
    pass
