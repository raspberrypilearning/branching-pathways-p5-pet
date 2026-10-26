## 3B - Make an angular body

Circles are only one possibility. Try building with rectangles and triangles.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **draw_body()**. A rectangle uses its top-left corner, then width and height.

```python
def draw_body():
    fill('gold')
    rect(x - 50, y - 45, 100, 90)
    fill('orange')
    triangle(x - 25, y - 45, x, y - 75, x + 25, y - 45)
    rect(x - 65, y - 10, 15, 35)
    rect(x + 50, y - 10, 15, 35)
```

## Test

Run your code. Click the middle of the body to check the reaction still works.

## Make it yours

Change the top into a horn, aerial or mountain peak. Keep your face visible. If you make a much bigger body, adjust its clickable area in [Click your pet](2A%20-%20Click%20your%20pet.md).

[Choose another part](landing.md).
