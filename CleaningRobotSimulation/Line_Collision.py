import numpy as np
import pygame
import helper_functions


pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotated Rectangle")

FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)

PADDLE_HEIGHT, PADDLE_WIDTH = 100, 20

class Line:
    COLOR = WHITE

    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
    
    def draw(self, win):
        pygame.draw.line(win, self.COLOR, self.start_pos, self.end_pos, width = 2)

class Robot:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x_center, y_center, radius):
        self.x_center = x_center
        self.y_center = y_center
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x_center, self.y_center), self.radius)

    def move(self):
        self.x_center += self.x_vel
        self.y_center += self.y_vel


def draw(win, borders, lines, robot):
    win.fill(BLACK)
    
    for border in borders:
        border.draw(win)

    for line in lines:
        line.draw(win)

    robot.draw(win)

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    _ = []

    lines = Line((400,0), (400,800))
    robot = Robot(200,400,10)
    helper_functions.rand_vel0(robot)

    print(lines)
            

    #line1 = Line((20,20), (400,400))
    while run:
        clock.tick(FPS)
        draw(WIN, _, [lines], robot)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        robot.move()
    pygame.quit()


if __name__ == '__main__':
    main()
