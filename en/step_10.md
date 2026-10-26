## 5A - Switch between moods

Your starter already connects a click to a reaction. Now decide what that reaction means.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **react()**. Both your click control and any keyboard control call this same function.

```python
def react():
    global mood, message
    if mood == 'calm':
        mood = 'happy'
        message = 'You found my tickle spot!'
    else:
        mood = 'calm'
        message = 'Again?'
```

## Test

Run your code and use your control twice. The face and message should swap each time. Your body and home should stay as you designed them.

## Make it yours

Rewrite both messages. Try **sleepy** instead of **happy**: the starter already knows how to draw that mouth. Your rule is: **When someone ___, my pet ___**.

[Choose another part](landing.md).
