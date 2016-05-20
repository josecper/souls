#!/usr/bin/python

# souls.py
# ------------------------------------------------------
# generate actual living souls in your screen
#
# todo:
# - evolving rules
# - more complex parser (allow nested operators)
# - god i hate parsers so much

import numpy
import PIL.Image
import sys
import pyglet
import pyglet.image
import pyglet.clock
import pyglet.gl
import re

black = numpy.array((False,False,False))
red = numpy.array((True, False, False))
green = numpy.array((False, True, False))
blue = numpy.array((False, False, True))
white = numpy.array((True,True,True))

fps=30

try:
    i=sys.argv.index("--fps")
    fps=int(sys.argv[i+1])
except ValueError:
    pass

density=0.2

def left(a): return numpy.roll(a, 1, axis=1)
def right(a): return numpy.roll(a,-1, axis=1)
def up(a): return numpy.roll(a, -1, axis=0)
def down(a): return numpy.roll(a, 1, axis=0)
def anywhere(a): return left(a) | right(a) | up(a) | down(a)
def everywhere(a): return left(a) & right(a) & up(a) & down(a)
def number(a,n):
    b = numpy.uint8(a)
    return up(b)+down(b)+left(b)+right(b) == n

def parse(command):
    
    condition,operator,assigned=re.split("([+=-])",command,maxsplit=1)
    
    dirs={"^": "up", "v": "down", ">": "right", "<": "left", "*": "anywhere", "!": "everywhere"}
    colors={"r": "red", "g": "green", "b": "blue", "k": "black", "w": "white"}
    s1=re.sub(r"([\^\*\<\>v])([rgbkw])", "{\g<1>}(\g<2>)", condition).format(**dirs)
    s1=re.sub(r"([1-4])([rgbkw])","number(\g<2>,\g<1>)", s1)
    s1="next_grid["+s1+"]"
    s2=re.sub(r"([rgbkw])","{\g<1>}",assigned).format(**colors)
    if(operator != "="): operator=operator+"="
    
    return "".join([s1,operator,s2])

def load_orders(filename):

    orders=""
    f=open(filename,"r")
    for command in f:
        orders += parse(command)

    return orders

def step(past_grid):
    
    k=numpy.all(past_grid == False, axis=2)
    w=numpy.all(past_grid == True, axis=2)
    r=past_grid[:,:,0]
    g=past_grid[:,:,1]
    b=past_grid[:,:,2]

    next_grid = past_grid.copy()
    exec(orders)        
    past_grid = next_grid.copy()
    
    return next_grid

grid=numpy.random.rand(400,400,3) > (1-density)

def update(dt):
    global grid
    grid = step(grid)
    grid8 = numpy.uint8(grid*255)
    im = pyglet.image.ImageData(400,400,"RGB",bytes(grid8.data), -400*3)
    im.blit(0,0,0)

def go():
    window = pyglet.window.Window(400,400)
    pyglet.clock.schedule_interval(update,1/fps)
    pyglet.app.run()

if __name__ == "__main__":
    orders = load_orders(sys.argv[1])
    go()
