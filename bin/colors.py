#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Mandelbrot Background : Color Selection
"""
import hjson

class ColorSelect:
    def __init__(self,topPath):
        self.current = 0
        self.colors = hjson.load(open(topPath + "colors/colors.hjson"))

    def GetDescriptions(self):
        return(self.colors["names"])

    def GetCurrent(self):
        return(self.current)

    def GetSelectedColor(self):
        #print (self.colors)
        selectedColor = SelectedColor(self.colors["settings"][self.current]["bits"],
                                self.colors["settings"][self.current]["blue_pos"],
                                self.colors["settings"][self.current]["green_pos"],
                                self.colors["settings"][self.current]["red_pos"],
                                self.colors["settings"][self.current]["default"]
                                      ) 
        return(selectedColor)


    def SetCurrent(self,newCurrent):
        self.current = newCurrent

class SelectedColor:
    def __init__(self,numBits,blue_pos,green_pos,red_pos,default):
        self.SetColor(numBits,blue_pos,green_pos,red_pos,default)

    def SetColor(self,numBits,blue_pos,green_pos,red_pos,default):
        self.numBits = numBits
        self.blue_pos = blue_pos 
        self.green_pos = green_pos 
        self.red_pos = red_pos 
        self.default = default 

    def GetNumBits(self):
        return(self.numBits)

    def Inter2Color(self,i):
        if i == 0:
            return(self.default)
        else:   
            rgbI = self.ConvertToRgbI(i)
            str = "#%06x" % (rgbI &0xffffff)
            return(str)

    def ConvertToRgbI(self,i):
        rgbI = 0
        redI = 0
        greenI = 0
        blueI = 0
        curBit = 0
        for curBit in range (0,self.numBits):
            if (i & (1<<curBit)) != 0:
                # add color
                if(self.blue_pos[curBit] >= 0):
                    blueI = blueI | (1<< self.blue_pos[curBit]) 
                if (self.green_pos[curBit] >= 0):
                    greenI = greenI | (1<< self.green_pos[curBit]) 
                if (self.red_pos[curBit] >= 0):
                    redI = redI | (1<< self.red_pos[curBit]) 
        rgbI = (redI << 16) | (greenI<<8) | blueI
        return rgbI