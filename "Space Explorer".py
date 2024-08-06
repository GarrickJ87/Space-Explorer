import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Define a class for each grid unit on the board
class SpaceUnit(object):
    grid_size = 20
    screen_size = 500
    
    def __init__(self, start_position, dir_x=1, dir_y=0, color=(0, 255, 255)):
        self.position = start_position
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.color = color

    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.position = (self.position[0] + self.dir_x, self.position[1] + self.dir_y)

    def draw(self, surface, with_lights=False):
        distance = self.screen_size // self.grid_size
        i, j = self.position
        
        pygame.draw.rect(surface, self.color, (i*distance+1, j*distance+1, distance-2, distance-2))
        if with_lights:
            center = distance // 2
            radius = 3
            circle_middle1 = (i * distance + center - radius, j * distance + 8)
            circle_middle2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (255, 255, 0), circle_middle1, radius)
            pygame.draw.circle(surface, (255, 255, 0), circle_middle2, radius)

# Define a class for the spaceship
class SpaceShip(object):
    body = []
    direction_changes = {}

    def __init__(self, color, start_pos):
        self.color = color
        self.head = SpaceUnit(start_pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.direction_changes[self.head.position[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.direction_changes[self.head.position[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_UP]:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.direction_changes[self.head.position[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.direction_changes[self.head.position[:]] = [self.dir_x, self.dir_y]

        for i, unit in enumerate(self.body):
            position = unit.position[:]
            if position in self.direction_changes:
                turn = self.direction_changes[position]
                unit.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.direction_changes.pop(position)
            else:
                if unit.dir_x == -1 and unit.position[0] <= 0:
                    unit.position = (unit.grid_size - 1, unit.position[1])
                elif unit.dir_x == 1 and unit.position[0] >= unit.grid_size - 1:
                    unit.position = (0, unit.position[1])
                elif unit.dir_y == 1 and unit.position[1] >= unit.grid_size - 1:
                    unit.position = (unit.position[0], 0)
                elif unit.dir_y == -1 and unit.position[1] <= 0:
                    unit.position = (unit.position[0], unit.grid_size - 1)
                else:
                    unit.move(unit.dir_x, unit.dir_y)

    def reset(self, start_pos):
        self.head = SpaceUnit(start_pos)
        self.body = []
        self.body.append(self.head)
        self.direction_changes = {}
        self.dir_x = 0
        self.dir_y = 1

    def add_unit(self):
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y

        if dx == 1 and dy == 0:
            self.body.append(SpaceUnit((tail.position[0] - 1, tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(SpaceUnit((tail.position[0] + 1, tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(SpaceUnit((tail.position[0], tail.position[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(SpaceUnit((tail.position[0], tail.position[1] + 1)))

        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy

    def draw(self, surface):
        for i, unit in enumerate(self.body):
            if i == 0:
                unit.draw(surface, True)
            else:
                unit.draw(surface)

# Define functions to draw the game grid
def draw_grid(screen_size, grid_size, surface):
    distance_between = screen_size // grid_size
    x = 0
    y = 0
    for line in range(grid_size):
        x += distance_between
        y += distance_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, screen_size))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (screen_size, y))

def redraw_window(surface):
    global grid_size, screen_size, spaceship, energy_orb
    surface.fill((0, 0, 0))
    spaceship.draw(surface)
    energy_orb.draw(surface)
    draw_grid(screen_size, grid_size, surface)
    pygame.display.update()

def random_position(grid_size, items):
    positions = items.body
    while True:
        x = random.randrange(grid_size)
        y = random.randrange(grid_size)
        if len(list(filter(lambda z: z.position == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global screen_size, grid_size, spaceship, energy_orb
    screen_size = 500
    grid_size = 20
    win = pygame.display.set_mode((screen_size, screen_size))
    spaceship = SpaceShip((0, 255, 255), (10, 10))
    energy_orb = SpaceUnit(random_position(grid_size, spaceship), color=(255, 0, 0))
    running = True

    clock = pygame.time.Clock()

    while running:
        pygame.time.delay(50)
        clock.tick(10)
        spaceship.move()
        if spaceship.body[0].position == energy_orb.position:
            spaceship.add_unit()
            energy_orb = SpaceUnit(random_position(grid_size, spaceship), color=(255, 0, 0))

        for x in range(len(spaceship.body)):
            if spaceship.body[x].position in list(map(lambda z: z.position, spaceship.body[x + 1:])):
                print('Score: ', len(spaceship.body))
                message_box('You Crashed!', 'Play again...')
                spaceship.reset((10, 10))
                break

        redraw_window(win)

    pass

main()
