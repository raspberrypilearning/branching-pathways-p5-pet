## 4B - Bounce up and down

Make a pet that cannot keep still.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **move_pet()**. The absolute value keeps each bounce above the starting height.

```python
def move_pet():
    from math import sin
    global x, y
    x = 200
    y = 230 - abs(sin(frame_count * 0.05)) * 80
```

## Test

Run your code. The pet should rise and return to the same place. Its face and decorations should travel with it.

## Make it yours

Change **80** to set the height and **0.05** to set the speed. Could it float gently instead of bouncing?

[Choose another part](landing.md).
