from p5 import *

# Your pet's starting point
x = 200
y = 230
mood = 'calm'
message = 'Click my body!'


def setup():
    size(400, 400)
    no_stroke()


def draw_home():
    background('lightblue')
    fill('lightgreen')
    rect(0, 290, 400, 110)


def move_pet():
    pass  # Your pet can stay still for now


def draw_body():
    fill('orchid')
    ellipse(x, y, 110, 100)


def draw_face():
    fill('white')
    circle(x - 20, y - 15, 24)
    circle(x + 20, y - 15, 24)
    fill('black')
    circle(x - 20, y - 15, 10)
    circle(x + 20, y - 15, 10)
    if mood == 'happy':
        ellipse(x, y + 20, 30, 20)
    elif mood == 'sleepy':
        ellipse(x, y + 20, 12, 20)
    else:
        ellipse(x, y + 20, 24, 5)


def draw_accessories():
    pass  # Add decorations here when you want them


def react():
    global mood, message
    if mood == 'calm':
        mood = 'happy'
        message = 'Hello, friend!'
    else:
        mood = 'calm'
        message = 'That tickles.'


def mouse_pressed():
    if dist(mouse_x, mouse_y, x, y) < 60:
        react()


def key_pressed():
    pass  # You can give a key a job later


def draw():
    draw_home()
    move_pet()
    draw_body()
    draw_face()
    draw_accessories()
    fill('black')
    text_size(18)
    text(message, 20, 365)


run()
