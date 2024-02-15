#!/usr/bin/env python
from os import system
from subprocess import call
import turtle
import mido
import math

games=[
    ["Pong", "python", r"/home/pi/Desktop/TurntableGames/DJPong/midi_test.py"],
    ["Sokoban","python", r"/home/pi/Desktop/TurntableGames/dj-sokoban/sokoban.py"]
]

sc = turtle.Screen()
sc.bgcolor("black")
screenTk = sc.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", True)
sc.setup(width=1.0, height=1.0)

#sketch = turtle.Turtle()
#sketch.speed(0)
#sketch.color("white")
#sketch.penup()
#sketch.hideturtle()
#sketch.write(
#    "  Pong        Tetris      Sokoban",
#    align="center",
#    font=("Terminal", 24, "normal"),
#)
num = len(games)
for pos,game in enumerate(games):
    sketch = turtle.Turtle()
    sketch.speed(0)
    sketch.color("white")
    sketch.penup()
    sketch.hideturtle()
    sketch.goto(int(300 * math.cos(pos*2*math.pi/num)), int(300 * math.sin(pos*2*math.pi/num)))
    sketch.write(game[0], font=("Terminal",24,"normal"))

sel_ball = turtle.Turtle()
sel_ball.speed(0)
sel_ball.shape("square")
sel_ball.color("white")
sel_ball.penup()
sel_ball.goto(0,200)

pyg = mido.Backend('mido.backends.pygame')
inport = pyg.open_input('Xponent MIDI 1')

t=0

while True:
    choice=None
    for msg in inport.iter_pending():
        if msg.type == "control_change" and msg.control == 22:
            t += 2*(msg.value-64)
        elif msg.type == "note_on":
            if msg.note == 18:
                exit()
            elif msg.note >= 19 and msg.note <= 21:
                t_tilde=t+360/(2*num)
                choice = t_tilde // (360/num)
    sel_ball.goto(200*math.cos(t*2*math.pi/360),200*math.sin(t*2*math.pi/360))
    if t< - 360/(2*num):
        t += 360
    if t> 360-360/(2*num):
        t -= 360
        
#    system("clear")
#    print(
#        """
#Programm wählen:
#1) Pong
#2) Tetris (noch nicht funktionsfähig)
#3) Sokoban
#"""
#    )
#    choice = input("> ").strip()
#
#    print(choice)
#
    if choice!=None:
        print([games[choice][1],games[choice][2]])
        call([games[choice][1],games[choice][2]])
#    choice=str(choice)
#    if choice == "1":
#        print("Starte Pong...")
#        call(["python", r"/home/pi/Desktop/TurntableGames/DJPong/midi_test.py"])
#    """if choice == "2":
#        print("Starte Tetris...")
#        call(["python", r"dj-tetris/__.py"])"""
#    if choice == "3":
#        print("Starte Sokoban...")
#        call(
#            ["python", r"/home/pi/Desktop/TurntableGames/dj-sokoban/sokoban.py"],
#            stdin=open(r"/home/pi/Desktop/TurntableGames/dj-sokoban/boards.txt", "r"),
#        )
