import turtle, time

screen = turtle.Screen()
screenTk = screen.getcanvas().winfo_toplevel()
screenTk.attributes("-fullscreen", True)

while True:
	print("test")
	time.sleep(1)
