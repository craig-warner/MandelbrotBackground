class Tplate:
    def __init__(self):
        self.default = 1
        self.descriptions = [
            "Left to Right, Enlarge, (3 images)",
            "Left to Right, Enlarge, (8 images)",
            "Left to Right, Enlarge, (11 images)",
            "Left to Right, Enlarge, (14 images)",
            "Big Center, (14 images)"
        ]
        self.filename= [
            "three_with_comments.hjson",
            "eight.json",
            "eleven.json",
            "fourteen.json",
            "center.json"
        ] 

    def GetAllTemplates(self):
        return(self.descriptions)

    def GetFilename(self,i):
        return(self.filename[i])

    def GetDefault(self):
        return(self.default)