## 5B - Surprise me

Perhaps your pet has a mind of its own.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **react()**. A random choice picks one mood whenever you use a control.

```python
def react():
    from random import choice
    global mood, message
    mood = choice(['calm', 'happy', 'sleepy'])
    if mood == 'happy':
        message = 'Play time!'
    elif mood == 'sleepy':
        message = 'Five more minutes...'
    else:
        message = 'Just watching.'
```

## Test

Run your code. Use your control several times. You might get the same mood twice; that is allowed by a random choice.

## Make it yours

Change the messages. Repeat **happy** in the list to make it more likely. If you invent a new mood, add a matching rule to **draw_face()**.

[Choose another part](landing.md).
