#!/usr/bin/env python
from os import system
from subprocess import call
import turtle
import mido
import math

games=[
    ["Pong", "python", r"/home/pi/Desktop/TurntableGames/DJPong/midi_test.py"],
    ["Sokoban","python", r"/home/pi/Desktop/TurntableGames/dj-sokoban/sokoban.py"],
]

texte=[]

sc = turtle.Screen()
sc.bgcolor("black")
screenTk = sc.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", True)
sc.setup(width=1.0, height=1.0)

num = len(games)
for pos,game in enumerate(games):
    sketch = turtle.Turtle()
    sketch.speed(0)
    sketch.color("white")
    sketch.penup()
    sketch.hideturtle()
    sketch.goto(int(300 * math.cos(pos*2*math.pi/num)), int(300 * math.sin(pos*2*math.pi/num)))
    sketch.write(game[0], font=("Terminal",24,"normal"))
    texte.append(sketch)

game_angle = 360/num

sel_ball = turtle.Turtle()
sel_ball.speed(0)
sel_ball.shape("square")
sel_ball.color("white")
sel_ball.penup()
sel_ball.goto(0,200)

pyg = mido.Backend('mido.backends.pygame')
inport = pyg.open_input('Xponent MIDI 1')

#paramter of the ball, amount that it moved
t=0
#counter for the time till the game is selcted
select_time = 0
#id of the selected game
select = None

while True:
    choice=None
    for msg in inport.iter_pending():
        if msg.type == "control_change" and msg.control == 22:
            t += 2*(msg.value-64)
        elif msg.type == "note_on":
            if msg.note == 18:
                exit()
            #elif msg.note >= 19 and msg.note <= 21:
            #    t_tilde=t+360/(2*num)
            #    choice = int(t_tilde // (360/num))
    if t%game_angle <= 10 or t%game_angle >= game_angle-10:
        select_new = None
        if t%game_angle <= 10:
            select_new = t//game_angle
        elif t%game_angle >= game_angle-10:
            select_new = t//game_angle +1
            if select_new == num:
                select_new = 0
        if select == select_new:
            select_time += 1
            color_red = 0xff - select_time*0xff/100
            color_green = 0x00 + select_time*0xff/100
            texte[select].color(color_red,color_green,0)
        select = select_new
        if select_time == 100:
            choice = select      
    sel_ball.goto(200*math.cos(t*2*math.pi/360),200*math.sin(t*2*math.pi/360))
    if t< - 360/(2*num):
        t += 360
    if t> 360-360/(2*num):
        t -= 360
    if choice!=None:
        print(choice)
        call([games[choice][1],games[choice][2]])