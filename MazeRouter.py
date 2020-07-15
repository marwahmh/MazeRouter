def MazeRouter(inFile):
    #reading input file
    infile=open(inFile)
    content=infile.read()
    infile.close()
    nets=content.split('\n')
    print(nets)




    

MazeRouter('input file.txt')
