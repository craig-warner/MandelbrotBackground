from struct import pack

class BmpFile():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.b = Bitmap(self.width, self.height)
    def ColorImage(self,start_x,start_y,size,dots):
        dot_num = 0
        for y in range(0,size):
            for x in range(0,size):
                val_str = dots.GetDot(dot_num)
                # DEBUG: print (dot_num, "S:",val_str)
                val_str2 = val_str[1:]
                val = int(val_str2,16)
                val_red = ((val>>16) & 0xff)
                val_green = ((val>>8) & 0xff)
                val_blue = (val & 0xff)
                # DEBUG: print(val_red,val_blue,val_green)
                #print(val_red,val_blue,val_green)
                #print(start_x,start_y,x,y)
                self.b.setPixel(start_x+x,start_y+size-1-y,(val_red,val_green,val_blue))
                dot_num = dot_num + 1
    def Save(self,filename):
        self.b.write(filename)

class Bitmap():
    def __init__(s, width, height):
        s._bfType = 19778 # Bitmap signature
        s._bfReserved1 = 0
        s._bfReserved2 = 0
        s._bcPlanes = 1
        s._bcSize = 12
        s._bcBitCount = 24
        s._bfOffBits = 26
        s._bcWidth = width
        s._bcHeight = height
        s._bfSize = 26+s._bcWidth*3*s._bcHeight
        s.clear()

    def clear(s):
        s._graphics = [(0,0,0)]*s._bcWidth*s._bcHeight


    def setPixel(s, x, y, color):
        if isinstance(color, tuple):
            if x<0 or y<0 or x>s._bcWidth-1 or y>s._bcHeight-1:
                raise ValueError('Coords out of range')
            if len(color) != 3:
                raise ValueError('Color must be a tuple of 3 elems')
            s._graphics[y*s._bcWidth+x] = (color[2], color[1], color[0])
        else:
            raise ValueError('Color must be a tuple of 3 elems')

    def write(s, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL',
                   s._bfType,
                   s._bfSize,
                   s._bfReserved1,
                   s._bfReserved2,
                   s._bfOffBits)) # Writing BITMAPFILEHEADER
            f.write(pack('<LHHHH',
                   s._bcSize,
                   s._bcWidth,
                   s._bcHeight,
                   s._bcPlanes,
                   s._bcBitCount)) # Writing BITMAPINFO
            for px in s._graphics:
                f.write(pack('<BBB', *px))
            for i in range((4 - ((s._bcWidth*3) % 4)) % 4):
                f.write(pack('B', 0))
