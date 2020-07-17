import numpy as np
import re





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
    width=1000
    height=1000
    viaCost= 10
    grid = np.empty([width, height,layers]) #array representing the grid
    print(grid)


    for i in range(len(nets)):
        print('Path for net'+ str(i+1))
        for j in range(len(nets[i])-1):
            findPath(nets[i][j][0],nets[i][j][1],nets[i][j][2],nets[i][j+1][0],nets[i][j+1][1],nets[i][j+1][2],grid) #every target becomes a source 
            print(nets[i][j], nets[i][j+1])
        

        
        
        

    
       
    

def HeuristicF(sourceLayer,sourceX, sourceY, targetLayer, targetX, targetY): #the heuristic function calculates the manhattan ditance + the cost of vias between the layers (the cost of the path between current and target nodes)

        xDist = abs(targetX-sourceX) #horizontal distance
        yDist = abs(targetY-sourceY) #vertical distance
        zDist= targetLayer-sourceLayer #distance between layers

        return xDist+yDist+zDist

    
def findPath(L1,x1,y1,L2,x2,y2,grid): #will check the path with the least f , there will be a list of all nodes, will check if the least one leads to the target, if no path found will check the rest of the nodes
#The "Open set" is the set of nodes we choose current from - that is, it contains all the nodes we might be interested in looking at next. The "Closed set" is the set of nodes we've already considered

    closed=[] #includes closed nodes (doesn't lead to any path) / we've already considered
    opened=[] #includes the possible next nodes
    path=[]

    startCell = (L1,x1,y1)
    targetCell = (L2,x2,y2)
    currentCell = startCell
    opened.append(currentCell)

    while opened: #loop on possible next nodes

        currentCell= getminF(opened,startCell,targetCell)
        
        if currentCell == targetCell:
            return path
        closed.append(currentCell)
        opened.remove(currentCell)

        if int(L1)%2 !=0 #odd layers M1,M3,M5... Horizontal
        
            children=[(L1,x1-1,y1),(L1,x1+1,y1),(L1+1,x1,y1),(L1-1,x1,y1)]

            for cell in children:
                if 

        else #even layers M2,M4... Vertical
            children=[(L1,x1,y1-1),(L1,x1+1,y1+1),(L1+1,x1,y1),(L1-1,x1,y1)]

        
        
            
def getminF (opened,startCell,targetCell): #########
    min=2000
    for cell in opened: #loop on each node and find the one with the least f ( heuristic function )
 
        H = HeuristicF(cell[0],cell[1],cell[2],targetCell[0],targetCell[1],targetCell[2])
        G=
        F=H+G

        if F < min:
            min = F
            chosenCell = cell


        
    
    
    



    

MazeRouter('input file.txt')
