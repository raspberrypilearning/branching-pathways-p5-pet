## 4C - Follow the pointer

Where you move, your pet follows.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **move_pet()**. The limits keep the centre away from the edges.

```python
def move_pet():
    global x, y
    x = max(70, min(330, mouse_x))
    y = max(100, min(270, mouse_y))
```

## Test

Run your code. Move your pointer around the visual output and into each corner. The pet should follow and stop near the edges.

## Make it yours

Make a pet that only follows sideways by replacing the last line with **y = 230**. On a touchscreen, try dragging a finger across the canvas.

[Choose another part](landing.md).
