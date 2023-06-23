from decimal import *

class MandelImage:
    # MinX,MinY,MaxX,MaxY = String containing floating point numbers defining the Madlbrot image
    # XDots,YDots = Integers specifying the width and the height in pixels
    # numBits = Integer specify the number fo color bits per color
    def __init__ (self,MinX,MinY,MaxX,MaxY,XDots,YDots,numBits,highPrecision):
        self.numBits = numBits
        self.XDots=XDots 
        self.YDots=YDots 
        self.highPrecision = highPrecision
        self.SetUpCalc(MinX,MinY,MaxX,MaxY)
        self.Dots = []

    def CalcColorDot(self,x,y):
        if(self.highPrecision):
            dot = self.HighPColorDot(x,y)
        else:
            dot = self.LowPColorDot(x,y)
        return dot

    def CalcColorOneLine(self,y):
        for x in range(0,self.XDots):
            if(self.highPrecision):
                dot = self.HighPColorDot(x,y)
            else:
                dot = self.LowPColorDot(x,y)
            self.Dots.append(dot)
    #       print("Dot",dot)

    def CalcColorAll(self):
        for y in range(0,self.YDots):
            for x in range(0,self.XDots):
                if(self.highPrecision):
                    dot = self.HighPColorDot(x,y)
                else:
                    dot = self.LowPColorDot(x,y)
                self.Dots.append(dot)

    def SetUpCalc(self,MinX,MinY,MaxX,MaxY):
        if self.highPrecision:
            self.threshold = Decimal('100.0')
            self.MinA = Decimal(MinX)
            self.MaxA = Decimal(MaxX)
            self.MinDi = Decimal(MinY)
            self.MaxDi = Decimal(MaxY)
            self.AperDot = (Decimal(MaxX)-Decimal(MinX))/Decimal.from_float(float(self.XDots))
            self.DiperDot = (Decimal(MaxY)-Decimal(MinY))/Decimal.from_float(float(self.YDots))
        else:
            self.threshold = float('100.0')
            self.MinA = float(MinX)
            self.MaxA = float(MaxX)
            self.MinDi = float(MinY)
            self.MaxDi = float(MaxY)
            self.AperDot = (float(MaxX)-float(MinX))/(float(self.XDots))
            self.DiperDot = (float(MaxY)-float(MinY))/(float(self.YDots))
        

    def RePosition(self,MinX,MinY,MaxX,MaxY):
        self.SetUpCalc(MinX,MinY,MaxX,MaxY)
        self.Dots = []

    def HighPColorDot(self,x,y):
        a = self.HighPGetA(x)
        # DEBUG: print("AA:",a)
        di = self.HighPGetDi(y)
        numIters = 1<<(self.numBits*3)
        colorI = self.HighPGetColor(a,di,numIters)
        # DEBUG: print(colorI)
        colorStr = self.Inter2Color(self.numBits,colorI)
        return(colorStr)

    def LowPColorDot(self,x,y):
        a = self.LowPGetA(x)
        # DEBUG: print("AA:",a)
        di = self.LowPGetDi(y)
        numIters = 1<<(self.numBits*3)
        colorI = self.LowPGetColor(a,di,numIters)
        # DEBUG: print(colorI)
        colorStr = self.Inter2Color(self.numBits,colorI)
        return(colorStr)

    def HighPGetColor(self,c,di,numIters):
        for i in range(0,numIters):
            if i == 0:
                a=c
                bi=di
            else:
                newA=a*a-bi*bi-c
                newBi=Decimal('2.0')*a*bi-di
                a=newA
                bi=newBi
            if a>self.threshold:
                return i
        return 0

    def LowPGetColor(self,c,di,numIters):
        for i in range(0,numIters):
            if i == 0:
                a=c
                bi=di
            else:
                newA=a*a-bi*bi-c
                newBi=2.0*a*bi-di
                a=newA
                bi=newBi
            if a>self.threshold:
                return i
        return 0

    def HighPGetA(self,xDot):
        a = self.AperDot*Decimal.from_float(float(xDot)) + self.MinA
        return a
    def LowPGetA(self,xDot):
        a = self.AperDot*(float(xDot)) + self.MinA
        return a
    def HighPGetDi(self,yDot):
        di = self.MaxDi - self.DiperDot*Decimal.from_float(yDot)
        return di
    def LowPGetDi(self,yDot):
        di = self.MaxDi - self.DiperDot*float(yDot)
        return di
    def Inter2Color(self,numBits,i):
        if numBits == 4:
            str = "#%03x" % (i&0xfff)
        elif numBits == 5:
            str = "#%04x" % (i&0x7fff)
        elif numBits == 6:
            str = "#%05x" % (i&0x3ffff)
        elif numBits == 8:
            str = "#%06x" % (i&0xffffff)
        elif numBits == 12:
            str = "#%09x" & (i&0xfffffffff)
        else:
            print ("Error 1")
            raise Exception("Not a Valid Color Width")
        return str
    def GetDot(self,index):
        return(self.Dots[index])