#!/usr/bin/env python

############Turntable Games Launcher##############################
# a programm to select one game that is then launched
# move the ball around to the text of the programm you want to start
# if the ball stays near one text, this text changes color, when green the corresponding game starts
##################################################################

from os import system
from subprocess import call
import turtle
import mido
import math

# all the games that can be selected
# [title, programm to call game, path to executable (/home/pi/Desktop/TurntableGames/... for the temporaerhaus device)]
# more then 17 games can lead to unexpected behaviour
games=[
    ["Pong", "python", r"/home/pi/Desktop/TurntableGames/DJPong/midi_test.py"],
    ["Sokoban","python", r"/home/pi/Desktop/TurntableGames/dj-sokoban/sokoban.py"],
#    ["tetris","python", r"/home/pi/Desktop/TurntableGames/dj-tetris/__.py"],
]

texte=[]

sc = turtle.Screen()
sc.tracer(0)
sc.colormode(255)
sc.bgcolor("black")
screenTk = sc.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", True)
sc.setup(width=1.0, height=1.0)

num = len(games)

# text to explain what to do
exp_text = turtle.Turtle()
exp_text.speed(0)
exp_text.color("white")
exp_text.penup()
exp_text.hideturtle()
exp_text.goto(0,350)
exp_text.write("Spiel auswählen", font=("Terminal",24,"normal"), align="center")

# writing all the games in a circle
for pos,game in enumerate(games):
    sketch = turtle.Turtle()
    sketch.speed(0)
    sketch.color("white")
    sketch.penup()
    sketch.hideturtle()
    sketch.goto(int(300 * math.cos(pos*2*math.pi/num)), int(300 * math.sin(pos*2*math.pi/num))-12) #-12 for being vertical centered
    sketch.write(game[0], font=("Terminal",24,"normal"), align="center")
    texte.append(sketch)

game_angle = 360/num

# ball to select a game
sel_ball = turtle.Turtle()
sel_ball.speed(0)
sel_ball.shape("square")
sel_ball.color("white")
sel_ball.penup()
sel_ball.goto(0,200)

pyg = mido.Backend('mido.backends.pygame')
inport = pyg.open_input('Xponent MIDI 1')

#paramter of the ball, amount that it moved
t=game_angle/2 # so that it starts off one of the games
#counter for the time till the game is selcted
select_time = 0
select_time_max = 60
#id of the selected game
select = None

text_set = False

def drawloop():
    global sc, t, select_time, select_time_max, select, text_set
    choice=None

    sc.update()
    
    # process the incoming signals of the dj desk
    for msg in inport.iter_pending():
        if msg.type == "control_change" and msg.control == 22:
            t -= 2*(msg.value-64)
        elif msg.type == "note_on":
            if msg.note == 8:
                exit()
                
    # chance the color of one text if one ball is near
    if t%game_angle <= 10 or t%game_angle >= game_angle-10:
        # number of the game selected
        select_new = None
        if t%game_angle <= 10:
            select_new = int(t//game_angle)
        elif t%game_angle >= game_angle-10:
            select_new = int(t//game_angle) +1
            if select_new == num:
                select_new = 0
        if select == select_new:
            select_time += 1
            color_change = int(0xff - select_time*0xff/select_time_max)
            texte[select].clear()
            texte[select].color((color_change,255,color_change))
            texte[select].write(games[select][0], font=("Terminal",24,"normal"), align="center")
            if not text_set:
                exp_text.clear()
                exp_text.write("Spiel startet gleich", font=("Terminal",24,"normal"), align="center")
                text_set = True
        else:
            select_time = 0
            for pos, text in enumerate(texte):
                text.clear()
                text.color("white")
                text.write(games[pos][0], font=("Terminal",24,"normal"), align="center")
            exp_text.clear()
            exp_text.write("Spiel auswählen", font=("Terminal",24,"normal"), align="center")     
        select = select_new
        if select_time == select_time_max:
            choice = select
            select_time = 0
    else:
        select_time = 0
        for pos, text in enumerate(texte):
            text.clear()
            text.color("white")
            text.write(games[pos][0], font=("Terminal",24,"normal"), align="center")
        if text_set:
            exp_text.clear()
            exp_text.write("Spiel auswählen", font=("Terminal",24,"normal"), align="center")
            text_set = False
    sel_ball.goto(200*math.cos(t*2*math.pi/360),200*math.sin(t*2*math.pi/360))
    if t< - 360/(2*num):
        t += 360
    if t> 360-360/(2*num):
        t -= 360
    if choice!=None:
        print(choice)
        call([games[choice][1],games[choice][2]])
        t = game_angle/2

    sc.ontimer(drawloop, 60)
		

drawloop()
sc.mainloop()
