# souls

create actual living souls inside your computer!

requires:
- python 3
- numpy
- pyglet
- currently a shitload of cpu time

current state:
- renders souls at 30 fps
- reads simple rules
- mostly terrible so far

syntax:

rules are executed first to last every step and consist of very simple syntax so far, each consisting of a left side (a combination of colors, modifiers and/or logical operators), an operator (-, +, =) and a right side (currently just a color to be assigned):

- tokens:
  - r, g, b, k, w = colors (red, green, blue, black, white)
  - ^, v, <, > = directions
  - 1, 2, 3, 4 = number operators (n of surrounding cells)
  - * = any (equivalent to 1 or greater)
  - ! = all (equivalent to 4)

- examples:

  - ^g&*k+g : if the next cell in the up direction (^) has green (g), and (&) there is black (k) anywhere around this cell (*), then add (+) green (g) to this cell.
  - k|w=b : if this cell is black (k) or (|) white (w), then turn (=) this cell blue.

*conway's game of life*

  - 1g&g-g : if there's exactly one (1) green (g) neighbour and (&) this cell is green (g), then remove (-) green (g) from this cell.
  - 4g&g-g : if there's exactly four (4) green (g) neighbours and (&) this cell is green (g), then remove (-) green (g) from this cell.
  - 3g+g : if there's exactly three (3) green (g) neighbours, add (+) green to this cell