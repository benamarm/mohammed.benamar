# Code from https://github.com/Karthikeyanc2/Autonomous-snake-game-with-A-star-algorithm-in-PYTHON
from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt
init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

cols = 25
rows = 25

width = 600
height = 600
wr = width/cols
hr = height/rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()


def getpath(food1, snake1):
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    # openset = array of unexplored Spots, initialize with latest Spot of Snake
    openset = [snake1[-1]]
    # closedset = array of explored Spots
    closedset = []
    # Array of direction to follow for path to food
    dir_array1 = []
    # While until we find the food
    while openset:
        # current1 = explored Spot with lowest f-cost
        current1 = min(openset, key=lambda x: x.f)
        # Remove current1 from openset, add to closedset
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        # Iterate through neighbors of current1
        for neighbor in current1.neighbors:
            # If neighbor is unexplored, not an obstacle, and not part of snake
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                # g-cost between two Spots is 1
                tempg = current1.g + 1
                # If neighbor was previously explored with higher g-cost, update to cheaper g-cost
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                # Else add it to explored neighbors
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                # h-cost = distance in number of Spots (x-difference + y-difference)
                # neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.h = abs(neighbor.x - food1.x) + abs(neighbor.y - food1.y)
                neighbor.f = neighbor.g + neighbor.h
                # Keep trace of how neighbor was explored, to finally form chain path to food
                neighbor.camefrom = current1
        if current1 == food1:
            break
    # Make array of directions that lead to food
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)
        current1 = current1.camefrom
    # Clear all Spots
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return dir_array1


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False
        if randint(1, 101) < 3:
            self.obstrucle = True

    def show(self, color):
        draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


# Populate all Spots and initialize their neighbors array (2, 3, or 4 surrounding Spots)
grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

# Snake is an array of Spots, for now only contains Spot in middle of map
snake = [grid[round(rows/2)][round(cols/2)]]
# Food = random Spot
food = grid[randint(0, rows-1)][randint(0, cols-1)]
# Current position = last Spot added to snake
current = snake[-1]
dir_array = getpath(food, snake)
food_array = [food]

while not done:
    clock.tick(12)
    screen.fill(BLACK)
    direction = dir_array.pop(-1)
    if direction == 0:    # down
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]

    if current.x == food.x and current.y == food.y:
        while 1:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food.obstrucle or food in snake):
                break
        food_array.append(food)
        dir_array = getpath(food, snake)
    else:
        snake.pop(0)

    for spot in snake:
        spot.show(WHITE)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstrucle:
                grid[i][j].show(RED)

    food.show(GREEN)
    snake[-1].show(BLUE)
    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_w and not direction == 0:
                direction = 2
            elif event.key == K_a and not direction == 1:
                direction = 3
            elif event.key == K_s and not direction == 2:
                direction = 0
            elif event.key == K_d and not direction == 3:
                direction = 1