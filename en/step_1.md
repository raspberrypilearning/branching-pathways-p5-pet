## 1A - Meet your pet

Your starter pet already has a body, a home and a reaction. Get it working, then change any part.

## Open your workspace

- Open the [Raspberry Pi Python editor](https://editor.raspberrypi.org/en/projects/blank-python-starter) in another tab.
- Copy the pet starter below. Replace everything in **main.py** with it.
- Select **Run**. A purple pet should appear in the visual output.

<details>
<summary>Copy the pet starter</summary>

```python
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
```

[Open the starter file](resources/pet.py) if you prefer to copy it from a file.

</details>

## Test

Click the middle of your pet. Its mouth and message should change. Click again to change them back.

You have made your first working pet!

## Keep your code

Use the editor's **Download** button to keep a copy of your Python project. If you log in, you can also save it in the editor.

This pathway saves your ticks and notes separately. **Save notes** does not save your Python code.

## Choose your next part

Start with controls, a body, movement, personality or a home. You can come back and change things.

<details>
<summary>How to use the code on these pages</summary>

- A function is a named chunk of code with one job.
- When a page says **replace a function**, replace its line starting with **def** and all the indented lines below it. Stop before the next **def**.
- Keep one copy of each function. Two versions with the same name do not run together.
- Keep **run()** at the very bottom. Keep the four spaces at the start of lines inside a function.
- Combine ideas from different parts. Options that replace the same function are alternatives; adapt one to include your own changes.

</details>

<details>
<summary>My pet did not appear</summary>

- Check you copied the whole starter, including its first and last lines.
- Look for an error message. Check the line it mentions for a missing bracket or changed spaces.
- If the editor says **Load failed**, refresh it or return to its home page and choose **Python**.

</details>

[Choose a part](landing.md).
