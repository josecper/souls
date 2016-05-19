import pyglet
import pyglet.image
import pyglet.clock
import sys


data = open(sys.argv[1], "rb").read()
minx = 1024
minsize = minx*minx*3
padlength = minsize - len(data) % minsize
data = data + bytes("\x00", "utf-8")*padlength

i = j = 0
delta = 64
im = pyglet.image.ImageData(1024,1024, "RGB", data)
window = pyglet.window.Window(400,400)

def update(dt):
    global i, j
    i = (i+delta) % 1024 
    im.get_region(i,i,400,400).blit(0,0,0)

pyglet.clock.schedule_interval(update,0.4)
pyglet.app.run()

