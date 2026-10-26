## 4A - Wobble from side to side

Repeated movement can give even a simple shape a personality.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **move_pet()**. The sine function makes a smooth repeating wave; you can explore the numbers without learning the maths first.

```python
def move_pet():
    from math import sin
    global x, y
    x = 200 + sin(frame_count * 0.04) * 75
    y = 230
```

## Test

Run your code. Watch the pet move left and right. Click its body while it moves to check it still reacts.

## Make it yours

Change **0.04** for the speed and **75** for the distance. Try small changes first. Keep your pet inside the canvas.

[Choose another part](landing.md).
