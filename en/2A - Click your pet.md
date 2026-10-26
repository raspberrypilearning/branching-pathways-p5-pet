## 2A - Click your pet

A click can be a pat, a tickle or a surprise. You decide what it means.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **mouse_pressed()**. The distance check makes clicks near the centre of your pet count.

```python
def mouse_pressed():
    if dist(mouse_x, mouse_y, x, y) < 60:
        react()
```

## Test

Run your code. Click your pet, then a far corner. Only the click near your pet should change its face and message.

## Make it yours

Change **60** to make the touch area bigger or smaller. To accept a click anywhere, remove the **if** line and move **react()** left by four spaces.

[Choose another part](landing.md).
