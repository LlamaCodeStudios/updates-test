import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
import subprocess

# 🔄 Run updater.py before game starts
subprocess.run(["python", "updater.py"])

# Initialize tkinter and pygame
root = tk.Tk()
root.withdraw()
pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# 🖼️ Load sprites
bg_img = pygame.image.load("assets/bg.png").convert()
snake_img = pygame.image.load("assets/snake.png").convert_alpha()
apple_img = pygame.image.load("assets/apple.png").convert_alpha()

# 🖱️ Click to start screen
font = pygame.font.SysFont(None, 48)
screen.blit(bg_img, (0, 0))
text = font.render("Click anywhere to start", True, (255, 255, 255))
rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(text, rect)
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            waiting = False

# Game state
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
food = (300, 200)
score = 0

def draw():
    screen.blit(bg_img, (0, 0))
    for segment in snake:
        screen.blit(snake_img, segment)
    screen.blit(apple_img, food)
    pygame.display.flip()

def move():
    global score
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)
    if head == food:
        score += 1
        spawn_food()
    else:
        snake.pop()

def spawn_food():
    global food
    food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)

def check_collision():
    head = snake[0]
    return (head in snake[1:] or
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT)

def is_opposite(new_dir, current_dir):
    return (new_dir[0] == -current_dir[0] and new_dir[1] == -current_dir[1])

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            new_direction = direction
            if event.key == pygame.K_UP:
                new_direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN:
                new_direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT:
                new_direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                new_direction = (CELL_SIZE, 0)
            if not is_opposite(new_direction, direction):
                direction = new_direction

    move()
    if check_collision():
        messagebox.showinfo("Game Over", f"The game is over :(\nYour score: {score}")
        pygame.quit()
        sys.exit()

    draw()
    clock.tick(10)
