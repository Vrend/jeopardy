from pyprocessing import *
import random as r
import os
import time

state = 0

team1 = ''
team2 = ''
score1 = 0
score2 = 0

turn = 0

answer = ''

answer_response = ''

categories = {'Derivatives': 0, 'Integrals': 1, 'Function Analysis': 2, "Related Rates": 3, "Misc": 4}

images = {}

image_to_answer = {}

solved = [[False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False]]

selected_text_box = False

show_box = False

selected_box = (0, 0)

root = os.getcwd()

tries = 2

stolen = False

img = None


def load_image():
    global img, state
    try:
        path = root + '/problems/' + images[selected_box]
        img = loadImage(path)
    except:
        print "Error loading image"
        state = 5


def load_problems():
    global images, categories, image_to_answer
    problems = open(root+'/problem_list', 'r')
    while True:
        l = problems.readline()
        if l == '':
            break
        problem = l.split(',')
        print problem
        images[(categories[problem[1]], (int(problem[2])/100-1))] = problem[0]
        image_to_answer[problem[0]] = int(problem[3])


def setup():
    global turn
    turn = r.randint(1, 2)
    if not os.path.isdir(root+"/problems"):
        os.mkdir(root+"/problems")
    if not os.path.isfile(root+'/problem_list'):
        problems = open(root+'/problem_list', 'w+')
        problems.close()
    load_problems()
    size(800, 500)
    frameRate(15)


def draw():
    global show_box, selected_box, state, answer, answer_response
    background(58, 57, 253)

    if state == 0:
        draw_enter()

    elif state == 1:
        draw_title()
        fill(255)
        text("Enter team 1 name", 350, 225, 100, 50)
        draw_text_box()

    elif state == 2:
        draw_title()
        fill(255)
        text("Enter team 2 name", 350, 225, 100, 50)
        draw_text_box()

    elif state == 3:
        if show_box:
            state = 4
        strokeWeight(2)
        draw_grid()
        draw_title()
        draw_cats()
        draw_points()

    elif state == 4:
        draw_title()
        draw_text_box()
        draw_image()
        fill(255)
        text(answer_response, 350, 450)

    elif state == 6:
        draw_title()
        fill(255)
        text(answer_response, 400, 300)
        rect(340, 325, 100, 50)
        fill(0)
        textSize(12)
        text('Ok', 365, 355)

    else:
        fill(255)
        textAlign(CENTER)
        textSize(250)
        text("Error", 400, 300)


def draw_image():
    global img
    image(img, 250, 50, 300, 300)


def check_answer(num):
    global selected_box
    ans = image_to_answer[images[selected_box]]
    if (ans - .005) <= int(num) <= (ans + .005):
        return True
    return False



def keyPressed():
    global answer, selected_text_box, state, answer_response, selected_box, show_box, tries, image_to_answer, images, solved, turn, stolen, team1, team2
    if state == 1:
        if selected_text_box:
            if key.code == BACKSPACE or key.code == DELETE:
                if len(team1) > 0:
                    team1 = team1[0:len(team1)-1]
            elif key.code == ENTER or key.code == RETURN:
                state = 2
                selected_text_box = False
    elif state == 2:
        if selected_text_box:
            if key.code == BACKSPACE or key.code == DELETE:
                if len(team2) > 0:
                    team2 = team2[0:len(team2)-1]
            elif key.code == ENTER or key.code == RETURN:
                state = 3
                selected_text_box = False
    elif state == 4:
        if selected_text_box:
            if key.code == BACKSPACE or key.code == DELETE:
                if len(answer) > 0:
                    answer = answer[0:len(answer)-1]
            elif key.code == ENTER or key.code == RETURN:
                if check_answer(answer):
                    answer_response = 'Correct!'
                    time.sleep(1)
                    answer_response = ''
                    add_points((selected_box[1]+1)*100)
                    show_box = False
                    tries = 2
                    solved[selected_box[0]][selected_box[1]] = True
                    state = 3
                    if not stolen:
                        turn = turn % 2 + 1
                    else:
                        stolen = False
                else:
                    tries -= 1
                    if tries == 0:
                        answer_response = 'The answer was: ' + str(image_to_answer[images[selected_box]])
                        tries = 2
                        show_box = False
                        solved[selected_box[0]][selected_box[1]] = True
                        state = 6
                    else:
                        answer_response = 'Sorry, that was wrong: but the other team can steal!'
                        turn = turn % 2 + 1
                        stolen = True
                answer = ''

def add_points(num):
    global turn, score1, score2
    if turn == 1:
        score1 += num
    elif turn == 2:
        score2 += num
    else:
        print "Problem with scoring"

def keyTyped():
    global answer, state, selected_text_box, team1, team2
    thing = key.char
    if state == 4:
        if selected_text_box:
            if '0123456789.'.__contains__(thing):
                answer += thing

    elif state == 1:
        if selected_text_box:
            team1 += key.char\

    elif state == 2:
        if selected_text_box:
            team2 += key.char

def draw_text_box():
    global selected_text_box, answer
    if selected_text_box:
        stroke(3)
    else:
        noStroke()

    fill(255)
    rect(340, 375, 100, 50)
    fill(0)
    textSize(12)
    text(answer, 390, 410)


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
    global solved
    for a in range(1, 6):
        x = a / 5.0 * 800 - 80

        if solved[a - 1][0]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("100", x, 135)
        if solved[a - 1][1]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("200", x, 220)
        if solved[a - 1][2]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("300", x, 300)
        if solved[a - 1][3]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("400", x, 375)
        if solved[a - 1][4]:
            fill(0, 255, 0)
        else:
            fill(255)
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
    global state, show_box, selected_box, selected_text_box, answer_response
    x = mouse.x
    y = mouse.y

    if state == 0:
        if 340 < x < 440 and 325 < y < 375:
            state = 3
    elif state == 6:
        if 340 < x < 440 and 325 < y < 375:
            state = 3
            answer_response = ''

    elif state == 3:
        v1 = None
        v2 = None
        for a in range(1, 6):
            x1 = (a - 1) / 5.0 * 800
            x2 = a / 5.0 * 800
            if x2 > x > x1:
                v1 = a - 1
                break
        for b in range(1, 6):
            y1 = (b - 1) / 6.0 * 500
            if y1 == 0:
                y1 = 85
            y2 = b / 6.0 * 500
            if y2 > y > y1:
                v2 = b - 2
                break
            elif y > 420:
                v2 = 4

        if v2 is None:
            return

        if solved[v1][v2]:
            return
        show_box = True
        selected_box = (v1, v2)
        state = 4
        load_image()

    elif state == 4:
        if 340 < x < 440 and 375 < y < 425:
            selected_text_box = True
        else:
            selected_text_box = False

run()
