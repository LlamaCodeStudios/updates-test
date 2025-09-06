import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(100, 100)]
direction = (CELL_SIZE, 0)
food = (300, 200)

def draw():
    screen.fill((0, 0, 0))
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, (255, 0, 0), (*food, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def move():
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)
    if head == food:
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN: direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT: direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT: direction = (CELL_SIZE, 0)

    move()
    if check_collision():
        pygame.quit()
        sys.exit()

    draw()
    clock.tick(10)
