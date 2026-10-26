## 5C - Give it a voice

A message can make the same creature seem shy, dramatic or very silly.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **react()**. This pet chooses a new line each time. Its voice is written on screen.

```python
def react():
    from random import choice
    global mood, message
    mood = 'happy'
    message = choice([
        'Is that a biscuit?',
        'I meant to do that.',
        'More adventures, please!'
    ])
```

## Test

Run your code and use your control. Check every message is short enough to fit inside the canvas.

## Make it yours

Write three lines for your own pet. Keep them short. You could borrow the strange food ideas from Python Bytes.

[Choose another part](landing.md).
