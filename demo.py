#!/usr/bin/env python3
"""
Demonstration of the BrailleCanvas capabilities.
"""

import math
from braille_canvas import BrailleCanvas


def demo_plot():
    """Demonstrate the plot method with various shapes."""
    print("Demo: Plotting points")
    print("-" * 50)
    
    canvas = BrailleCanvas(80, 40, default_color=0)
    
    # Draw a circle using plot
    center_x, center_y = 40, 20
    radius = 15
    circle_points = []
    for angle in range(0, 360, 2):
        rad = math.radians(angle)
        x = int(center_x + radius * math.cos(rad))
        y = int(center_y + radius * math.sin(rad))
        circle_points.append((x, y))
    
    canvas.plot(1, circle_points)  # Red circle
    
    # Draw a square
    square_points = []
    for i in range(20):
        square_points.append((10 + i, 5))
        square_points.append((10 + i, 15))
        square_points.append((10, 5 + i))
        square_points.append((30, 5 + i))
    
    canvas.plot(2, square_points)  # Green square
    
    # Draw random scattered points
    import random
    random.seed(42)
    scattered = [(random.randint(50, 75), random.randint(25, 38)) for _ in range(50)]
    canvas.plot(3, scattered)  # Yellow points
    
    print(canvas)
    print()


def demo_lines():
    """Demonstrate line drawing."""
    print("Demo: Drawing lines")
    print("-" * 50)
    
    canvas = BrailleCanvas(80, 40, default_color=0)
    
    # Draw a star pattern
    center_x, center_y = 40, 20
    colors = [1, 2, 3, 4, 5, 6, 7]
    
    for i, angle in enumerate(range(0, 360, 45)):
        rad = math.radians(angle)
        x = int(center_x + 30 * math.cos(rad))
        y = int(center_y + 15 * math.sin(rad))
        canvas.line(center_x, center_y, x, y, colors[i % len(colors)])
    
    print(canvas)
    print()


def demo_clear():
    """Demonstrate clearing with different colors."""
    print("Demo: Clear with different background colors")
    print("-" * 50)
    
    canvas = BrailleCanvas(80, 40)
    
    # Draw some content
    canvas.line(10, 10, 70, 30, 7)
    canvas.line(10, 30, 70, 10, 7)
    print("Before clear:")
    print(canvas)
    print()
    
    # Clear with blue background
    canvas.clear(4)
    canvas.line(40, 0, 40, 39, 7)  # White vertical line
    canvas.line(0, 20, 79, 20, 7)  # White horizontal line
    print("After clear (blue background):")
    print(canvas)
    print()


def demo_sine_wave():
    """Draw a colorful sine wave."""
    print("Demo: Multi-colored sine wave")
    print("-" * 50)
    
    canvas = BrailleCanvas(160, 40, default_color=0)
    
    # Generate sine wave points
    for color_offset in range(8):
        points = []
        for x in range(160):
            y = int(20 + 10 * math.sin((x + color_offset * 10) * 0.1))
            points.append((x, y))
        canvas.plot(color_offset, points)
    
    print(canvas)
    print()


def demo_grid():
    """Draw a colored grid."""
    print("Demo: Colored grid")
    print("-" * 50)
    
    canvas = BrailleCanvas(80, 40, default_color=0)
    
    # Vertical lines
    for x in range(0, 80, 10):
        canvas.line(x, 0, x, 39, 6)  # Cyan
    
    # Horizontal lines
    for y in range(0, 40, 5):
        canvas.line(0, y, 79, y, 5)  # Magenta
    
    # Diagonal
    canvas.line(0, 0, 79, 39, 3)  # Yellow
    canvas.line(79, 0, 0, 39, 3)  # Yellow
    
    print(canvas)
    print()


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 50)
    print("BRAILLE CANVAS DEMONSTRATION")
    print("=" * 50 + "\n")
    
    demo_plot()
    demo_lines()
    demo_sine_wave()
    demo_grid()
    demo_clear()
    
    print("\nColor palette:")
    print("0: Black, 1: Red, 2: Green, 3: Yellow")
    print("4: Blue, 5: Magenta, 6: Cyan, 7: White")


if __name__ == "__main__":
    main()
