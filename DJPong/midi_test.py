import mido
import turtle
import numpy

sc = turtle.Screen()
sc.bgcolor("black")
screenTk = sc.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", True)
sc.setup(width=1.0, height=1.0)

left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("white")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup()
left_pad.goto(-560, 0)

right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("white")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(560, 0)

hit_ball = turtle.Turtle()
hit_ball.speed(0)
hit_ball.shape("square")
hit_ball.color("white")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 12
hit_ball.dy = -12

# Initialize the score
left_player = 0
right_player = 0


# Displays the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("white")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 350)
sketch.write(
    "Spieler*in 1: 0    Level: 1     Spieler*in 2: 0",
    align="center",
    font=("Terminal", 24, "normal"),
)

pyg = mido.Backend('mido.backends.pygame')
inport = pyg.open_input('Xponent MIDI 1') ##for Linux
#inport = mido.open_input("Xponent Audio   0")  ##for Windows
numCol = 0
inactivity = 0
inactive = False
level = 1
while True:
    lefty = 0
    righty = 0
    for msg in inport.iter_pending():
        if inactive:
            hit_ball.goto(0, 0)
            hit_ball.dx = 12
            hit_ball.dy = -12
            left_player = 0
            right_player = 0
            sketch.clear()
            sketch.write(
                "Spieler*in 1: 0    Level: 1     Spieler*in 2: 0",
                align="center",
                font=("Terminal", 24, "normal"),
            )
            level = 1
            inactive = False
        if msg.type == "control_change" and msg.control == 22:
            if (msg.channel % 5) == 1:
                lefty += 2 * (64 - msg.value)
            elif (msg.channel % 5) == 0:
                righty += 2 * (64 - msg.value)
        elif msg.type == "note_on" and msg.note == 18:
            exit()
    left_pad.sety(left_pad.ycor() + lefty)
    right_pad.sety(right_pad.ycor() + righty)
    if lefty == 0 and righty == 0:
        inactivity += 1
    else:
        inactivity = 0
    sc.update()

    if numCol == 3:
        hit_ball.dx = numpy.sign(hit_ball.dx) * (abs(hit_ball.dx) + 1)
        hit_ball.dy = numpy.sign(hit_ball.dy) * (abs(hit_ball.dy) + 1)
        numCol = 0
        level += 1
        sketch.clear()
        sketch.write(
            "Spieler*in 1: {}    Level: {}     Spieler*in 2: {}".format(
                left_player, level, right_player
            ),
            align="center",
            font=("Terminal", 24, "normal"),
        )

    new_x = hit_ball.xcor() + hit_ball.dx
    new_y = hit_ball.ycor() + hit_ball.dy
    hit_ball.goto(new_x, new_y)

    # Checking borders
    if hit_ball.ycor() > 370:
        hit_ball.sety(370)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -370:
        hit_ball.sety(-370)
        hit_ball.dy *= -1

    if hit_ball.xcor() > 700:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        left_player += 1
        sketch.clear()
        sketch.write(
            "Spieler*in 1: {}    Level: {}     Spieler*in 2: {}".format(
                left_player, level, right_player
            ),
            align="center",
            font=("Terminal", 24, "normal"),
        )
        numCol = 0
        level = 1
        hit_ball.dx = 12 * numpy.sign(hit_ball.dx)
        hit_ball.dy = 12 * numpy.sign(hit_ball.dy)

    if hit_ball.xcor() < -700:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        right_player += 1
        sketch.clear()
        sketch.write(
            "Spieler*in 1: {}    Level: {}     Spieler*in 2: {}".format(
                left_player, level, right_player
            ),
            align="center",
            font=("Terminal", 24, "normal"),
        )
        numCol = 0
        level = 1
        hit_ball.dx = 12 * numpy.sign(hit_ball.dx)
        hit_ball.dy = 12 * numpy.sign(hit_ball.dy)

    if (hit_ball.xcor() > 520 and hit_ball.xcor() < 521 + abs(hit_ball.dx)) and (
        hit_ball.ycor() < right_pad.ycor() + 60
        and hit_ball.ycor() > right_pad.ycor() - 60
    ):
        hit_ball.setx(520)
        hit_ball.dx *= -1
        numCol += 1

    if (hit_ball.xcor() < -520 and hit_ball.xcor() > -521 - abs(hit_ball.dx)) and (
        hit_ball.ycor() < left_pad.ycor() + 60
        and hit_ball.ycor() > left_pad.ycor() - 60
    ):
        hit_ball.setx(-520)
        hit_ball.dx *= -1
        numCol += 1

    if inactivity > 500:
        # exit to game selection screen
        exit()

    if left_pad.ycor() > 800:
        left_pad.sety(-800)
    if left_pad.ycor() < -800:
        left_pad.sety(800)
    if right_pad.ycor() > 800:
        right_pad.sety(-800)
    if right_pad.ycor() < -800:
        right_pad.sety(800)
