import mido
import turtle
import time 

sc = turtle.Screen()
sc.bgcolor("black")
screenTk = sc.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", True)
sc.setup(width=1.0, height=1.0)

bounds = turtle.Turtle()
bounds.speed(0)
bounds.shape("square")
bounds.color("white")
bounds.shapesize(stretch_wid=50, stretch_len=1)
bounds.penup()
bounds.goto(150, 0)

bounds2 = turtle.Turtle()
bounds2.speed(0)
bounds2.shape("square")
bounds2.color("white")
bounds2.shapesize(stretch_wid=50, stretch_len=1)
bounds2.penup()
bounds2.goto(-150, 0)

outerbounds = turtle.Turtle()
outerbounds.speed(0)
outerbounds.shape("square")
outerbounds.color("white")
outerbounds.shapesize(stretch_wid=50, stretch_len=1)
outerbounds.penup()
outerbounds.goto(450, 0)

outerbounds2 = turtle.Turtle()
outerbounds2.speed(0)
outerbounds2.shape("square")
outerbounds2.color("white")
outerbounds2.shapesize(stretch_wid=50, stretch_len=1)
outerbounds2.penup()
outerbounds2.goto(-450, 0)

player = turtle.Turtle()
player.speed(0)
player.shape("square")
player.color("white")
player.penup()
player.goto(0, -400)

# Initialize the score
score = 0

#time.sleep(10)
# Displays the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("white")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 450)
sketch.write(
    "Score: 0",
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
playerx=0
sumx=0
while True:
    for msg in inport.iter_pending():
        if inactive:
         #   hit_ball.goto(0, 0)
          #  hit_ball.dx = 12
         #   hit_ball.dy = -12
          #  left_player = 0
           # right_player = 0
            #sketch.clear()
         #   sketch.write(
          #      "Spieler*in 1: 0    Level: 1     Spieler*in 2: 0",
           #     align="center",
            #    font=("Terminal", 24, "normal"),
         #   )
            level = 1
          #  inactive = False
        if msg.type == "control_change" and msg.control == 22:
            if (msg.channel % 5) == 1:
                sumx += 64-msg.value
                if sumx > 8:
                    playerx +=1
                    sumx=0
                if sumx < -8:
                    playerx -=1
                    sumx=0
                if playerx > 1:
                    playerx -=1
                if playerx < -1:
                    playerx +=1
            if playerx == 1:
                player.goto(225, -400)
            elif playerx == 0:
                player.goto(0, -400)
            elif playerx == -1:
                player.goto(-225, -400)


         #   elif (msg.channel % 5) == 0:
          #      righty += 2 * (64 - msg.value) 
                # right_pad.sety(right_pad.ycor() + 10*(64-msg.value))
                # right_pad.sety(msg.pitch/30)
        elif msg.type == "note_on" and msg.note == 18:
            exit()
   # left_pad.sety(left_pad.ycor() + lefty)
    #right_pad.sety(right_pad.ycor() + righty)
   # if lefty == 0 and righty == 0:
        inactivity += 1
   # else:
   #     inactivity = 0
    #sc.update()

#    if numCol == 3:
#        hit_ball.dx = numpy.sign(hit_ball.dx) * (abs(hit_ball.dx) + 1)
#        hit_ball.dy = numpy.sign(hit_ball.dy) * (abs(hit_ball.dy) + 1)
#        numCol = 0
 #       level += 1
  #      sketch.clear()
   #     sketch.write(
    #        "Spieler*in 1: {}    Level: {}     Spieler*in 2: {}".format(
     #           left_player, level, right_player
      #      ),
       #     align="center",
        #    font=("Terminal", 24, "normal"),
      #  )

#    new_x = hit_ball.xcor() + hit_ball.dx
 #   new_y = hit_ball.ycor() + hit_ball.dy
  #  hit_ball.goto(new_x, new_y)

    # Checking borders
 #   if hit_ball.ycor() > 370:
  #      hit_ball.sety(370)
   #     hit_ball.dy *= -1

 #   if hit_ball.ycor() < -370:
  #      hit_ball.sety(-370)
   #     hit_ball.dy *= -1

#    if hit_ball.xcor() > 700:
 #       hit_ball.goto(0, 0)
  #      hit_ball.dy *= -1
   #     left_player += 1
    #    sketch.clear()
     #   sketch.write(
#            "Spieler*in 1: {}    Level: {}     Spieler*in 2: {}".format(
 #               left_player, level, right_player
     #       ),
  #          align="center",
   #         font=("Terminal", 24, "normal"),
    #    )
    #    numCol = 0
     #   level = 1
      #  hit_ball.dx = 12 * numpy.sign(hit_ball.dx)
#        hit_ball.dy = 12 * numpy.sign(hit_ball.dy)

  #  if hit_ball.xcor() < -700:
 #       hit_ball.goto(0, 0)
#        hit_ball.dy *= -1
 #       right_player += 1
  #      sketch.clear()
   #     sketch.write(
    #        "Spieler*in 1: {}    Level: {}     Spieler*in 2: {}".format(
     #           left_player, level, right_player
   #         ),
      #      align="center",
       #     font=("Terminal", 24, "normal"),
  #      )
#        numCol = 0
 #       level = 1
  #      hit_ball.dx = 12 * numpy.sign(hit_ball.dx)
   #     hit_ball.dy = 12 * numpy.sign(hit_ball.dy)

#    if (hit_ball.xcor() > 520 and hit_ball.xcor() < 521 + abs(hit_ball.dx)) and (
 #       hit_ball.ycor() < right_pad.ycor() + 60
  #      and hit_ball.ycor() > right_pad.ycor() - 60
 #   ):
  #      hit_ball.setx(520)
 #       hit_ball.dx *= -1
   #     numCol += 1

#    if (hit_ball.xcor() < -520 and hit_ball.xcor() > -521 - abs(hit_ball.dx)) and (
 #       hit_ball.ycor() < left_pad.ycor() + 60
  #      and hit_ball.ycor() > left_pad.ycor() - 60
  #  ):
#        hit_ball.setx(-520)
 #       hit_ball.dx *= -1
  #      numCol += 1

#    if inactivity > 300:
 #       inactive = True
  #      inactivity = 0

#    if left_pad.ycor() > 800:
 #       left_pad.sety(-800)
  #  if left_pad.ycor() < -800:
   #     left_pad.sety(800)
#    if right_pad.ycor() > 800:
 #       right_pad.sety(-800)
  #  if right_pad.ycor() < -800:
   #     right_pad.sety(800)
