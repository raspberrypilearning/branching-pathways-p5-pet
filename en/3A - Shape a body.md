## 3A - Shape a body

Build a creature from a few shapes. It does not have to be an animal anyone has seen before.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **draw_body()**. The ears are drawn first so the body sits in front of them. The face is drawn separately.

```python
def draw_body():
    fill('orchid')
    ellipse(x - 35, y - 45, 25, 65)
    ellipse(x + 35, y - 45, 25, 65)
    ellipse(x, y, 110, 100)
```

## Test

Run your code and click your pet. Your new body should still have a face that reacts.

## Make it yours

Try wide ears, tiny ears or no ears. An ellipse uses centre x, centre y, width and height. Keep positions relative to **x** and **y** so every part moves together.

[Choose another part](landing.md).
