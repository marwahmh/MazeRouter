import numpy as np
import re

class Cell:
    def __init__(self,L,X,Y,taken=0):
        self.taken = taken # 0 or 1
        self.point=(X,Y,L)
        self.H = 0
        self.G = 0
        self.F = 0
        self.parent=None
        self.children=[]
        
    def setF(self):
        self.F= self.H + self.G
        #return (self.f)
   # def move_cost(self,other):
    #    return 0 if self.value == '.' else 1




def MazeRouter(inFile):
    #reading input file
    infile=open(inFile)
    content=infile.read()
    infile.close()
    lines=content.split('\n')
    nets=[]
    nets2=[]
    h=[]

    for i in lines:
        nets.append(re.findall(r'\((.+?)\)', i, re.DOTALL))
    #print (nets)
    for i in range(len(nets)):
        nets2.clear()
        for j in nets[i]:
            h.clear()
            h=j.split(', ')
            for k in range(len(h)):
                h[k]=int(h[k])
            nets2.append(tuple(h))
            n=tuple(nets2)
        nets[i]=n
            
    #print(nets)       


    #get max layer from file

    #constants
    layers = int(input('Please enter the number of layers'))
    width = 101
    height = 101
    viaCost = 10
    #3d list representing the grid
    grid = [[[0 for k in range(layers)] for j in range(height)] for i in range(width)]
    
    #covert 3d entries to cells
    for i in range(width):
        for j in range(height):
            for k in range(layers):
                grid[i][j][k]= Cell(k,i,j,0)
                #grid[i][j][k]= 0
    #grid[9][9][1]=1
    #print(grid)


    #make it with priority (check the source with the shortest path)
    #for i in range(len(nets)):
     #   print('Path for net'+ str(i+1))
      #  for j in range(len(nets[i])-1):
       #     print(findPath(nets[i][j][0],nets[i][j][1],nets[i][j][2],nets[i][j+1][0],nets[i][j+1][1],nets[i][j+1][2],grid)) #every target becomes a source 
        #    #print(nets[i][j], nets[i][j+1])
    #print(nets[0][0])
    #findPath(nets[0][0][0],nets[0][0][1],nets[0][0][2],nets[0][1][0],
     #        nets[0][1][1],nets[0][1][2],grid) #every target becomes a source


    findPath(4,7,8,3,0,0,grid) #every target becomes a source
    print("path2")
    findPath(4,7,8,3,0,0,grid)
    print('path3')
    findPath(4,7,8,3,0,0,grid)
    #findPath(4,7,8,3,0,0,grid)
    #print('path5') #path shouldn't exist
    #findPath(4,7,8,3,0,0,grid)




    #findPath(1,0,0,4,1,1,grid)
    #print ('path')
    #findPath(1,0,0,2,1,1,grid)

    
    
def HeuristicF(sourcePoint, targetPoint): #the heuristic function calculates the manhattan ditance + the cost of vias between the layers (the cost of the path between current and target nodes)

        xDist = abs(targetPoint[0]-sourcePoint[0]) #horizontal distance
        yDist = abs(targetPoint[1]-sourcePoint[1]) #vertical distance
        zDist = abs(targetPoint[2]-sourcePoint[2])*10 #distance between layers

        return xDist+yDist+zDist
    
def findPath(L1,x1,y1,L2,x2,y2,grid):
    '''will check the path with the least f , there will be a list of all nodes,
    will check if the least one leads to the target, if no path found will check
    the rest of the nodes.
    The "Opened" is the list of nodes we choose current from - that is, it contains
    all the nodes we might be interested in looking at next.
    The "Closed" is the list of nodes we've already considered'''
    #print(L1)
    closed = [] #includes closed nodes (doesn't lead to any path) / we've already considered
    opened = [] #includes the possible next nodes
    path = []

    #grid[x1][y1][0] = 0
    #grid[x2][y2][0] = 0

    grid[x1][y1][L1].taken=1
    startCell = grid[x1][y1][L1]
    targetCell = grid[x2][y2][L2]
    currentCell = startCell
    opened.append(currentCell)
    print (currentCell.point)
    steps=0
    
    #while opened: #loop on possible next nodes
    while currentCell.point != targetCell.point:
        #currentCell= getminF(opened,startCell,targetCell)
        x_1 = currentCell.point[0]
        y_1 = currentCell.point[1]
        L_1 = currentCell.point[2]
        #print(L_1)

        #path.append(currentCell.point)         #AT THE END
        #print (currentCell.point)

        if currentCell.point == targetCell.point:
            #print (currentCell.point)
            #return path
            break
        #closed.append(currentCell)
        #opened.remove(currentCell)
        

        if int(L_1)%2 != 0: #odd layers M1,M3,M5... Horizontal
            #print(L_1)
            #right,left
            if grid[x_1+1][y_1][L_1].taken == 0:
              #  print('yes')
                currentCell.children.append(grid[x_1+1][y_1][L_1])
            if grid[x_1-1][y_1][L_1].taken == 0:
               # print('yes')
                currentCell.children.append(grid[x_1-1][y_1][L_1])
        else: #even layers M2,M4... Vertical
            #north,south
            #print(L_1)
            if grid[x_1][y_1+1][L_1].taken == 0:
               # print('yes')
                currentCell.children.append(grid[x_1][y_1+1][L_1])
            if grid[x_1][y_1-1][L_1].taken == 0:
               # print('yes')
                currentCell.children.append(grid[x_1][y_1-1][L_1])
        #up and down cells       
       # if (steps>3):
        #print('yes')
        if grid[x_1][y_1][L_1+1].taken == 0:
            currentCell.children.append(grid[x_1][y_1][L_1+1])
        if grid[x_1][y_1][L_1-1].taken == 0:
            currentCell.children.append(grid[x_1][y_1][L_1-1])

            
        Fmin = 20000
        Hmin =2000
        if (len(currentCell.children) != 0):
            print(len(currentCell.children))

            parent=currentCell

            for cell in currentCell.children:

                #if cell.taken==0:
                #find h
                cell.H = HeuristicF(cell.point,targetCell.point)
                #print(cell.H)
                #find g
                if cell.point[2] == currentCell.point[2]:
                    cell.G +=1 #if I am in the same layer the cost is 1
                else:
                    cell.G += 10 #I add a via to move to other layer
                        
                #update F
                cell.setF() 
                cell.parent = parent

                if cell.F < Fmin:
                    Fmin = cell.F
                    Hmin = cell.H
                    currentCell = cell
               # elif cell.F == Fmin:
               #     if cell.H < Hmin:
                #        currentCell = cell
                 #       Hmin = cell.H
                    
                        
                    
            currentCell.taken=1
            x_1 = currentCell.point[0]
            y_1 = currentCell.point[1]
            L_1 = currentCell.point[2]

            grid[x_1][y_1][L_1]= currentCell
            grid[parent.point[0]][parent.point[1]][parent.point[2]].children = []
                    
            steps+=1
           # print(steps)
            print (currentCell.point)
         #   print (targetCell.point)
      #  print(grid[x_1][y_1][L_1].taken)
        #print(len(currentCell.parent.children))
       #S print(len(grid[x_1][y_1][L_1].children))
    grid[x2][y2][L2].taken=0


MazeRouter('input file.txt')
