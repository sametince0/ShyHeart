import pygame
import math
import random

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (20, 5, 10)   
HEART_COLOR = (255, 40, 90)      
NUM_PARTICLES = 12000            
INTERACTION_RADIUS = 40          
RETURN_SPEED = 0.04              
FRICTION = 0.88                  
SCATTER_STRENGTH = 25            

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Korkan Kalp Noktaları - Samet")
clock = pygame.time.Clock()

class Particle:
    def __init__(self, target_x, target_y):
        self.target_x = target_x  
        self.target_y = target_y  
        self.x = random.randint(0, WIDTH)  
        self.y = random.randint(0, HEIGHT)
        self.vx = 0  
        self.vy = 0  
        
        self.size = random.randint(2, 4) 
        
        color_var = random.randint(-50, 20)
        r = max(100, min(255, HEART_COLOR[0] + color_var))
        g = max(0, min(255, HEART_COLOR[1] + color_var // 2))
        b = max(0, min(255, HEART_COLOR[2] + color_var // 2))
        self.color = (r, g, b)

    def update(self, mouse_x, mouse_y):
        dx = self.x - mouse_x
        dy = self.y - mouse_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < INTERACTION_RADIUS:
            force = (INTERACTION_RADIUS - distance) / INTERACTION_RADIUS
            angle = math.atan2(dy, dx)
            
            push_x = math.cos(angle) * force * SCATTER_STRENGTH
            push_y = math.sin(angle) * force * SCATTER_STRENGTH
            
            self.vx += push_x
            self.vy += push_y

        home_dx = self.target_x - self.x
        home_dy = self.target_y - self.y
        
        self.vx += home_dx * RETURN_SPEED
        self.vy += home_dy * RETURN_SPEED
        
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

def get_filled_heart_points(num_points, scale=13):
    points = []
    for _ in range(num_points):
        t = random.uniform(0, math.pi * 2)
        
        r = math.sqrt(random.random())
        
        x = 16 * math.sin(t)**3
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        
        x *= r
        y *= r
        
        px = WIDTH // 2 + x * scale
        py = HEIGHT // 2 - y * scale 
        
        points.append((px, py))
    return points

def main():
    running = True
    
    heart_coordinates = get_filled_heart_points(NUM_PARTICLES, scale=15)
    particles = [Particle(x, y) for x, y in heart_coordinates]

    while running:
        screen.fill(BACKGROUND_COLOR)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for p in particles:
            p.update(mouse_x, mouse_y)
            p.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()