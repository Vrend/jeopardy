from pyprocessing import *
import random as r
import os

# By Vrend Copyright 2017

# the pyprocessing import copies everything (*) into the program from that file, allowing for the game to work
# added the random file with the alias r, which allows it to be
# called like this: r.randint(x, y) vs random.randint(x, y)
# imports os functions for file IO

# Holds game state
# 0 is main menu
# 1 and 2 is name choice
# 3 is jeopardy board
# 4 is the question board
# 5 is error board
# 6 returns answer
# 7 is winning screen
state = 0

# holds team names and respective score
team1 = ''
team2 = ''
score1 = 0
score2 = 0

# holds current player's turn, 1 for team 1 and 2 for team 2
turn = 0

# holds current guessed answer
answer = ''

# this is whatever response, like it is wrong, it can be stolen, and the answer itself
answer_response = ''

# this is used to convert from the category to the x coordinate of the question list
categories = {'Derivatives': 0, 'Integrals': 1, 'Function Analysis': 2, "Related Rates": 3, "Misc": 4}

# this holds the image, taking in the coordinate in this form: (x, y), which returns the name of the image
images = {}

# plug in the image name to get its respective answer
image_to_answer = {}

# this holds the questions that both teams get wrong
wrong = {}

# holds whether or not a question has been answered
solved = [[False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False],
          [False, False, False, False, False], [False, False, False, False, False]]

# symbol list
symbols = {'5': '%', '6': '^', '8': '*', '=': '+', '9': '(', '0': ')', '7': '&', ',': '<', '.': '>'}

# variable for detecting whether or not a text box is 'active'
selected_text_box = False

# variable used to move to the 4th state
show_box = False

# when you click on a box, this variable sets it to that box
selected_box = (0, 0)

# root dirctory used in locating images
root = os.getcwd()

# variable that keeps track of tries for each question
tries = 2

# used to determine when turns change, if the question is stolen
stolen = False

# holds the image that will be displayed
img = None

# this is the coordinates of a random question, which will be worth double
double_points = (-1, -1)

# when this is true, it will be the last question, which is worth double
last_question = False

shift = False


# this function creates a dictionary of (x, y) coordinates that correspond to a boolean. This can be used to determine if a question was wrong
def build_wrong():
    for x in range(0, 5):
        for y in range(0, 5):
            wrong[(x, y)] = False


# loads the image file into the img variable, using the path from the currently selected box
def load_image():
    global img, state
    try:
        # sets the location of the problem using the root,
        # the folder name, and the name of the file using the 'images' dictionary
        path = root + '/problems/' + images[selected_box]
        # loads the image into the 'img' variable using the path
        img = loadImage(path)
    except:
        print "Error loading image"
        # if the picture doesn't exist, or you try and access an empty coordinate, it will go to the error state
        state = 5


# uses problem_list file to populate image dictionary, as well as populate the answer dictionary
def load_problems():
    global images, categories, image_to_answer
    # opens the problem_list file as read-only
    problems = open(root + '/problem_list', 'r')
    while True:
        # gets the line of the program, and if it's empty, break this loop
        l = problems.readline()
        if l == '':
            break
        # split the line by the comma, creating the list 'problem'
        problem = l.split(',')
        # this is putting the coordinates of the image as the key and the name of the picture as the value
        # the coordinates use the 'categories' dictionary to get the x coordinate and takes the point value
        # divides it by 100, and subtracts one, because it's a zero based index
        images[(categories[problem[1]], (int(problem[2]) / 100 - 1))] = problem[0]
        # assigns the name of the picture as the key and the answer as the value in the 'image_to_answer' dictionary
        image_to_answer[problem[0]] = problem[3]


# run at the beginning of the program
def setup():
    global turn, double_points
    # fills the wrong array as all false (none solved)
    build_wrong()
    # determines who goes first
    turn = r.randint(1, 2)
    # chooses a random question to be worth double points
    double_points = (r.randint(0, 4), r.randint(0, 4))
    # checks if the problems directory and the problem_list file exists, and if they don't, create them
    if not os.path.isdir(root + "/problems"):
        os.mkdir(root + "/problems")
    if not os.path.isfile(root + '/problem_list'):
        problems = open(root + '/problem_list', 'w+')
        problems.close()
    # opens the problem_list file and loads the problem information into the dictionaries
    load_problems()
    # sets the window size to 800 x 500
    size(800, 500)
    # the draw function will be called 15 times a second
    frameRate(15)


# runs 15 times a second
def draw():
    global show_box, selected_box, state, answer, answer_response, double_points, last_question
    # sets background color to blue-ish using rgb
    background(58, 57, 253)

    # if in the main menu, run the draw_enter function
    if state == 0:
        draw_enter()

    # if you are naming the teams, you will complete this and the one below, and then enter state 3
    elif state == 1:
        draw_title()
        fill(255)
        textSize(18)
        text("Enter team 1 name", 350, 225)
        draw_text_box()
        text(team1, 390, 410)

    elif state == 2:
        draw_title()
        fill(255)
        textSize(18)
        text("Enter team 2 name", 350, 225)
        draw_text_box()
        text(team2, 390, 410)

    # this is where the main board is
    elif state == 3:
        # checks when to move to the question state (may be deprecated)
        if show_box:
            state = 4
        # sets the line thickness
        strokeWeight(2)
        # draws the lines for the boxes
        draw_grid()
        # draws the color-changing jeopardy title
        draw_title()
        # draws the category names
        draw_cats()
        # draws the point values
        draw_points()
        # draws the team names and their scores
        draw_scores()

    elif state == 4:
        # draws jeopardy title
        draw_title()
        # draws text box
        draw_text_box()
        # draws associated image
        draw_image()
        # sets color to white (255 in grayscale is white)
        fill(255)
        # draws the response at (350, 450)
        text(answer_response, 350, 450)
        # if this box is the double points box,
        # or 'last_question' is true, then it will say double points with flashing colors
        if selected_box == double_points or last_question:
            # sets to random color
            fill(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
            textSize(48)
            text("Double points!!!", 380, 480)

    # this is the confirmation state, when both teams get the answer wrong. It displays here
    elif state == 6:
        draw_title()
        fill(255)
        # draws answer and creates rectangle, which is clicked to move on
        text(answer_response, 400, 300)
        rect(340, 325, 100, 50)
        fill(0)
        textSize(12)
        text('Ok', 385, 355)

    # winning screen, which displays the winning teams name and their score
    elif state == 7:
        fill(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        textSize(48)
        fin = ' wins with '
        if score1 > score2:
            fin = team1 + fin + str(score1) + ' points!'
        elif score2 > score1:
            fin = team2 + fin + str(score2) + ' points!'
        else:
            fin = "Tie?"
        text(fin, 100, 200, 600, 200)
        textSize(12)
        fill(255)
        text('Press esc to quit.', 350, 350)

    # when the state is anything else, this is the error screen
    else:
        fill(255)
        textAlign(CENTER)
        textSize(250)
        text("Error", 400, 300)


# writes the teams name and score in the top right and top left corners
def draw_scores():
    global score1, score2, team1, team2
    fill(255)
    text(team1 + ': ' + str(score1), 100, 20)
    text(team2 + ': ' + str(score2), 700, 20)


# uses the img variable to draw the image on the screen
def draw_image():
    global img
    image(img, 250, 50, 500, 300)


# takes in a number and compares it to the answer,
# based on the coordinate. If it is within .005 of the answer, it is deemed correct
def check_answer(num):
    global selected_box
    # plugs in the currently selected box to get the image name, which is used to get the answer
    ans = image_to_answer[images[selected_box]]
    # if the num parameter when casted to float (because it was a string) is within the margin, it returns true
    try:
        if (float(ans) - .005) <= float(num) <= (float(ans) + .005):
            return True
    except:
        if str(ans).strip() == str(num).strip():
            return True
    return False


# used to detect if the control keys are pressed (backspace and return)
def keyPressed():
    global answer, selected_text_box, state, answer_response, selected_box, show_box, tries, image_to_answer, images, solved, turn, stolen, team1, team2, shift, last_question
    # when selecting names, this detects when to move to the other team, as well as
    # when they delete a character and when the name is too big
    if state == 1:
        # if they clicked on the text box
        if selected_text_box:
            # and they pressed backspace if on windows or delete on mac
            if key.code == BACKSPACE or key.code == DELETE:
                # can't delete if the length of the string is zero (no name)
                if len(team1) > 0:
                    # deletes the last character of the string
                    team1 = team1[0:len(team1) - 1]
            # if they hit enter on windows or return on mac
            elif key.code == ENTER or key.code == RETURN:
                # moves to the next team
                if len(team1.strip()) > 0:
                    state = 2
                    selected_text_box = False
    # same as above
    elif state == 2:
        if selected_text_box:
            if key.code == BACKSPACE or key.code == DELETE:
                if len(team2) > 0:
                    team2 = team2[0:len(team2) - 1]
            elif key.code == ENTER or key.code == RETURN:
                # moves to game state
                if len(team2.strip()) > 0:
                    state = 3
                    selected_text_box = False
    # if in the question state
    elif state == 4:
        # and the text box is selected
        if selected_text_box:
            # and the user types backspace or delete
            if key.code == BACKSPACE or key.code == DELETE:
                shift = False
                if len(answer) > 0:
                    # it will delete the last character, if the length isn't zero
                    answer = answer[0:len(answer) - 1]
            elif key.code == SHIFT:
                shift = not shift
            # if the user presses enter or return
            elif key.code == ENTER or key.code == RETURN:
                shift = False
                # it will check the answer, and if it's true
                if check_answer(answer):
                    # answer response is reset
                    answer_response = ''
                    # points are added to the current team,
                    # using the y coordinate of the box, adding one, and multiplying by 100
                    add_points((selected_box[1] + 1) * 100)
                    # may be deprecated
                    show_box = False
                    # reset number of tries
                    tries = 2
                    # sets this question to solved
                    solved[selected_box[0]][selected_box[1]] = True
                    # sets the state to the game state
                    state = 3
                    # text box is no longer selected
                    selected_text_box = False
                    # this keeps track so if the question is stolen, it will be the team who stole's turn
                    if not stolen:
                        turn = turn % 2 + 1
                    else:
                        stolen = False
                # if the answer is wrong
                else:
                    # subtract a try
                    tries -= 1
                    # and if both teams failed
                    if tries == 0:
                        # sets the answer in the response
                        answer_response = 'The answer was: ' + str(image_to_answer[images[selected_box]])
                        # resets try
                        tries = 2
                        # hides this window
                        show_box = False
                        # sets question as solved and solved wrong
                        solved[selected_box[0]][selected_box[1]] = True
                        wrong[selected_box] = True
                        # goes to confirmation state
                        state = 6
                        # text box is not selected
                        selected_text_box = False
                    else:
                        # if it isn't the last guess, then allow the other team to steal
                        answer_response = 'Sorry, that was wrong: but the other team can steal!'
                        turn = turn % 2 + 1
                        stolen = True
                # in any case, clear the answer
                answer = ''
                # and count how many problems are left. If only one is left,
                # activate last_question. If none are left, then move to the winning state, state 7
                count = 0
                for x in solved:
                    for y in x:
                        if not y:
                            count += 1
                if count == 1:
                    last_question = True
                elif count == 0:
                    state = 7


# takes in a number and adds it to the score of the team that is currently taking their turn
def add_points(num):
    global turn, score1, score2, double_points, selected_box

    # checks if it is the double points question, and doubles value
    if selected_box == double_points:
        num *= 2
    # checks which team is having their turn
    if turn == 1:
        score1 += num
    elif turn == 2:
        score2 += num
    else:
        print "Problem with scoring"


# handles when users type in numbers, letters, or grammar keys
def keyTyped():
    global answer, state, selected_text_box, team1, team2, symbols
    thing = key.char
    if state == 4:
        # only adds to the answer if it is selected
        if selected_text_box:
            try:
                if shift:
                    answer += symbols[thing]
                else:
                    answer += thing
            except:
                answer += thing
    # if selecting name of team, make sure it isn't longer than 15
    elif state == 1:
        if selected_text_box:
            if len(team1) <= 15:
                team1 += key.char
    # same as above
    elif state == 2:
        if selected_text_box:
            if len(team2) <= 15:
                team2 += key.char


# draws a homemade text box and writes the current value of answer in it
def draw_text_box():
    global selected_text_box, answer
    # if it is selected, give a border around the rectangle
    if selected_text_box:
        stroke(3)
    else:
        noStroke()

    fill(255)
    rect(340, 375, 100, 50)
    fill(0)
    textSize(12)
    # write the answer in the rectangle
    text(answer, 390, 410)


# draws the enter buttion, which can be used to change states
def draw_enter():
    # draws white rectangle, for enter button
    fill(255)
    rect(340, 325, 100, 50)
    # draws changing color jeopardy title
    fill(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    textSize(36)
    text('Jeopardy!', 290, 150)
    # draws enter in black text
    fill(0)
    textSize(12)
    text('Enter', 365, 355)


# draws the point values on the board. If the question is in the wrong dictionary as true,
# then it will be red. If it is true in the solved list, it will be green, otherwise it will be white
def draw_points():
    global solved, wrong
    for a in range(1, 6):
        x = a / 5.0 * 800 - 80

        if wrong[(a - 1, 0)]:
            fill(255, 0, 0)
        elif solved[a - 1][0]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("100", x, 135)
        if wrong[(a - 1, 1)]:
            fill(255, 0, 0)
        elif solved[a - 1][1]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("200", x, 220)
        if wrong[(a - 1, 2)]:
            fill(255, 0, 0)
        elif solved[a - 1][2]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("300", x, 300)
        if wrong[(a - 1, 3)]:
            fill(255, 0, 0)
        elif solved[a - 1][3]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("400", x, 375)
        if wrong[(a - 1, 4)]:
            fill(255, 0, 0)
        elif solved[a - 1][4]:
            fill(0, 255, 0)
        else:
            fill(255)
        text("500", x, 465)


# draws the jeopardy title in large, changing colors
def draw_title():
    fill(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    textAlign(CENTER)
    textSize(22)
    text("Jeopardy!", 390, 30)


# draws the names of the categories during state 3
def draw_cats():
    fill(255)
    textSize(14)
    text("Derivatives", 75, 70)
    text("Integrals", 240, 70)
    text("Function Analysis", 400, 70)
    text("Related Rates", 555, 70)
    text("Miscellaneous", 720, 70)


# draws the grid lines in state 3
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

    # draws the border lines
    line(2, (500 / 6.0 - 40), 2, 500)
    line(798, (500 / 6.0 - 40), 798, 500)
    line(0, 498, 800, 498)
    line(0, (500 / 6.0 - 40), 800, (500 / 6.0 - 40))


# handles when the mouse is clicked
def mouseClicked():
    global state, show_box, selected_box, selected_text_box, answer_response
    # mouse coordinates
    x = mouse.x
    y = mouse.y

    # main menu
    if state == 0:
        # clicking on enter rectangle, enter team name
        if 340 < x < 440 and 325 < y < 375:
            state = 1
    # clicking on rectangle? select the box
    elif state == 1 or state == 2:
        if 340 < x < 440 and 375 < y < 425:
            selected_text_box = True
        else:
            selected_text_box = False
    # seeing the answer, hit the confirm button and go back
    elif state == 6:
        if 340 < x < 440 and 325 < y < 375:
            state = 3
            answer_response = ''
    # detects if clicking on a box
    elif state == 3:
        v1 = None
        v2 = None
        # checks x value
        for a in range(1, 6):
            x1 = (a - 1) / 5.0 * 800
            x2 = a / 5.0 * 800
            if x2 > x > x1:
                v1 = a - 1
                break
        # checks y value
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
        # if not one of the boxes give up
        if v2 is None:
            return
        # moves to question state and loads image, along with setting the current box
        if solved[v1][v2]:
            return
        show_box = True
        selected_box = (v1, v2)
        state = 4
        load_image()
    # if clicking on text box, then select it
    elif state == 4:
        if 340 < x < 440 and 375 < y < 425:
            selected_text_box = True
        else:
            selected_text_box = False


# starts the program
run()
