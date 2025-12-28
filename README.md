# Braille Canvas

A high-performance Braille canvas for terminal graphics in Python. Uses Unicode Braille characters (U+2800-U+28FF) to achieve 2x4 pixel resolution per character, allowing for detailed graphics in the terminal.

## Features

- **High Resolution**: Each Braille character represents a 2x4 pixel grid, providing excellent detail
- **8-Color Palette**: Supports standard ANSI terminal colors (Black, Red, Green, Yellow, Blue, Magenta, Cyan, White)
- **Efficient Rendering**: Optimized for performance with direct buffer manipulation
- **Line Drawing**: Bresenham's algorithm for fast, accurate line drawing
- **Batch Plotting**: Plot multiple points at once from any iterable

## Installation

No external dependencies required! Uses only Python standard library.

## Usage

### Basic Example

```python
from braille_canvas import BrailleCanvas

# Create a canvas (width and height in pixels)
canvas = BrailleCanvas(80, 40, default_color=0)

# Plot individual points
points = [(10, 10), (11, 10), (12, 11)]
canvas.plot(color=1, points=points)  # Red points

# Draw a line
canvas.line(x0=0, y0=0, x1=79, y1=39, color=2)  # Green diagonal

# Clear the canvas
canvas.clear(color=0)  # Clear with black

# Render to terminal
print(canvas.render())
# or simply
print(canvas)
```

### Drawing Shapes

```python
import math
from braille_canvas import BrailleCanvas

canvas = BrailleCanvas(80, 40, default_color=0)

# Draw a circle
center_x, center_y = 40, 20
radius = 15
circle_points = []
for angle in range(0, 360, 2):
    rad = math.radians(angle)
    x = int(center_x + radius * math.cos(rad))
    y = int(center_y + radius * math.sin(rad))
    circle_points.append((x, y))

canvas.plot(1, circle_points)  # Red circle
print(canvas)
```

## API Reference

### `BrailleCanvas(width: int, height: int, default_color: int = 7)`

Create a new Braille canvas.

- `width`: Canvas width in pixels (not characters)
- `height`: Canvas height in pixels (not characters)
- `default_color`: Default color index (0-7), defaults to white

### `plot(color: int, points: Iterable[Tuple[int, int]])`

Plot multiple points with the given color.

- `color`: Color index (0-7)
- `points`: Iterable of (x, y) coordinate tuples

### `line(x0: int, y0: int, x1: int, y1: int, color: int)`

Draw a line using Bresenham's algorithm.

- `x0, y0`: Starting point coordinates
- `x1, y1`: Ending point coordinates
- `color`: Color index (0-7)

### `clear(color: int = 7)`

Clear the canvas with a single color.

- `color`: Color index (0-7) to fill the canvas with

### `render() -> str`

Render the canvas to a string with ANSI color codes.

Returns a string that can be printed to the terminal.

## Color Palette

| Index | Color   | ANSI Code |
|-------|---------|-----------|
| 0     | Black   | `\033[30m` |
| 1     | Red     | `\033[31m` |
| 2     | Green   | `\033[32m` |
| 3     | Yellow  | `\033[33m` |
| 4     | Blue    | `\033[34m` |
| 5     | Magenta | `\033[35m` |
| 6     | Cyan    | `\033[36m` |
| 7     | White   | `\033[37m` |

## How It Works

### Braille Characters

Braille characters in Unicode use a 2x4 dot pattern:

```
0 3
1 4
2 5
6 7
```

Each dot can be individually controlled using bit positions in the Unicode range U+2800-U+28FF. This allows for 256 different patterns per character.

### Performance

- **Direct Buffer Access**: The canvas stores Braille patterns and colors in a 2D array for O(1) access
- **Efficient Line Drawing**: Bresenham's algorithm draws lines without floating-point arithmetic
- **Color Optimization**: Only emits ANSI color codes when the color changes

## Running the Demo

```bash
python demo.py
```

The demo showcases:
- Plotting points to create shapes
- Drawing lines with the star pattern
- Multi-colored sine waves
- Grid patterns
- Clear functionality

## License

MIT
