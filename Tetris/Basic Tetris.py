
import random
import copy
from Tkinter import *

def init():
    printInstructions()
    canvas.data.isGameOver = False 
    board = []
    for x in xrange(canvas.data.rows):
        board.append(["blue"]*canvas.data.cols)
    canvas.data.emptyColor = "blue"
    canvas.data.tetrisBoard = board
    tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
    canvas.data.tetrisPieces = tetrisPieces()
    canvas.data.tetrisPieceColors = tetrisPieceColors
    canvas.data.score = 0
    newFallingPiece()
    redrawAll()
    
def printInstructions():
    print "Welcome to Tetris!"
    print "Use the arrow keys to move Left, Right, and Down."
    print "Press Up to rotate counter-clockwise"
    print "Press 'r' to restart."
    print "Press 'q' to end the game."

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
    index = random.randint(0, len(canvas.data.tetrisPieces)-1)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[index]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[index]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 - len(canvas.data.fallingPiece[0])/2

def drawFallingPiece():
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                drawCell(tetrisBoard, row+canvas.data.fallingPieceRow, col+canvas.data.fallingPieceCol,canvas.data.fallingPieceColor)

def moveFallingPiece(drow, dcol):
    initialrow = canvas.data.fallingPieceRow
    initialcol = canvas.data.fallingPieceCol
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if(fallingPieceIsLegal() == False):
        print "ILLEGAL MOVE"
        canvas.data.fallingPieceRow = initialrow
        canvas.data.fallingPieceCol = initialcol
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
            
def drawTetrisBoard():
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(tetrisBoard)):
        for col in range(len(tetrisBoard[0])):
            drawCell(tetrisBoard, row, col,tetrisBoard[row][col])

def redrawAll():
    removeFullRows()
    if (canvas.data.isGameOver == True):
        cx = canvas.data.canvasWidth/2
        cy = canvas.data.canvasHeight/2
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
    else:
        canvas.delete(ALL)
        drawGame()
        drawFallingPiece()
        drawScore()

def drawScore():
        cx = canvas.data.canvasWidth - 80
        cy = 20
        score = "Score: " +  str(canvas.data.score)
        canvas.create_text(cx, cy, text=score, font=("Helvetica", 12, "bold"), fill="white")    

def drawGame():
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + canvas.data.cols*cellSize
    canvasHeight = 2*margin + canvas.data.rows*cellSize
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="orange")
    drawTetrisBoard() 

def drawCell(board,row,col,color):
    margin = 5
    cellSize = 30
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="black")
    bordersize = 0 #incase you want to increase the space in between each cell
    canvas.create_rectangle(left+bordersize, top+bordersize, right-bordersize, bottom-bordersize, fill=color)

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

def rotateFallingPiece():
    oldPiece = canvas.data.fallingPiece
    oldRow = canvas.data.fallingPieceRow
    oldCol = canvas.data.fallingPieceCol
    oldCollen = len(canvas.data.fallingPiece[0])
    newCol = oldRow
    newRow = (oldCollen-1) - oldCol
    (oldCenterRow, oldCenterCol) = fallingPieceCenter()
    newPiece = turnCounterClockwise(oldPiece)
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

def removeFullRows():
    fullRows = 0
    newRow = canvas.data.rows-1
    for oldRow in xrange(canvas.data.rows-1, 0,-1):
        if(canvas.data.emptyColor in canvas.data.tetrisBoard[oldRow]):
            canvas.data.tetrisBoard[newRow] = copy.deepcopy(canvas.data.tetrisBoard[oldRow])
            newRow -= 1
        else:
            fullRows += 1
    for x in xrange(newRow-1, 0,-1):
        canvas.data.tetrisBoard[x] = [canvas.data.emptyColor]*canvas.data.cols
    canvas.data.score += (fullRows**2)*100
        
def timerFired():
    if(moveFallingPiece(1,0) == False):
        placeFallingPiece()
        newFallingPiece()
        if(fallingPieceIsLegal() == False):
            canvas.data.isGameOver = True
    redrawAll()
    delay = 600
    canvas.after(delay, timerFired)

def keyPressed(event):
    if (event.char == "q"):
        canvas.data.isGameOver = True
    elif (event.char == "r"):
        init()    
    if (canvas.data.isGameOver == False):
        if (event.keysym == "Down"):
            moveFallingPiece(1, 0)
        elif (event.keysym == "Left"):
            moveFallingPiece(0,-1)
        elif (event.keysym == "Right"):
            moveFallingPiece(0,1)
        elif (event.keysym == "Up"):
            rotateFallingPiece()
    redrawAll()
  
def run(rows, cols):
    global canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    root.canvas = canvas.canvas = canvas
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    init()
    root.bind("<Key>", keyPressed)
    if(canvas.data.isGameOver == False):
        timerFired()
    root.mainloop()
    
run(15,10)
