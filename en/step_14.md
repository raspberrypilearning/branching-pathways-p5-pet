## 6B - Invent a strange world

Your pet does not need an ordinary home.

> [!CAUTION]
>
> Have you [run your starter](1A%20-%20Meet%20your%20pet.md)? That is the only step you need first.

## Try the code

Replace **draw_home()**. These repeated shapes could become stars, bubbles or stepping stones.

```python
def draw_home():
    background('midnightblue')
    fill('lightcyan')
    for star_x in range(30, 400, 70):
        circle(star_x, 60, 6)
        circle(star_x + 20, 130, 4)
    fill('mediumpurple')
    circle(340, 230, 75)
    fill('lavender')
    rect(0, 330, 400, 70)
```

## Test

Run your code. Count the repeated shapes. Check the pet and its message are easy to see against the new background.

## Make it yours

Change the colours and circle sizes to make an underwater home. Change **70** to adjust the gap between repeated shapes.

[Choose another part](landing.md).
