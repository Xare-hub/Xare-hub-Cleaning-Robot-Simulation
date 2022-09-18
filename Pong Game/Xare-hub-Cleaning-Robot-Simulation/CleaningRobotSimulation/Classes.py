import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)
LIGHT_GREEN = (69, 245, 99)


class Rect:
    COLOR = WHITE

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height), width = 5)

class Line:
    COLOR = WHITE

    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
    
    def draw(self, win):
        pygame.draw.line(win, self.COLOR, self.start_pos, self.end_pos, width = 2)

class Robot:
    MAX_VEL = 5
    EDGE_COLOR = LIGHT_GREEN
    ROBOT_COLOR = WHITE 

    def __init__(self, x_center, y_center, radius):
        self.x_center = x_center
        self.y_center = y_center
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        self.recent_collision = False

    def draw(self, win):
        pygame.draw.circle(win, self.ROBOT_COLOR, (self.x_center, self.y_center), self.radius)
        pygame.draw.circle(win, self.EDGE_COLOR, (self.x_center, self.y_center), self.radius, 2)
        

    def move(self):
        self.x_center += self.x_vel
        self.y_center += self.y_vel


def draw(win, lines, robot):
    # win.fill(BLACK)

    for line in lines:
        line.draw(win)

    robot.draw(win)

    pygame.display.update()