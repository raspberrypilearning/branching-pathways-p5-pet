## 3C - Add decorations

Give your pet a detail that makes it yours.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **draw_accessories()**. This draws on top of the body and face.

```python
def draw_accessories():
    fill('tomato')
    triangle(x - 30, y - 45, x, y - 95, x + 30, y - 45)
    fill('gold')
    circle(x, y - 95, 12)
```

## Test

Run your code. Your pet should wear a hat. If you have chosen movement, the hat should move with it.

## Make it yours

Turn the hat into hair or a crown. Add spots with circles. Use **x +** or **y -** to keep decorations attached to your pet.

[Choose another part](landing.md).
