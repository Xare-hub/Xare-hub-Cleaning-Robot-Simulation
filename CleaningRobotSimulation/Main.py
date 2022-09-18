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

    robot = Robot(154, 141, 15)
    rand_vel0(robot) # comment this line to return to random direction each run
    
    # robot.x_vel = vel[0]
    # robot.y_vel = vel[1]
    
    # direction = [-5,5]  #set fixed initial direction
    # f = 2   # change to modify pixels traveled per frame
    # vel = direction/np.linalg.norm(direction)   # get unitary vector with the direction chose   
    # robot.x_vel = 2
    # robot.y_vel = 2

    while run:
        clock.tick(FPS)
        draw(WIN, [Border], lines, robot)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        robot.move()
        collision_detected, Normal_vector = collision_scan(WALL_CORNERS, (robot.x_center, robot.y_center), robot.radius, robot, verbose = True)


        if collision_detected and not(robot.recent_collision):
            robot_collision_handler(robot, Normal_vector)

    
    pygame.quit()


if __name__ == '__main__':
    main()
