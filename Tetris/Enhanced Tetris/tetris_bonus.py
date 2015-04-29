
import random
import copy
from Tkinter import *

#Hard Drop -- Done
#Pause Feature -- Done
#Dual Rotation -- Done
#Levels of Play -- (Drop Faster -- Done), (Different Piece Types -- Not Started), (Randomly Filled Blocks -- In Progress)
#Piece Preview -- Done
#Title Picture -- Done
#Ghost Piece -- Done
#Start Screen -- Not Started
#Sounds -- Not Started
#High Score -- Not Started


def init():
    if(canvas.data.instructionsPrinted == False):
        canvas.data.rotationDirection = printInstructions()
        canvas.data.instructionsPrinted = True
    canvas.data.isGameOver = False
    canvas.data.isPaused = False
    canvas.data.levelNumber = 1
    canvas.data.skipOne = False
    canvas.data.nextPieceIndex = -1
    canvas.data.lineCount = 0
    canvas.data.emptyColor = "blue"
    board = []
    for x in xrange(canvas.data.rows):
        board.append([canvas.data.emptyColor]*canvas.data.cols)
    canvas.data.tetrisBoard = board
    tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
    canvas.data.tetrisPieces = tetrisPieces()
    canvas.data.tetrisPieceColors = tetrisPieceColors
    canvas.data.nextPieceBoard = []
    for x in xrange(4):
        canvas.data.nextPieceBoard.append([canvas.data.emptyColor]*5)
    canvas.data.score = 0
    newFallingPiece()
    redrawAll()
  
    
def printInstructions():
    print "Welcome to Tetris!"
    print "Use the arrow keys to move Left, Right, and Down."
    print "Press Up to rotate the piece."
    print "Press Shift or Space Bar to hard drop."
    print "Press 'p' to pause."
    print "Press 'r' to restart."
    print "Press 'q' to end the game."
    print ""
    return raw_input("Enter 'cw' for clockwise rotation, or 'ccw' for counterclockwise rotation.\n")

def tetrisPieces():
    iPiece = [[ True,  True,  True,  True]]
    jPiece = [[ True, False, False ],[ True, True,  True]]
    lPiece = [[ False, False, True],[ True,  True,  True]]
    oPiece = [[ True, True],[ True, True]]
    sPiece = [[ False, True, True],[ True,  True, False ]]
    tPiece = [[ False, True, False ],[ True,  True, True]]
    zPiece = [[ True,  True, False ],[ False, True, True]]
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]    
    return tetrisPieces

def newFallingPiece():
    if(canvas.data.nextPieceIndex < 0):
        index = random.randint(0, len(canvas.data.tetrisPieces)-1)
        canvas.data.fallingPiece = canvas.data.tetrisPieces[index]
        canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[index]
    else:
        canvas.data.fallingPiece = canvas.data.tetrisPieces[canvas.data.nextPieceIndex]
        canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[canvas.data.nextPieceIndex]
    canvas.data.nextPieceIndex = random.randint(0, len(canvas.data.tetrisPieces)-1)
    canvas.data.nextFallingPiece= canvas.data.tetrisPieces[canvas.data.nextPieceIndex]
    canvas.data.nextFallingPieceColor = canvas.data.tetrisPieceColors[canvas.data.nextPieceIndex]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 - len(canvas.data.fallingPiece[0])/2

def drawStartScreen():
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + canvas.data.cols*cellSize
    canvasHeight = 2*margin + canvas.data.rows*cellSize 
    canvas.create_rectangle(0, 0, canvas.data.canvasWidth, canvas.data.canvasHeight, fill="black")

    
def drawFallingPiece():
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                drawCell(tetrisBoard, row+canvas.data.fallingPieceRow, col+canvas.data.fallingPieceCol,canvas.data.fallingPieceColor)

def drawGhostPiece():
    canvas.data.ghostPieceRow = int(canvas.data.fallingPieceRow)
    canvas.data.ghostPieceCol = int(canvas.data.fallingPieceCol)    
    while(moveGhostPiece(1,0)):
        None
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                drawGhostCell(tetrisBoard, row+canvas.data.ghostPieceRow, col+canvas.data.ghostPieceCol, canvas.data.fallingPieceColor)

def moveFallingPiece(drow, dcol):
    initialrow = canvas.data.fallingPieceRow
    initialcol = canvas.data.fallingPieceCol
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if(fallingPieceIsLegal() == False):
        canvas.data.fallingPieceRow = initialrow
        canvas.data.fallingPieceCol = initialcol
        return False
    return True

def moveGhostPiece(drow, dcol):
    initialrow = canvas.data.ghostPieceRow
    initialcol = canvas.data.ghostPieceCol
    canvas.data.ghostPieceRow += drow
    canvas.data.ghostPieceCol += dcol
    if(ghostPieceIsLegal() == False):
        canvas.data.ghostPieceRow = initialrow
        canvas.data.ghostPieceCol = initialcol
        return False
    return True

def placeFallingPiece():
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                canvas.data.tetrisBoard[row+canvas.data.fallingPieceRow][col+canvas.data.fallingPieceCol] = canvas.data.fallingPieceColor
    redrawAll()

def fallingPieceIsLegal():
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                if(row+canvas.data.fallingPieceRow >= canvas.data.rows) or (row+canvas.data.fallingPieceRow < 0):
                    return False
                if(col+canvas.data.fallingPieceCol >= canvas.data.cols) or (col+canvas.data.fallingPieceCol < 0):
                    return False
                if(tetrisBoard[row+canvas.data.fallingPieceRow][col+canvas.data.fallingPieceCol] != canvas.data.emptyColor):
                    return False
    return True

def ghostPieceIsLegal():
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                if(row+canvas.data.ghostPieceRow >= canvas.data.rows) or (row+canvas.data.ghostPieceRow < 0):
                    return False
                if(col+canvas.data.ghostPieceCol >= canvas.data.cols) or (col+canvas.data.ghostPieceCol < 0):
                    return False
                if(tetrisBoard[row+canvas.data.ghostPieceRow][col+canvas.data.ghostPieceCol] != canvas.data.emptyColor):
                    return False
    return True
            
def drawTetrisBoard():
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(tetrisBoard)):
        for col in range(len(tetrisBoard[0])):
            drawCell(tetrisBoard, row, col,tetrisBoard[row][col])

def drawNextPieceBoard():
    nextPieceBoard = canvas.data.nextPieceBoard
    for row in range(len(nextPieceBoard)):
        for col in range(len(nextPieceBoard[0])):
            drawCell(nextPieceBoard, row +17, col+5,nextPieceBoard[row][col])
    for row in range(len(canvas.data.nextFallingPiece)):
        for col in range(len(canvas.data.nextFallingPiece[0])):
            if(canvas.data.nextFallingPiece[row][col] == True):
                drawCell(nextPieceBoard, row+18, col+6,canvas.data.nextFallingPieceColor)

def redrawAll():
    removeFullRows()
    if (canvas.data.isGameOver):
        cx = canvas.data.canvasWidth/2 
        cy = canvas.data.canvasHeight/2 - 50
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
    elif (canvas.data.isPaused):
        cx = canvas.data.canvasWidth/2
        cy = canvas.data.canvasHeight/2 - 50
        canvas.create_text(cx, cy, text="Game Paused!", font=("Helvetica", 32, "bold"))
    else:
        canvas.delete(ALL)
        drawGame()
        drawGhostPiece()
        drawFallingPiece()
        drawStats()

def drawStats():
        cx = canvas.data.canvasWidth - 300
        cy = 650
        score = "Score: " +  str(canvas.data.score)
        canvas.create_text(cx, cy, text=score, font=("Helvetica", 14, "bold"), fill="white")
        cy = 690
        lines = "Lines Cleared: " + str(canvas.data.lineCount)
        canvas.create_text(cx, cy, text=lines, font=("Helvetica", 14, "bold"), fill="white")
        cy = 730
        levelnumber = "Level: " + str(canvas.data.levelNumber)
        canvas.create_text(cx, cy, text=levelnumber, font=("Helvetica", 14, "bold"), fill="white")
        canvas.create_text(cx+175, 610, text="Next Piece:", font=("Helvetica", 18, "bold"), fill="white")
        drawNextPieceBoard()
        canvas.create_image(198, 65, image = canvas.data.titlePicture)

def drawGame():
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + canvas.data.cols*cellSize
    canvasHeight = 2*margin + canvas.data.rows*cellSize 
    canvas.create_rectangle(0, 0, canvas.data.canvasWidth, canvas.data.canvasHeight, fill="black")
    drawTetrisBoard() 

def drawCell(board,row,col,color):
    margin = 50
    cellSize = 30
    left = margin + col * cellSize
    right = left + cellSize
    top = (margin + row * cellSize)+80
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="black")
    bordersize = 0 #incase you want to increase the border size in between each cell
    canvas.create_rectangle(left+bordersize, top+bordersize, right-bordersize, bottom-bordersize, fill=color)

def drawGhostCell(board,row,col,color):
    margin = 50
    cellSize = 30
    left = margin + col * cellSize
    right = left + cellSize
    top = (margin + row * cellSize)+80
    bottom = top + cellSize
    bordersize = 1 #incase you want to increase the border size in between each cell
    canvas.create_rectangle(left+bordersize, top+bordersize, right-bordersize, bottom-bordersize, fill=canvas.data.emptyColor, outline=color)

def turnCounterClockwise(piece):
    sublist = []
    rotatedPiece = []
    for x in xrange(len(piece[0])):
        for y in xrange(len(piece)):
            sublist.append(piece[y][x])
        rotatedPiece.append(sublist)
        sublist = []
    rotatedPiece.reverse()
    return rotatedPiece

def turnClockwise(piece):
    sublist = []
    rotatedPiece = []
    for x in xrange(len(piece[0])):
        for y in xrange(len(piece)):
            sublist.append(piece[y][x])
        sublist.reverse()
        rotatedPiece.append(sublist)
        sublist = []
    return rotatedPiece

def rotateFallingPiece():
    oldPiece = canvas.data.fallingPiece
    oldRow = canvas.data.fallingPieceRow
    oldCol = canvas.data.fallingPieceCol
    oldCollen = len(canvas.data.fallingPiece[0])
    newCol = oldRow
    newRow = (oldCollen-1) - oldCol
    (oldCenterRow, oldCenterCol) = fallingPieceCenter()
    if(canvas.data.rotationDirection == "ccw"):
        newPiece = turnCounterClockwise(oldPiece)
    else:
        newPiece = turnClockwise(oldPiece)
    canvas.data.fallingPiece = newPiece
    canvas.data.fallingPieceRow = newRow
    canvas.data.fallingPieceCol = newCol
    (newCenterRow, newCenterCol) = fallingPieceCenter() 
    canvas.data.fallingPieceRow += oldCenterRow - newCenterRow
    canvas.data.fallingPieceCol += oldCenterCol - newCenterCol
    if(fallingPieceIsLegal()):
        drawFallingPiece()
    else:
        canvas.data.fallingPiece = oldPiece
        canvas.data.fallingPieceRow = oldRow
        canvas.data.fallingPieceCol = oldCol        

def fallingPieceCenter():
    row = canvas.data.fallingPieceRow + len(canvas.data.fallingPiece)/2
    col = canvas.data.fallingPieceCol + len(canvas.data.fallingPiece[0])/2
    return (row,col)

def fillRandomSpot():
    x = random.randint(0, len(canvas.data.tetrisBoard))
    y = random.randint(0, len(canvas.data.tetrisBoard[x]))
    canvas.data.tetrisBoard[x][y] = "gray74"
    redrawAll()

def removeFullRows():
    fullRows = 0
    newRow = canvas.data.rows-1
    for oldRow in xrange(canvas.data.rows-1, 0,-1):
        if(canvas.data.emptyColor in canvas.data.tetrisBoard[oldRow]):
            canvas.data.tetrisBoard[newRow] = copy.deepcopy(canvas.data.tetrisBoard[oldRow])
            newRow -= 1
        else:
            fullRows += 1
            canvas.data.lineCount += 1
    for x in xrange(newRow-1, 0,-1):
        canvas.data.tetrisBoard[x] = [canvas.data.emptyColor]*canvas.data.cols
    canvas.data.score += (fullRows**2)*100
        
def timerFired():
    if(canvas.data.isPaused == False and moveFallingPiece(1,0) == False):
        placeFallingPiece()
        newFallingPiece()
        if(fallingPieceIsLegal() == False):
            canvas.data.isGameOver = True
    redrawAll()
    delay = checkLevel()
    canvas.after(delay, timerFired)
    canvas.data.skipOne = False

def checkLevel():
    if(canvas.data.score >= 7500):
        dropSpeed = 50
        canvas.data.levelNumber = 12
    elif(canvas.data.score >= 7000):
        dropSpeed = 100
        canvas.data.levelNumber = 11
    elif(canvas.data.score >= 6500):
        dropSpeed = 150
        canvas.data.levelNumber = 10
    elif(canvas.data.score >= 6000):
        dropSpeed = 200
        canvas.data.levelNumber = 9
    elif(canvas.data.score >= 5500):
        dropSpeed = 250
        canvas.data.levelNumber = 8
    elif(canvas.data.score >= 5000):
        dropSpeed = 300
        canvas.data.levelNumber = 7
    elif(canvas.data.score >= 4500):
        dropSpeed = 350
        canvas.data.levelNumber = 6
    elif(canvas.data.score >= 4000):
        dropSpeed = 400
        canvas.data.levelNumber = 5
    elif(canvas.data.score >= 3500):
        dropSpeed = 450
        canvas.data.levelNumber = 4
    elif(canvas.data.score >= 3000):
       dropSpeed = 500
       canvas.data.levelNumber = 3
    elif(canvas.data.score >= 2000):
        dropSpeed = 550
        canvas.data.levelNumber = 2
    else:
        dropSpeed = 600
        canvas.data.levelNumber = 1
    return dropSpeed


def keyPressed(event):
    if (event.char == "q"):
        canvas.data.isGameOver = True
    elif (event.char == "r"):
        init()
    elif (event.char == "p"):
      if(canvas.data.isPaused):
          canvas.data.isPaused = False
      else:
          canvas.data.isPaused = True
    if(canvas.data.isGameOver == False and canvas.data.isPaused == False):
        if(canvas.data.skipOne == False):
            if (event.keysym == "Down"):
                moveFallingPiece(1, 0)
            elif (event.keysym == "Left"):
                moveFallingPiece(0,-1)
            elif (event.keysym == "Right"):
                moveFallingPiece(0,1)
            elif (event.keysym == "Up"):
                rotateFallingPiece()
            elif (event.keysym == "Shift_R" or event.keysym == "Shift_L" or event.keysym == "space"):
                while(moveFallingPiece(1,0)):
                    redrawAll()
                canvas.data.skipOne = True
    redrawAll()
  
def run(rows, cols):
    global canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize + 90
    canvasHeight = 2*margin + rows*cellSize + 350
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
    canvas.data.titlePicture = PhotoImage(file="tetristitle.gif") #found from Google Images
    init()
    root.bind("<Key>", keyPressed)
    if(canvas.data.isGameOver == False and canvas.data.isPaused == False):
        timerFired()
    root.title("Tetris -- By Neil Barot")
    root.lift()
    root.mainloop()


run(15,10)
