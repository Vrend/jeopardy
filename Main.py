from pyprocessing import *
import random as r

def setup():
    size(800, 500)
    strokeWeight(2)

def draw():
    background(58, 57, 253)
    draw_grid()
    draw_title()


def draw_title():
    fill(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    textAlign(CENTER)
    textSize(22)
    text("Jeopardy!", 390, 30)

def draw_grid():
    for x in range(1, 6):
        x1 = 0
        x2 = 800
        y1 = x/6.0 * 500
        y2 = y1
        line(x1, y1, x2, y2)
    for y in range(1, 5):
        x1 = y/5.0 * 800
        x2 = x1
        y1 = 500/6.0 - 40
        y2 = 500
        line(x1, y1, x2, y2)

    line(2, (500/6.0 - 40), 2, 500)
    line(798, (500/6.0 - 40), 798, 500)
    line(0, 498, 800, 498)
    line(0, (500/6.0 - 40), 800, (500/6.0 -40))

run()