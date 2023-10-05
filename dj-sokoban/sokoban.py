import mido
import turtle
import numpy
import time

# linkes Turntable: links / rechts bewegen
# rechtes Turntable: hoch / runter bewegen
# Pfeile rechts unterhalb Turntables:
#   |> drücken für Linksdrehung hoch, Rechtsdrehung runter
#   <| drücken für Rechtsdrehung hoch, Linksdrehung runter
# OUT für Spiel beenden
# zyklische Pfeile direkt über OUT um Level zurückzusetzen

sc = turtle.Screen()
sc.bgcolor("black")
sc.setup(width=.9, height=.9)

turtle.register_shape("crate", ((1, 1), (1, -1), (-1, -1),
                      (-1, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)))
turtle.register_shape("sokoban", ((-2, 0), (-4, -2), (-2, 1),
                      (-2, -5), (2, 1), (2, -5), (-2, 1), (-1, 1), (-2, 2), (-2, 4), (-1, 5), (1, 5), (2, 4), (2, 2), (1, 1), (2, 1), (4, -2), (2, 0), (2, 1), (-2, 1)))

substeps = 8
stroke = 2
gridScale = 2.8
gridSize = 20 * gridScale

boards = []
lines = []
width = 0
height = 0
level = 0

grid = turtle.Turtle()
grid.color("white", "black")
grid.shape("square")
grid.shapesize(gridScale, gridScale, stroke)
grid.speed(speed=0)
grid.penup()

decoration = turtle.Turtle()
decoration.color("white")
decoration.pensize(stroke)
decoration.speed(0)
decoration.hideturtle()

# turtle.shape("turtle")
turtle.color("white")
turtle.speed(0)
turtle.hideturtle()
playerPosition = (0, 0)

halfGrid = gridSize/2
quartGrid = gridSize/4


def drawWall(x, y):
    def horizontal(_y):
        decoration.goto(x-halfGrid, _y)
        decoration.pendown()
        decoration.goto(x+halfGrid, _y)
        decoration.penup()

    def vertical(_x, _y):
        decoration.goto(_x, _y)
        decoration.pendown()
        decoration.goto(_x, _y+quartGrid)
        decoration.penup()

    horizontal(y-quartGrid)
    horizontal(y)
    horizontal(y+quartGrid)
    vertical(x-quartGrid, y-halfGrid)
    vertical(x+quartGrid, y-halfGrid)
    vertical(x-quartGrid, y)
    vertical(x+quartGrid, y)
    vertical(x, y-quartGrid)
    vertical(x, y+quartGrid)


def drawTarget(x, y):
    eightGrid = gridSize/8
    decoration.goto(x-quartGrid, y-quartGrid-eightGrid)
    decoration.pendown()
    decoration.goto(x-quartGrid-eightGrid, y-quartGrid-eightGrid)
    decoration.goto(x-quartGrid-eightGrid, y-quartGrid)
    decoration.penup()

    decoration.goto(x+quartGrid, y-quartGrid-eightGrid)
    decoration.pendown()
    decoration.goto(x+quartGrid+eightGrid, y-quartGrid-eightGrid)
    decoration.goto(x+quartGrid+eightGrid, y-quartGrid)
    decoration.penup()

    decoration.goto(x+quartGrid, y+quartGrid+eightGrid)
    decoration.pendown()
    decoration.goto(x+quartGrid+eightGrid, y+quartGrid+eightGrid)
    decoration.goto(x+quartGrid+eightGrid, y+quartGrid)
    decoration.penup()

    decoration.goto(x-quartGrid, y+quartGrid+eightGrid)
    decoration.pendown()
    decoration.goto(x-quartGrid-eightGrid, y+quartGrid+eightGrid)
    decoration.goto(x-quartGrid-eightGrid, y+quartGrid)
    decoration.penup()
    turtle.update()


while True:
    try:
        line = input()
    except EOFError:
        break
    width = len(line)
    if width == 0:
        continue
    boards.append([])
    try:
        while (len(line) == width):
            boards[level].append(line)
            line = input()
    except EOFError:
        break
    level += 1

print(boards)
level = 0

# def prepareRound():


def resetGame():
    turtle.clearscreen()
    sc.bgcolor("black")
    turtle.tracer(False)
    turtle.penup()


resetGame()
boxes = []


def toScreenPosition(gridX, gridY):
    return ((gridX - (width/2)) * gridSize + halfGrid, ((height/2) - gridY) * gridSize - halfGrid)


def isValidPosition(x, y):
    if x < 0 or x >= width or y < 0 or y >= height:
        return False
    print(x, y, width, height)
    if lines[y][x] == "w":
        return False
    return True


def containsBox(gridX, gridY):
    (x, y) = toScreenPosition(gridX, gridY)
    for box in boxes:
        if (x, y) == box.pos():
            return box
    return False


def setPlayerPosition(gridX, gridY):
    global playerPosition
    playerPosition = (gridX, gridY)
    (oldX, oldY) = turtle.pos()
    (newX, newY) = toScreenPosition(gridX, gridY)
    deltaX = (newX-oldX)/substeps
    deltaY = (newY-oldY)/substeps
    for i in range(substeps):
        turtle.goto(oldX + i*deltaX,
                    oldY + i*deltaY)
        turtle.update()
    turtle.goto(newX, newY)
    turtle.update()


def setPlayerAndBoxPosition(gridX, gridY, box, boxX, boxY):
    global playerPosition
    playerPosition = (gridX, gridY)
    (oldX, oldY) = turtle.pos()
    (newX, newY) = toScreenPosition(gridX, gridY)
    (oldBoxX, oldBoxY) = box.pos()
    (newBoxX, newBoxY) = toScreenPosition(boxX, boxY)
    deltaX = (newX-oldX)/substeps
    deltaY = (newY-oldY)/substeps
    for i in range(substeps):
        turtle.goto(oldX + i*deltaX,
                    oldY + i*deltaY)
        box.goto(oldBoxX+i*deltaX, oldBoxY+i*deltaY)
        turtle.update()
    turtle.goto(newX, newY)
    box.goto(newBoxX, newBoxY)
    turtle.update()


boxesStored = 0
isMoving = False
gameOver = False


def move(direction):
    global isMoving, boxesStored, level
    if isMoving:
        return
    isMoving = True
    (gridX, gridY) = playerPosition
    (newX, newY) = playerPosition
    (beyondNewX, beyondNewY) = playerPosition
    if direction == "left":
        newX -= 1
        beyondNewX -= 2
    if direction == "right":
        newX += 1
        beyondNewX += 2
    if direction == "down":
        newY += 1
        beyondNewY += 2
    if direction == "up":
        newY -= 1
        beyondNewY -= 2
    if not isValidPosition(newX, newY):
        isMoving = False
        return
    boxAtTarget = containsBox(newX, newY)
    if not boxAtTarget:
        setPlayerPosition(newX, newY)
        isMoving = False
        return
    if not isValidPosition(beyondNewX, beyondNewY):
        isMoving = False
        return
    boxBeyondTarget = containsBox(beyondNewX, beyondNewY)
    if not boxBeyondTarget:
        setPlayerAndBoxPosition(newX, newY, boxAtTarget,
                                beyondNewX, beyondNewY)
        if lines[newY][newX] == "t":
            boxesStored -= 1
        if lines[beyondNewY][beyondNewX] == "t":
            boxesStored += 1
        if len(boxes) == boxesStored:
            level += 1
            if level < len(boards):
                startRound()
                isMoving = False
                boxesStored = 0
                return
            turtle.clearscreen()
            sc.bgcolor("black")
            turtle.color("white")
            turtle.hideturtle()
            turtle.write("    GAME OVER    \nDu hast gewonnen!", align="center",
                         font=("Terminal", 24, "normal"))
            global gameOver
            gameOver = True
            time.sleep(5)
            level = 0
            resetGame()
            startRound()
            gameOver = False
    isMoving = False


def startRound():
    resetGame()
    global playerPosition, boxes, boxesStored, height, width, lines
    decoration.color("white", "black")
    decoration.pensize(stroke)

    lines = boards[level]
    height = len(lines)
    width = len(lines[0])
    print(height)
    decoration.goto(0, (height/2 + 1)*gridSize)
    decoration.write("Level " + str(level+1), align="center",
                     font=("Terminal", 24, "normal"))
    decoration.pendown()
    decoration.forward(0)
    decoration.penup()
    decoration.write("Level " + str(level+1), align="center",
                     font=("Terminal", 24, "normal"))

    for box in boxes:
        box.reset()
        box.hideturtle()
    boxesStored = 0
    boxes = []
    for (i, row) in enumerate(lines):
        y = ((height/2) - i) * gridSize - halfGrid
        if len(row) != width:
            break
        for (j, cell) in enumerate(row):
            x = (j - (width/2)) * gridSize + halfGrid
            grid.goto(x, y)
            grid.stamp()
            if cell == "p":
                playerPosition = (i, j)
                turtle.goto(x, y)
                turtle.showturtle()
            if cell == "b":
                box = turtle.Turtle()
                box.end_fill()
                box.goto(x, y)
                box.shape("crate")
                box.shapesize(quartGrid, quartGrid, stroke)
                box.color("white", "black")
                box.penup()
                box.speed(0)
                box.showturtle()
                boxes.append(box)
            if cell == "w":
                drawWall(x, y)
            if cell == "t":
                drawTarget(x, y)
            turtle.update()
    turtle.shape("sokoban")
    turtle.shapesize(gridScale*1.8, gridScale*1.8, stroke)
    turtle.color("white", "black")
    turtle.setheading(90)
    turtle.showturtle()
    grid.hideturtle()
    turtle.update()

    def up():
        move("up")

    def down():
        move("down")

    def left():
        move("left")

    def right():
        move("right")

    turtle.listen()

    turtle.onkey(up, "Up")
    turtle.onkey(down, "Down")
    turtle.onkey(left, "Left")
    turtle.onkey(right, "Right")
    turtle.onkey(lambda: startRound(), "r")


startRound()


threshold = 50
pyg = mido.Backend('mido.backends.pygame')
inport = pyg.open_input('Xponent MIDI 1') ##for Linux
#inport = mido.open_input("Xponent Audio   0")  ##for Windows
# numCol=0
inactivity = 0
inactive = False
leftacc = 0
rightacc = 0
mode = 'left'
while True:
    if isMoving:
        continue
    if gameOver:
        continue
    isActive = False
    for msg in inport.iter_pending():
        #print(msg)
        if inactive:
            print("reset")
            exit()
            inactive = False
        if msg.type == 'note_on' and (msg.note == 43 or msg.note == 18):
            exit()
        if msg.type == 'note_on' and msg.note == 42:
            startRound()
            break
        if msg.type == 'note_on' and msg.note == 16:
            mode = 'left'
        if msg.type == 'note_on' and msg.note == 17:
            mode = 'right'
        if msg.type == 'control_change' and msg.control == 22:
            isActive = True
            if (msg.channel % 5) == 0:
                leftacc += 2*(64-msg.value)
            elif (msg.channel % 5) == 1:
                rightacc += 2*(64-msg.value)
    if leftacc > threshold:
        move("left")
        leftacc = 0
        rightacc = 0
    if leftacc < -threshold:
        move("right")
        leftacc = 0
        rightacc = 0
    if rightacc > threshold:
        if mode == 'right':
            move("up")
        if mode == 'left':
            move("down")
        leftacc = 0
        rightacc = 0
    if rightacc < - threshold:
        if mode == 'right':
            move("down")
        if mode == 'left':
            move("up")
        leftacc = 0
        rightacc = 0

    if not isActive:
        inactivity += 1
    else:
        inactivity = 0

turtle.update()
turtle.done()
