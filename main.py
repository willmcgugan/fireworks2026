#!/usr/bin/env python3
"""
Fireworks simulation using Braille canvas.
"""

import math
import random
import time
import os
from typing import List, Tuple
from braille_canvas import BrailleCanvas


class Particle:
    """A 3D particle with position, velocity, and lifetime."""
    
    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float, 
                 color: str, lifetime: float):
        """
        Initialize a particle.
        
        Args:
            x, y, z: Initial 3D position
            vx, vy, vz: Initial 3D velocity
            color: RGB color string
            lifetime: Time in seconds before particle disappears
        """
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        
    def update(self, dt: float, gravity: float = 20.0, air_resistance: float = 0.95):
        """
        Update particle position and age.
        
        Args:
            dt: Time delta in seconds
            gravity: Gravity acceleration (pixels/s^2)
            air_resistance: Air resistance factor (0-1, closer to 1 = less resistance)
        """
        # Apply gravity to vertical velocity
        self.vy += gravity * dt
        
        # Apply air resistance (damping) to all velocities
        # This causes particles to slow down over time
        damping = air_resistance ** dt
        self.vx *= damping
        self.vy *= damping
        self.vz *= damping
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        
        # Update age
        self.age += dt
        
    def is_alive(self) -> bool:
        """Check if particle is still alive."""
        return self.age < self.lifetime
    
    def get_2d_position(self, camera_distance: float = 200.0, center_x: float = 0.0, center_y: float = 0.0) -> Tuple[int, int]:
        """
        Get 2D screen position with perspective projection.
        
        Args:
            camera_distance: Distance of camera from z=0 plane
            center_x: X coordinate of screen center (camera looks at this point)
            center_y: Y coordinate of screen center (camera looks at this point)
            
        Returns:
            (x, y) screen coordinates
        """
        # Perspective projection: closer objects (negative z) appear larger
        # Objects at z=0 are at the "screen" plane
        # Objects with positive z are behind the screen (appear smaller)
        z_offset = self.z + camera_distance
        
        if z_offset <= 0:
            # Particle is behind camera, don't render
            return (-1, -1)
        
        # Apply perspective scaling relative to screen center
        scale = camera_distance / z_offset
        
        # Project relative to center, then add center back
        screen_x = center_x + (self.x - center_x) * scale
        screen_y = center_y + (self.y - center_y) * scale
        
        return (int(screen_x), int(screen_y))


class Firework:
    """A firework that launches, arcs, and explodes."""
    
    def __init__(self, canvas_width: int, canvas_height: int):
        """
        Initialize a firework.
        
        Args:
            canvas_width: Width of the canvas in pixels
            canvas_height: Height of the canvas in pixels
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        
        # Random neon color
        self.color = self._random_neon_color()
        
        # Launch from bottom of screen
        self.x = random.uniform(canvas_width * 0.2, canvas_width * 0.8)
        self.y = canvas_height - 1
        self.z = 0.0
        
        # Launch velocity (upward with slight horizontal drift)
        self.vx = random.uniform(-20, 20)
        self.vy = random.uniform(-150, -120)  # Strong upward velocity
        self.vz = 0.0
        
        # Explosion parameters
        self.exploded = False
        self.particles: List[Particle] = []
        
        # Trail particle for launch phase
        self.launch_trail: List[Tuple[float, float]] = []
        
    def _random_neon_color(self) -> str:
        """Generate a random neon color."""
        neon_colors = [
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow
            (255, 0, 128),    # Hot pink
            (0, 255, 128),    # Spring green
            (255, 128, 0),    # Orange
            (128, 0, 255),    # Purple
            (255, 0, 0),      # Red
            (0, 255, 0),      # Green
            (0, 128, 255),    # Light blue
        ]
        r, g, b = random.choice(neon_colors)
        return BrailleCanvas.rgb_color(r, g, b)
    
    def update(self, dt: float):
        """
        Update firework state.
        
        Args:
            dt: Time delta in seconds
        """
        if not self.exploded:
            # Update launch phase
            gravity = 100.0
            self.vy += gravity * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            
            # Store trail position
            self.launch_trail.append((self.x, self.y))
            if len(self.launch_trail) > 15:
                self.launch_trail.pop(0)
            
            # Check if we should explode (when velocity becomes positive or reaches apex)
            if self.vy > -20:
                self.explode()
        else:
            # Update explosion particles
            for particle in self.particles:
                particle.update(dt)
            
            # Remove dead particles
            self.particles = [p for p in self.particles if p.is_alive()]
    
    def explode(self):
        """Create explosion particles."""
        self.exploded = True
        
        # Generate particles in all directions (more particles, slower speed)
        num_particles = random.randint(270, 450)
        speed = random.uniform(25, 40)
        
        for i in range(num_particles):
            # Random direction on a sphere
            theta = random.uniform(0, 2 * math.pi)  # Azimuthal angle
            phi = random.uniform(0, math.pi)  # Polar angle
            
            # Convert to Cartesian coordinates
            vx = speed * math.sin(phi) * math.cos(theta)
            vy = speed * math.cos(phi)
            vz = speed * math.sin(phi) * math.sin(theta)
            
            # Random lifetime with some variation (around 2-3 seconds)
            base_lifetime = random.uniform(1.8, 2.5)
            lifetime_variation = random.uniform(-0.2, 0.2)
            lifetime = base_lifetime + lifetime_variation
            
            particle = Particle(
                self.x, self.y, self.z,
                vx, vy, vz,
                self.color,
                lifetime
            )
            self.particles.append(particle)
    
    def render(self, canvas: BrailleCanvas):
        """
        Render firework to canvas.
        
        Args:
            canvas: BrailleCanvas to render to
        """
        if not self.exploded:
            # Render launch trail - collect all points first
            if self.launch_trail:
                points = [(int(x), int(y)) for x, y in self.launch_trail 
                         if 0 <= x < canvas.width and 0 <= y < canvas.height]
                if points:
                    canvas.plot(self.color, points)
        else:
            # Render explosion particles with perspective - batch processing
            # Pre-allocate list with estimated size for better performance
            points = []
            canvas_w = canvas.width
            canvas_h = canvas.height
            center_x = canvas_w / 2.0
            center_y = canvas_h / 2.0
            
            for particle in self.particles:
                pos = particle.get_2d_position(camera_distance=200.0, center_x=center_x, center_y=center_y)
                # Check bounds and that particle is visible (not behind camera)
                x, y = pos
                if 0 <= x < canvas_w and 0 <= y < canvas_h:
                    points.append(pos)
            
            if points:
                canvas.plot(self.color, points)
    
    def is_finished(self) -> bool:
        """Check if firework is finished (exploded and all particles dead)."""
        return self.exploded and len(self.particles) == 0


def main():
    """Main fireworks simulation loop."""
    # Get terminal size
    try:
        columns, rows = os.get_terminal_size()
    except OSError:
        columns, rows = 80, 24
    
    # Canvas dimensions (pixels)
    canvas_width = columns * 2
    canvas_height = rows * 4
    
    # Create canvas
    canvas = BrailleCanvas(canvas_width, canvas_height, default_color=0)
    
    # Fireworks list
    fireworks: List[Firework] = []
    
    # Timing
    target_fps = 60
    frame_time = 1.0 / target_fps
    last_spawn_time = 0.0
    spawn_interval = random.uniform(0.5, 1.5)  # Spawn new firework every 0.5-1.5 seconds
    
    # Hide cursor
    print("\033[?25l", end="")
    
    try:
        start_time = time.time()
        last_frame_time = start_time
        
        while True:
            current_time = time.time()
            dt = current_time - last_frame_time
            
            # Limit frame rate
            if dt < frame_time:
                time.sleep(frame_time - dt)
                current_time = time.time()
                dt = current_time - last_frame_time
            
            last_frame_time = current_time
            elapsed = current_time - start_time
            
            # Spawn new fireworks
            if elapsed - last_spawn_time > spawn_interval:
                fireworks.append(Firework(canvas_width, canvas_height))
                last_spawn_time = elapsed
                spawn_interval = random.uniform(0.5, 1.5)
            
            # Update all fireworks
            for firework in fireworks:
                firework.update(dt)
            
            # Remove finished fireworks
            fireworks = [f for f in fireworks if not f.is_finished()]
            
            # Clear canvas
            canvas.clear(0)
            
            # Render all fireworks
            for firework in fireworks:
                firework.render(canvas)
            
            # Render to screen (single write operation is faster)
            output = "\033[H" + canvas.render()
            print(output, end="")
            
    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor
        print("\033[?25h")
        print("\nFireworks simulation ended.")


if __name__ == "__main__":
    main()
