#### Bejeweled -- By Neil Barot
"""
Things I can add on:
# -- Need to do butterfly mode counter
# -- Need to add music
# -- Need to do reverse animation
# -- Need to do drop animation
# -- Need to do high scores -> sql database
# -- Need to do profile --> Text Field to enter name'
"""

## --> Good for now, I'll study instead.....


import random
import copy
import time
from Tkinter import *

def init():
    canvas.data.mode = "zen"
    canvas.data.playerName = "Player 1"
    canvas.data.disableTimerFired = False
    canvas.data.pressedPlay = False
    canvas.data.isGameOver = False
    canvas.data.isPaused = False
    canvas.data.isSelected = False
    canvas.data.score = 0
    canvas.data.pauseTime = 0
    canvas.data.scoreStart = 60
    canvas.data.levelNumber = 1
    canvas.data.scoreAdded = 0
    canvas.data.butterflyNumber = 0
    canvas.data.butterflyScore = 0
    canvas.data.classicLevels = [[1, 240, 200], [2, 180, 350], [3, 120, 500], [4, 60, 580], [5, 30, 630], [6, 30, 690], [7, 30, 760], [8,30, 840], [9,30, 930], [10,30,1030]] 
    canvas.data.startTime = time.time()
    canvas.data.colors = ["black", "white", "magenta", "green", "yellow", "orange", "red"]
    board = []
    boardrow = []
    for x in xrange(canvas.data.rows):
        for y in xrange(canvas.data.cols):
            index = random.randint(0, len(canvas.data.colors) -1)
            boardrow.append(canvas.data.colors[index])
        board.append(boardrow)
        boardrow = []
    canvas.data.board = createBoard()
    fixMatchedGems()
    redrawAll()

def startScreen():
    if(canvas.data.pressedPlay == False):
        canvas.create_rectangle(0, 0, canvas.data.canvasWidth, canvas.data.canvasHeight, fill="black")
        canvas.create_image(208, 65, image = canvas.data.titlePicture)
        canvas.create_rectangle(50, 150, 350, 250, fill="blue")
        canvas.create_text(200, 200, text="Classic Mode", font=("Helvetica", 18, "bold"), fill="white")  
        canvas.create_rectangle(50, 285, 350, 385, fill="red")
        canvas.create_text(200, 335, text="Zen Mode", font=("Helvetica", 18, "bold"), fill="white")  
        canvas.create_rectangle(50, 430, 350, 530, fill="dark green")
        canvas.create_text(200, 480, text="Blitz Mode", font=("Helvetica", 18, "bold"), fill="white")  
        canvas.create_rectangle(50, 565, 350, 665, fill="goldenrod")
        canvas.create_text(200, 610, text="Butterfly Mode", font=("Helvetica", 18, "bold"), fill="white")
##        canvas.create_rectangle(20, 690, 120, 720, fill="dark blue", outline="red")
##        canvas.create_text(70, 705, text="Profile", font=("Helvetica", 14, "bold"), fill="white")
##        canvas.create_rectangle(280, 690, 380, 720, fill="dark blue", outline="red")
##        canvas.create_text(330, 705, text="Scores", font=("Helvetica", 14, "bold"), fill="white")
##
        canvas.create_text(canvas.data.canvasWidth/2 - 105, 675 + 50, text="Press 'r' to restart", font=("Helvetica", 12, "bold"), fill="red")
        canvas.create_text(canvas.data.canvasWidth/2 + 95, 675+ 50, text="Press 'q' to end game", font=("Helvetica", 12, "bold"), fill="green")
        canvas.create_text(canvas.data.canvasWidth/2, 675+ 20, text="Press 'p' to pause", font=("Helvetica", 12, "bold"), fill="gold")


def createBoard():
    board = []
    boardrow = []
    for x in xrange(canvas.data.rows):
        for y in xrange(canvas.data.cols):
            index = random.randint(0, len(canvas.data.colors) -1)
            boardrow.append(canvas.data.colors[index])
        board.append(boardrow)
        boardrow = []
    return board

def fixMatchedGems():
    canvas.data.disableTimerFired = False
    while(findMatchingGems(False) != [] ):
        findMatchingGems(True)
        for x in xrange(len(canvas.data.board)):
            for y in xrange(len(canvas.data.board[x])):
                if(canvas.data.board[x][y] == -1):
                    tempRow = x
                    while(tempRow > 0):
                        canvas.data.board[tempRow][y] = canvas.data.board[tempRow-1][y]
                        tempRow -= 1
                    canvas.data.board[0][y] = canvas.data.colors[random.randint(0, len(canvas.data.colors) -1)]

def fixButterflies():
    for x in xrange(canvas.data.cols):
        if((canvas.data.board[1][x])[0:9] == "butterfly"):
            canvas.data.isGameOver = True
    for x in xrange(1, canvas.data.rows):
        for y in xrange(canvas.data.cols):
            if((canvas.data.board[x][y])[0:9] == "butterfly"):
                aGem = canvas.data.board[x-1][y]
                bGem = canvas.data.board[x][y]
                canvas.data.board[x-1][y] = bGem
                canvas.data.board[x][y] =  aGem 
                        
def swapGems(arow,acol,brow,bcol):
    if(not (abs(arow-brow) > 1) and not (abs(acol-bcol) > 1) and not ((abs(acol-bcol) == 1) and (abs(arow-brow) == 1))): 
        animatedSwap()
        time.sleep(.3)
    canvas.data.disableTimerFired = False
    aGem = canvas.data.board[arow][acol]
    bGem = canvas.data.board[brow][bcol]
    canvas.data.board[arow][acol] = bGem
    canvas.data.board[brow][bcol] =  aGem
    if(swapIsLegal(arow,acol,brow,bcol) == False):
        canvas.data.board[arow][acol] = aGem
        canvas.data.board[brow][bcol] = bGem
        return False
    return True     

def swapIsLegal(arow,acol,brow,bcol):
    canvas.data.gemsToRemove = findMatchingGems(False)
    if(abs(arow-brow) > 1):
        return False
    if(abs(acol-bcol) > 1):
        return False
    if((abs(acol-bcol) == 1) and (abs(arow-brow) == 1)):
        return False
    if(canvas.data.gemsToRemove == []):
        return False
    if((arow == brow) and (acol == bcol)):
        return False
    for x in xrange(len(canvas.data.gemsToRemove)):
        canvas.data.score += len(canvas.data.gemsToRemove[x])
        canvas.data.scoreAdded = int(len(canvas.data.gemsToRemove[x])/2)
        canvas.data.scoreStart += canvas.data.scoreAdded
    fixMatchedGems()
    if(canvas.data.mode == "butterfly"):
        fixButterflies()
        index = random.randint(0,canvas.data.cols-1)
        canvas.data.board[canvas.data.rows-1][index] = "butterfly"+canvas.data.board[canvas.data.rows-1][index]
        canvas.data.butterflyNumber += 1
    return True

def drawBoard():
    board = canvas.data.board
    for row in range(len(board)):
        for col in range(len(board[0])):
            drawCell(board, row, col,board[row][col])
    canvas.data.gemsToRemove =  findMatchingGems(False)

def findMatchingGems(yesAlias):
    gemsToRemove = [] 
    if(yesAlias):
        board = canvas.data.board
    else:
        board = copy.deepcopy(canvas.data.board)
    for x in xrange(canvas.data.rows):
        for y in xrange(canvas.data.cols):
            if(getGemAt(board, x, y) == getGemAt(board, x+1, y) == getGemAt(board, x+2, y)):
                targetGem = getGemAt(board, x, y)
                increment = 0
                currentRemove = []
                while getGemAt(board, x+increment, y) == targetGem:
                    currentRemove.append((x+increment, y))
                    board[x + increment][y] = -1
                    increment += 1
                gemsToRemove.append(currentRemove)
            if(getGemAt(board, x, y) == getGemAt(board, x, y+1) == getGemAt(board, x, y+2)):
                targetGem = getGemAt(board, x, y)
                increment = 0
                currentRemove = []
                while getGemAt(board, x, y+increment) == targetGem:
                    currentRemove.append((x, y+increment))
                    board[x][y + increment] = -1
                    increment += 1
                gemsToRemove.append(currentRemove)
    return gemsToRemove

def getGemAt(board, x, y):
    if x < 0 or y < 0 or x >= canvas.data.rows or y >= canvas.data.cols:
        return None
    else:
        if(board[x][y] == -1 or board[x][y][0:9] != "butterfly"):
            return board[x][y]
        else:
            return board[x][y][9::]

def drawStats():
        canvas.data.disableTimerFired = False
        cx = canvas.data.canvasWidth/2 -5 
        cy = 625
        lines = "Score: " + str(canvas.data.score)
        canvas.create_text(cx, cy, text=lines, font=("Helvetica", 18, "bold"), fill="white")
        cy = 675
        if((canvas.data.scoreStart - int((time.time() - canvas.data.startTime))) <= 0) and canvas.data.mode == "blitz":
            canvas.data.isGameOver = True
        if((canvas.data.classicLevels[canvas.data.levelNumber -1][1] -  int((time.time() - canvas.data.startTime))) <= 0) and canvas.data.mode == "classic":
            canvas.data.isGameOver = True
        if((canvas.data.classicLevels[canvas.data.levelNumber -1][2] <= canvas.data.score) and canvas.data.mode == "classic"):
            canvas.data.levelNumber += 1
            canvas.data.startTime = time.time()
        if(canvas.data.mode == "blitz"):
            timeremaining = "Time Remaining: " + str(canvas.data.scoreStart - int((time.time() - canvas.data.startTime))) + " seconds"
            canvas.create_text(cx, cy, text=timeremaining, font=("Helvetica", 18, "bold"), fill="white")
        elif(canvas.data.mode == "zen"):
            canvas.create_text(cx, cy, text="Zen Mode", font=("Helvetica", 18, "bold"), fill="white")
        elif(canvas.data.mode == "classic"):
            canvas.create_text(cx, cy-20, text="Classic Mode", font=("Helvetica", 18, "bold"), fill="white")
            canvas.create_text(cx, cy+10, text=("Level: "+str(canvas.data.levelNumber)), font=("Helvetica", 18, "bold"), fill="white")
            canvas.create_text(cx - 100, cy + 50, text=("Time Remaining: "+str(canvas.data.classicLevels[canvas.data.levelNumber -1][1] -  int((time.time() - canvas.data.startTime)))), font=("Helvetica", 12, "bold"), fill="red")
            canvas.create_text(cx+ 100, cy+ 50, text=("Score Needed: "+str(canvas.data.classicLevels[canvas.data.levelNumber -1][2])), font=("Helvetica", 12, "bold"), fill="green")
        elif(canvas.data.mode == "butterfly"):
            canvas.create_text(cx, cy-20, text="Butterfly Mode", font=("Helvetica", 18, "bold"), fill="white")
##            canvas.create_text(cx, cy+10, text="Butterflies: " + str(canvas.data.butterflyScore), font=("Helvetica", 18, "bold"), fill="white")
            canvas.create_text(cx, cy+10, text="Don't let the butterfly pieces reach the top!", font=("Helvetica", 12, "bold"), fill="red")
            canvas.create_text(cx, cy+40, text="Butterfly colors match the gems with the same color.", font=("Helvetica", 11, "bold"), fill="red")            
        canvas.create_image(208, 65, image = canvas.data.titlePicture)

def drawGame():
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + canvas.data.cols*cellSize
    canvasHeight = 2*margin + canvas.data.rows*cellSize 
    canvas.create_rectangle(0, 0, canvas.data.canvasWidth, canvas.data.canvasHeight, fill="black")
    drawBoard() 

def gemSelect():
    if(canvas.data.isSelected == False):
        canvas.data.rowSelected = canvas.data.rowClicked
        canvas.data.colSelected = canvas.data.colClicked
        canvas.data.isSelected = True
    else:
        canvas.data.isSelected = False
        findDirections()
        if(canvas.data.rowSelected >= 0 and canvas.data.rowSelected < canvas.data.rows and canvas.data.colSelected >= 0 and canvas.data.colSelected < canvas.data.cols) and (canvas.data.rowClicked >= 0 and canvas.data.rowClicked < canvas.data.rows and canvas.data.colClicked >= 0 and canvas.data.colClicked < canvas.data.cols):
            swapGems(canvas.data.rowSelected, canvas.data.colSelected, canvas.data.rowClicked, canvas.data.colClicked)
    
def drawCell(board,row,col,color):
    margin = 50
    cellSize = 30
    left = margin + col * cellSize
    right = left + cellSize
    top = (margin + row * cellSize)+80
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="black", outline="white")
    bordersize = 2 #incase you want to increase the border size in between each cell
    x = -1
    if(color == "white"):
        x = canvas.data.gem7Image
    elif(color == "black"):
        x = canvas.data.gem6Image
    elif(color == "magenta"):
        x = canvas.data.gem2Image
    elif(color == "green"):
        x = canvas.data.gem1Image
    elif(color == "yellow"):
        x = canvas.data.gem4Image
    elif(color == "orange"):
        x = canvas.data.gem3Image
    elif(color == "red"):
        x = canvas.data.gem5Image
    elif(color == "butterflywhite"):
        x = canvas.data.whiteButterfly
    elif(color == "butterflyblack"):
        x = canvas.data.blackButterfly
    elif(color == "butterflymagenta"):
        x = canvas.data.magentaButterfly
    elif(color == "butterflygreen"):
        x = canvas.data.greenButterfly
    elif(color == "butterflyyellow"):
        x = canvas.data.yellowButterfly
    elif(color == "butterflyorange"):
        x = canvas.data.orangeButterfly
    elif(color == "butterflyred"):
        x = canvas.data.redButterfly
    if(x != -1):    
        canvas.create_image(left, top, image=x, anchor = NW)
    if(canvas.data.isSelected):
        left = margin + canvas.data.colSelected * cellSize
        right = left + cellSize
        top = (margin + canvas.data.rowSelected * cellSize)+80
        bottom = top + cellSize
        if(canvas.data.rowSelected >= 0 and canvas.data.rowSelected < canvas.data.rows and canvas.data.colSelected >= 0 and canvas.data.colSelected < canvas.data.cols):
            canvas.create_rectangle(left+bordersize, top+bordersize, right-bordersize, bottom-bordersize, outline="magenta", width=1)


##################### Animation
def findDirections():
    canvas.data.colselectedDirection = 0
    canvas.data.rowselectedDirection = 0
    canvas.data.colclickedDirection = 0
    canvas.data.rowclickedDirection = 0
    if(canvas.data.colSelected+1 == canvas.data.colClicked):
        canvas.data.colselectedDirection = 1
        canvas.data.colclickedDirection = -1
    if(canvas.data.colSelected-1 == canvas.data.colClicked):
        canvas.data.colselectedDirection = -1
        canvas.data.colclickedDirection = 1
    if(canvas.data.rowSelected+1 == canvas.data.rowClicked):
        canvas.data.rowselectedDirection = 1
        canvas.data.rowclickedDirection = -1
    if(canvas.data.rowSelected-1 == canvas.data.rowClicked):
        canvas.data.rowselectedDirection = -1
        canvas.data.rowclickedDirection = 1

def animatedSwap():
    margin = 50
    cellSize = 30
    color = canvas.data.board[canvas.data.rowSelected][canvas.data.colSelected]
    colorClicked = canvas.data.board[canvas.data.rowClicked][canvas.data.colClicked]
    left = margin + canvas.data.colSelected * cellSize
    right = left + cellSize
    top = (margin + canvas.data.rowSelected * cellSize)+80
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="black", outline="white")
    left = margin + canvas.data.colClicked * cellSize
    right = left + cellSize
    top = (margin + canvas.data.rowClicked * cellSize)+80
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="black", outline="white")
    x = -1
    y = -1
    if(color == "white"):
        x = canvas.data.gem7Image
    elif(color == "black"):
        x = canvas.data.gem6Image
    elif(color == "magenta"):
        x = canvas.data.gem2Image
    elif(color == "green"):
        x = canvas.data.gem1Image
    elif(color == "yellow"):
        x = canvas.data.gem4Image
    elif(color == "orange"):
        x = canvas.data.gem3Image
    elif(color == "red"):
        x = canvas.data.gem5Image
    elif(color == "butterflywhite"):
        x = canvas.data.whiteButterfly
    elif(color == "butterflyblack"):
        x = canvas.data.blackButterfly
    elif(color == "butterflymagenta"):
        x = canvas.data.magentaButterfly
    elif(color == "butterflygreen"):
        x = canvas.data.greenButterfly
    elif(color == "butterflyyellow"):
        x = canvas.data.yellowButterfly
    elif(color == "butterflyorange"):
        x = canvas.data.orangeButterfly
    elif(color == "butterflyred"):
        x = canvas.data.redButterfly
    if(colorClicked == "white"):
        y = canvas.data.gem7Image
    elif(colorClicked == "black"):
        y = canvas.data.gem6Image
    elif(colorClicked == "magenta"):
        y = canvas.data.gem2Image
    elif(colorClicked == "green"):
        y = canvas.data.gem1Image
    elif(colorClicked == "yellow"):
        y = canvas.data.gem4Image
    elif(colorClicked == "orange"):
        y = canvas.data.gem3Image
    elif(colorClicked == "red"):
        y = canvas.data.gem5Image
    elif(colorClicked == "butterflywhite"):
        y = canvas.data.whiteButterfly
    elif(colorClicked == "butterflyblack"):
        y = canvas.data.blackButterfly
    elif(colorClicked == "butterflymagenta"):
        y = canvas.data.magentaButterfly
    elif(colorClicked == "butterflygreen"):
        y = canvas.data.greenButterfly
    elif(colorClicked == "butterflyyellow"):
        y = canvas.data.yellowButterfly
    elif(colorClicked == "butterflyorange"):
        y = canvas.data.orangeButterfly
    elif(colorClicked == "butterflyred"):
        y = canvas.data.redButterfly
    if(x != -1 and y != -1):
        left = margin + canvas.data.colSelected * cellSize
        top = (margin + canvas.data.rowSelected * cellSize)+80
        canvas.create_image(left, top, image=x, anchor = NW, tag = 'gemSelected')
        left = margin + canvas.data.colClicked * cellSize
        top = (margin + canvas.data.rowClicked * cellSize)+80
        canvas.create_image(left, top, image=y, anchor = NW, tag = 'gemClicked')
        canvas.data.disableTimerFired = True
        for a in xrange(cellSize):
            canvas.move('gemSelected', canvas.data.colselectedDirection, canvas.data.rowselectedDirection)
            canvas.move('gemClicked', canvas.data.colclickedDirection, canvas.data.rowclickedDirection)
            canvas.update()
    canvas.data.disableTimerFired = False
      
#####################

def redrawAll():
    canvas.data.disableTimerFired = False
    if (canvas.data.isGameOver):
        cx = canvas.data.canvasWidth/2 
        cy = canvas.data.canvasHeight/2 - 50
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"), fill="white")
    elif (canvas.data.isPaused):
        cx = canvas.data.canvasWidth/2
        cy = canvas.data.canvasHeight/2 - 50
        canvas.create_text(cx, cy, text="Game Paused!", font=("Helvetica", 32, "bold"), fill="white")
    else:
        canvas.delete(ALL)
        fixMatchedGems()
        drawGame()
        drawStats()
        startScreen()
       
def timerFired():
    delay = 900
    if(canvas.data.disableTimerFired == False):
        redrawAll()
        canvas.after(delay, timerFired)
    else:
        canvas.data.disableTimerFired = False
        canvas.after(delay, timerFired)

def keyPressed(event):
    if (event.char == "q" and canvas.data.pressedPlay == True):
        canvas.data.isGameOver = True
    elif (event.char == "r" and canvas.data.pressedPlay == True):
        init()
    elif (event.char == "p" and canvas.data.pressedPlay == True):
      if(canvas.data.isPaused):
          canvas.data.isPaused = False
          canvas.data.pauseTime = time.time() - canvas.data.pauseTime
          canvas.data.startTime += canvas.data.pauseTime
      else:
          canvas.data.isPaused = True
          canvas.data.pauseTime = time.time()
    redrawAll()

def Click(event):
    margin = 50
    cellSize = 30
    if(canvas.data.pressedPlay == False):
##        print event.x
##        print event.y
        if(event.x >= 50 and event.y >= 150 and event.x <= 350 and event.y <= 250):
            canvas.data.pressedPlay = True
            canvas.data.mode = "classic"
            canvas.data.startTime = time.time()
        elif(event.x >= 50 and event.y >= 285 and event.x <= 350 and event.y <= 385):
            canvas.data.pressedPlay = True
            canvas.data.mode = "zen"
        elif(event.x >= 50 and event.y >= 430 and event.x <= 350 and event.y <= 530):
            canvas.data.pressedPlay = True
            canvas.data.mode = "blitz"
            canvas.data.startTime = time.time()
        elif(event.x >= 50 and event.y >= 565 and event.x <= 350 and event.y <= 665):
            canvas.data.pressedPlay = True
            canvas.data.mode = "butterfly"
##        elif(event.x >= 20 and event.y >= 690 and event.x <= 120 and event.y <= 720):
##            print "profile"
##        elif(event.x >= 280 and event.y >= 690 and event.x <= 380 and event.y <= 720):
##            print "scores"
    else:
        canvas.data.colClicked = (event.x -margin)/cellSize
        canvas.data.rowClicked = ((event.y-10)/cellSize) - 4
        if(canvas.data.isGameOver == False):
            gemSelect()
    redrawAll()
  
def run(rows, cols):
    global canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize + 90
    canvasHeight = 2*margin + rows*cellSize + 280
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    root.canvas = canvas.canvas = canvas
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.instructionsPrinted = False
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.titlePicture = PhotoImage(file="bejeweledtitle.gif") #found from Google Images
    canvas.data.gem1Image = PhotoImage(file="gem1.gif") #from Osmic on opengameart.org
    canvas.data.gem2Image = PhotoImage(file="gem2.gif") #from Osmic on opengameart.org
    canvas.data.gem3Image = PhotoImage(file="gem3.gif") #from Osmic on opengameart.org
    canvas.data.gem4Image = PhotoImage(file="gem4.gif") #from Osmic on opengameart.org
    canvas.data.gem5Image = PhotoImage(file="gem5.gif") #from Osmic on opengameart.org
    canvas.data.gem6Image = PhotoImage(file="gem6.gif") #from Osmic on opengameart.org
    canvas.data.gem7Image = PhotoImage(file="gem7.gif") #from Osmic on opengameart.org
    canvas.data.whiteButterfly = PhotoImage(file="whitebutterfly.gif") 
    canvas.data.orangeButterfly = PhotoImage(file="orangebutterfly.gif") 
    canvas.data.yellowButterfly = PhotoImage(file="yellowbutterfly.gif") 
    canvas.data.redButterfly = PhotoImage(file="redbutterfly.gif") 
    canvas.data.magentaButterfly = PhotoImage(file="magentabutterfly.gif") 
    canvas.data.blackButterfly = PhotoImage(file="blackbutterfly.gif") 
    canvas.data.greenButterfly = PhotoImage(file="greenbutterfly.gif") 
    init()
    root.bind("<Key>", keyPressed)
    root.bind("<Button-1>", Click)
    if(canvas.data.isGameOver == False and canvas.data.isPaused == False):
        timerFired()
    root.title("Bejeweled -- By Neil Barot")
    root.lift()
    root.mainloop()

run(15,10)
