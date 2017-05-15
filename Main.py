from pyprocessing import *
import random as r

state = 4

team1 = ''
team2 = ''
score1 = 0
score2 = 0

boxx = []
boxy = []


show_box = False
selected_box = (0, 0)

def setup():
    size(800, 500)
    frameRate(15)


def draw():
    global show_box, selected_box, state
    background(58, 57, 253)

    if state == 0:
        draw_enter()

    if state == 3:
        if(show_box):
            print selected_box
            show_box = False
        strokeWeight(2)
        draw_grid()
        draw_title()
        draw_cats()
        draw_points()

    if state == 4:
        draw_title()
        draw_text_box()


def draw_text_box():
    noStroke()
    fill(255)
    rect(340, 375, 100, 50)

def draw_enter():
    fill(255)
    rect(340, 325, 100, 50)
    fill(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    textSize(36)
    text('Jeopardy!', 290, 150)
    fill(0)
    textSize(12)
    text('Enter', 365, 355)

def draw_points():
    for a in range(1, 6):
        x = a/5.0 * 800 - 80
        text("100", x, 135)
        text("200", x, 220)
        text("300", x, 300)
        text("400", x, 375)
        text("500", x, 465)


def draw_title():
    fill(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    textAlign(CENTER)
    textSize(22)
    text("Jeopardy!", 390, 30)


def draw_cats():
    fill(255)
    textSize(14)
    text("Derivatives", 75, 70)
    text("Integrals", 240, 70)
    text("Function Analysis", 400, 70)
    text("Related Rates", 555, 70)
    text("Miscellaneous", 720, 70)


def draw_grid():
    for x in range(1, 6):
        x1 = 0
        x2 = 800
        y1 = x / 6.0 * 500
        y2 = y1
        line(x1, y1, x2, y2)
    for y in range(1, 5):
        x1 = y / 5.0 * 800
        x2 = x1
        y1 = 500 / 6.0 - 40
        y2 = 500
        line(x1, y1, x2, y2)

    line(2, (500 / 6.0 - 40), 2, 500)
    line(798, (500 / 6.0 - 40), 798, 500)
    line(0, 498, 800, 498)
    line(0, (500 / 6.0 - 40), 800, (500 / 6.0 - 40))


def mouseClicked():
    global state, show_box, selected_box
    x = mouse.x
    y = mouse.y

    if state == 0:
        if x > 340 and x < 440 and y > 325 and y < 375:
            state = 3

    elif state == 3:
        v1 = None
        v2 = None
        for a in range(1, 6):
            x1 = (a-1)/5.0 * 800
            x2 = a/5.0 * 800
            if x < x2 and x > x1:
                v1 = a-1
                break
        for b in range(1, 6):
            y1 = (b-1)/6.0 * 500
            y2 = b/6.0 * 500
            if y < y2 and y > y1:
                v2 = b-2
                break
        if v2 == None:
            v2 = 4
        show_box = True
        selected_box = (v1, v2)

run()
