class Cell:
    def __init__(self,L,X,Y,taken=0):
        self.t = taken # 0 or 1
        #self.x= X
        #self.y= Y
        #self.layer = L
        self.point=(X,Y,L)
        self.H = 0
        self.G = 0
        self.F = 0
       # self.F = self.H + self.G
    def setF(self):
        self.F = self.G + self.H

hi=Cell(3,4,5,0)
hi.H=5
hi.G=10
hi.setF()
print(hi.F)
