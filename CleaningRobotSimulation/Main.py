import numpy as np
import pygame
from WALL_CORNERS import WALL_CORNERS
from helper_functions import rand_vel0, collision_scan, robot_collision_handler
from Classes import Line, Robot, Rect, draw


pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotated Rectangle")

FPS = 60

lines = [Line] * 24


def main():
    run = True
    clock = pygame.time.Clock()
    _ = []
    Border = Rect(10, 10, 780, 780)
    
    lines = [Line(WALL_CORNERS[i], WALL_CORNERS[i+1]) for i in range(0, len(WALL_CORNERS)-1)]

    robot = Robot(362, 480, 15)
    rand_vel0(robot)    

    recent_collision = False
    counter = 0
    while run:
        clock.tick(FPS)
        draw(WIN, [Border], lines, robot)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        robot.move()
        collision_detected, Normal_vector = collision_scan(WALL_CORNERS, (robot.x_center, robot.y_center), robot.radius, verbose = False)

        if collision_detected:
            robot_collision_handler(robot, Normal_vector)
    
    pygame.quit()


if __name__ == '__main__':
    main()
