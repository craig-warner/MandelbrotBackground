class Tplate:
    def __init__(self):
        self.default = 4
        self.descriptions = [
            "Big Center (17 images)",
            "Diagonal (17 images)",
            "Five (5 images)",
            "Left to Right, Enlarge, (3 images)",
            "Left to Right, Enlarge, (8 images)",
            "Left to Right, Enlarge, (11 images)",
            "Left to Right, Enlarge, (14 images)",
            "One (1 image)",
            "Two (2 images)"
        ]
        self.filename= [
            "center.json",
            "diagonal.hjson",
            "five.hjson",
            "three_with_comments.hjson",
            "eight.json",
            "eleven.json",
            "fourteen.json",
            "one.hjson",
            "two.hjson"
        ] 

    def GetAllTemplates(self):
        return(self.descriptions)

    def GetFilename(self,i):
        return(self.filename[i])

    def GetDefault(self):
        return(self.default)