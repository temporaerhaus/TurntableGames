#!/usr/bin/env python
from os import system
from subprocess import call
import turtle
import mido

sc = turtle.Screen()
sc.bgcolor("black")
screenTk = sc.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", True)
sc.setup(width=1.0, height=1.0)

sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("white")
sketch.penup()
sketch.hideturtle()
sketch.write(
    "  Pong        Tetris      Sokoban",
    align="center",
    font=("Terminal", 24, "normal"),
)

sel_ball = turtle.Turtle()
sel_ball.speed(0)
sel_ball.shape("square")
sel_ball.color("white")
sel_ball.penup()
sel_ball.goto(0,-10)

pyg = mido.Backend('mido.backends.pygame')
inport = pyg.open_input('Xponent MIDI 1')

while True:
    choice=0
    xchange=0
    for msg in inport.iter_pending():
        if msg.type == "control_change" and msg.control == 22:
            xchange += 2*(msg.value-64)
        elif msg.type == "note_on":
            if msg.note == 18:
                exit()
            elif msg.note >= 19 and msg.note <= 21:
                if sel_ball.xcor() <= -125:
                    choice = 1
                elif sel_ball.xcor() >= 125:
                    choice = 3
                else:
                    choice = 2
    sel_ball.setx(sel_ball.xcor()+xchange)
    if sel_ball.xcor() < -300:
        sel_ball.setx(-300)
    elif sel_ball.xcor() > 300:
        sel_ball.setx(300)
        
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
    choice=str(choice)
    if choice == "1":
        print("Starte Pong...")
        call(["python", r"/home/pi/Desktop/TurntableGames/DJPong/midi_test.py"])
    """if choice == "2":
        print("Starte Tetris...")
        call(["python", r"dj-tetris/__.py"])"""
    if choice == "3":
        print("Starte Sokoban...")
        call(
            ["python", r"/home/pi/Desktop/TurntableGames/dj-sokoban/sokoban.py"],
            stdin=open(r"/home/pi/Desktop/TurntableGames/dj-sokoban/boards.txt", "r"),
        )
