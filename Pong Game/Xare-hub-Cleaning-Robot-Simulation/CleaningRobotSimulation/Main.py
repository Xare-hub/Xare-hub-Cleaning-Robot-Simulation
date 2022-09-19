from pathlib import Path
import numpy as np
import pygame
from WALL_CORNERS import WALL_CORNERS
from helper_functions import rand_vel0, collision_scan, robot_collision_handler, cleaning_percentage
from Classes import Line, Robot, Rect, draw, WHITE


pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotated Rectangle")

FPS = 400

# Initialize the list of vectors with line objects
lines = [Line] * 24

#Create list to store the fps at each frame
fps_list = []
clock_simulation = pygame.time.Clock()

def main():
    run = True
    clock = pygame.time.Clock()

    lines = [Line(WALL_CORNERS[i], WALL_CORNERS[i+1]) for i in range(0, len(WALL_CORNERS)-1)]
    
    robot = Robot(629, 238, 15)
    # rand_vel0(robot)                                        # comment this line to return to random direction each run
    # initial_direction = [robot.x_vel, robot.y_vel]
    
    # uncomment next lines to define a normalized specific direction for the robot
    robot.x_vel = -0.42
    robot.y_vel = -0.26
    initial_direction = [robot.x_vel, robot.y_vel]

    # uncomment next lines to define a specific direction in terms of the x and y vel components:
    # robot.x_vel = vel[0]
    # robot.y_vel = vel[1]

    

    # Load room image to background
    background = pygame.image.load("Pong Game/Xare-hub-Cleaning-Robot-Simulation/CleaningRobotSimulation/room.png")
    WIN.blit(background, (0,0))

    # Extract the pixel values from the frame image, only from the square that engulfs the room
    imgdata = pygame.surfarray.pixels3d(WIN)
    total_red_pixels = np.sum(imgdata[30:743,54:640,:] == (255, 174, 201))

    counter = 0
    cln_perc = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # pygame.display.flip()
        # WIN.blit(background, (0,0))

        robot.move()
        collision_detected, Normal_vector = collision_scan(WALL_CORNERS, (robot.x_center, robot.y_center), robot.radius, robot, verbose = False)


        if collision_detected and not(robot.recent_collision):
            robot_collision_handler(robot, Normal_vector, rand_angle=True)

        draw(WIN, lines, robot)

        
        counter += 1
        if counter % 1000 == 0:
            cln_perc = cleaning_percentage(WIN, total_red_pixels, verbose=True)           
        
        if cln_perc >= 90:
            break
        
        fps_list.append(clock.get_fps())
        clock.tick(FPS)
    
    clock_simulation.tick()

    simulation_time = clock_simulation.get_time()
    print("Simulation time: " + str(simulation_time/1000) + " seconds")
    print("Initial robot direction: ({:.4f}, {:.4f})".format(initial_direction[0], initial_direction[1]) )
    
    pygame.quit()

    print("Avergae fps: " + str(np.average(fps_list)))


if __name__ == '__main__':
    main()
