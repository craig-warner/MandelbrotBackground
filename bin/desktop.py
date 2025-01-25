class Desktop:
    def __init__(self):
        self.force_size = False 
        self.force_x = 0 
        self.force_y = 0 
        self.descriptions = [
            "128 x 108 (Test Size)",
            "640 x 360 (nHD)",
            "800 x 600 (SVGA)",
            "1024 x 768 (XGA)",
            "1280 x 720 (WXGA - 16:9)",
            "1280 x 800 (WXGA - 16:10)",
            "1280 x 1024 Super-eXtended Graphics Array (SXGA)",
            "1360 x 768 High Definition (HD - 1360 width)",
            "1366 x 768 High Definition (HD - 1366 width)",
            "1440 x 900 (WXGA+)",
            "1536 x 864 No Name",
            "1600 x 900 High Definition Plus (HD+)",
            "1600 x 1200 (UXGA)",
            "1680 x 1050 (WSXGA+)",
            "1920 x 1080 Full High Definition (FHD)",
            "1920 x 1200 Wide Ultra Extended Graphics Array (WUXGA)",
            "2048 x 1152 (QWXGA)",
            "2048 x 1536 (QXGA)",
            "2560 x 1080 (UWFHD)",
            "2560 x 1440 Quad High Definition (QHD)",
            "2560 x 1600 (WQXGA)",
            "3440 x 1440 Wide Quad High Definition (UWQHD)",
            "3840 x 2160 4K or Ultra High Definition (UHD)"]
        self.x_dots = [
            128,
            640,
            800,
            1024,
            1280,
            1280,
            1280,
            1360,
            1366,
            1440,
            1536,
            1600,
            1600,
            1680,
            1920,
            1920,
            2048,
            2048,
            2560,
            2560,
            2560,
            3440,
            3840
        ] 
        self.y_dots = [
            108,
            360,
            600,
            768,
            720,
            800,
            1024,
            768,
            768,
            900,
            864,
            900,
            1200,
            1050,
            1080,
            1200,
            1152,
            1536,
            1080,
            1440,
            1600,
            1440,
            2160
        ]
        self.default=14 # Most Popular: "1920 x 1080 Full High Definition (FHD)",

    def GetAllSizes(self):
        return(self.descriptions)

    def GetDefault(self):
        return(self.default)

    def GetPixelsPerUnitAndPads(self,xunits,yunits):
        width = self.GetXSize()
        height = self.GetYSize()
        pixels_per_unit_x = int(width / xunits)
        pixels_per_unit_y = int(height / yunits) 
        if(pixels_per_unit_x < pixels_per_unit_y):
            # use x   
            pixels_per_unit = pixels_per_unit_x
        else:
            pixels_per_unit = pixels_per_unit_y
        xpad = int((width - xunits*pixels_per_unit) / 2)  # Might be shifted left one pixel
        ypad = int((height - yunits*pixels_per_unit) / 2)  # Might be shifted up one pixel
        return(pixels_per_unit,xpad,ypad)

    def GetXSize(self):
        if self.force_size:
            return(self.force_x)
        else:
            return(self.x_dots[self.default])

    def GetYSize(self):
        if self.force_size:
            return(self.force_y)
        else:
            return(self.y_dots[self.default])

    def SetDefault(self,i):
        self.default=i 

    def SetDefaultWidthHeight(self, Width, Height):
        self.force_size=True 
        self.force_x = Width 
        self.force_y = Height 