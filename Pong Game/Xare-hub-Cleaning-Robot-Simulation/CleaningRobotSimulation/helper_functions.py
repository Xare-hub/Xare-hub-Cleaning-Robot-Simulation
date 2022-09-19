from cmath import pi
import numpy as np
from numpy.linalg import norm
from WALL_CORNERS import WALL_CORNERS
import pygame
import time

def rand_vel0(robot):
    """
    This function receives a robot object and modifies its x_vel and y_vel
    values, so that the robot starts moving in a different direction at the
    same speed in each run of the simulation
    """
    angle = np.random.random()*pi        # Increases the possibility of choosing a different direction
    
    x_speed = np.cos(angle)
    y_speed = np.sin(angle)
    
    #Produces unitary vector for a random direction. each pixel equals 1 squared centimeter
    robot.x_vel = x_speed*0.5
    robot.y_vel = y_speed*0.5

def dist_point2line(P1,P2, P3, verbose = False):
    """
    This function gets the shortest distance between a point P3 and a line 
    that passes through points P1 and P2.
    This is done using the projection of P13 onto P12 to find the point on
    P12 that is closes to the point P3, to finally use the euclidean distance
    formula to find the shortest distance between the point and the line.
    The three points P1, P2 and P3 are passed as a list and transformed to 
    np.arrays
    """
    P1 = np.array(P1)
    P2 = np.array(P2)
    P3 = np.array(P3)
    P12 = P2 - P1
    P13 = P3 - P1
    proj = np.dot(P13, P12)
    P12_norm = norm(P12)
    d_on_P12 = proj/(P12_norm**2)
    cp_on_P12 = P1 + d_on_P12 * P12
    distance = norm(cp_on_P12 - P3) 

    if verbose == True:
        print("\nShortest distance to line:", distance)

    return distance


def detect_line_collision(rob_coordinates, wall_corners, rob_radius):
    """
    This function will detect when the robot collides with a wall.
    It will receive the coordinates of the robot, two points which define
    the corners of a wall, and the radius of the robot.
    It will return the normal vector of the wall into which the robot will
    collide, and a boolean flag that indicates whether it will collide or
    not
    """
    rob_coordinates = np.array(rob_coordinates)
    wall_corners = np.array(wall_corners)

    Wall = wall_corners[1] - wall_corners[0]
    vec2corner1 = rob_coordinates - wall_corners[0]
    vec2corner2 = rob_coordinates - wall_corners[1]

    # Calculate the normalized perpendicular vector to the wall
    NormalVec2Wall = (Wall[1], -Wall[0])
    NormalizedVec2Wall = NormalVec2Wall / norm(Wall)

    # If the norm both vectors to each corner of a wall are smaller than the
    # norm of the vector that defines the wall, then the ball is capable of
    # colliding with the wall

    if ((norm(vec2corner1) <= norm(Wall) + rob_radius) and (norm(vec2corner2) <= norm(Wall) + rob_radius)):

        d = dist_point2line(wall_corners[0], wall_corners[1], rob_coordinates, verbose = False)

    else:
        
        d = np.min([norm(vec2corner1), norm(vec2corner2)])

    if d < rob_radius + 1:
        
        collision_detected = True

        # return [collision_detected, NormalizedVec2Wall]
        return [collision_detected, NormalizedVec2Wall, d]


    collision_detected = False
    NormalizedVec2Wall = (0,0)

    # return [collision_detected, NormalizedVec2Wall]
    return [collision_detected, NormalizedVec2Wall, d]

rec_col_counter = 0

def collision_scan(wall_corners, rob_coordinates, rob_radius, robot, verbose = False):
    """
    This function will iterate, at each frame, over all the corners that
    define the walls of the room and obstacles in order to check if a
    collision between the robot and a wall has ocurred.
    Wall_corners    is an array that contains the coordinates of every
                    corner in the room
    rob_coordinates is a tuple that contains the robot's position
    rob_radius      is a scalar defining the radius of the robot
    """
    collisions = []
    normalized_vectors = []
    distances = []
    global rec_col_counter
    for i in range(0, len(wall_corners)-1):
        collision_detected, NormalizedVec2Wall, d = detect_line_collision(rob_coordinates, (wall_corners[i], wall_corners[i+1]), rob_radius)
        collisions.append(collision_detected)
        normalized_vectors.append(NormalizedVec2Wall)
        distances.append(d)
        
    distances = np.array(distances)
    min_dist_index = np.argmin(distances)

    collision_detected = collisions[min_dist_index] 
    NormalizedVec2Wall = normalized_vectors[min_dist_index]
    
    if collision_detected:
        if verbose:
            print("Line segment collided:", min_dist_index, normalized_vectors[min_dist_index])
            if min_dist_index == 0:
                print(distances[min_dist_index:min_dist_index+2])
            else:
                print(distances[min_dist_index-1: min_dist_index+2])
            print(rob_coordinates, robot.x_vel, robot.y_vel, "\n")
        return [collision_detected, NormalizedVec2Wall]
    # To implement collision detection tolerance <-- if a collision is detected recently, then do not trigger collision_detected 
    else:
        rec_col_counter += 1
        if rec_col_counter > 1:
            robot.recent_collision = False
            counter = 0
    return [collision_detected, NormalizedVec2Wall]
        
RAND_ANGLE = 5

def robot_collision_handler(robot,NormalizedVec2Wall, rand_angle = False, verbose = False):
    """
    This function receives a robot object as an input, and is in charge of
    determining where the robot will go after colliding with a wall. The 
    new direction of the robot will be equal to the reflected vector of the
    old direction about the normal vector of the wall the robot collided with.
    The reflected vector is calculated as r = d - 2(dot_product(d, n)*n
    Where r is the reflected vector, d is the incident vector, and n is the 
    normalized normal vector.
    from: https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector
    """

    NormalizedVec2Wall = np.array(NormalizedVec2Wall)
    old_direction = np.array((robot.x_vel, robot.y_vel))
    new_direction = old_direction - 2*np.dot(old_direction, NormalizedVec2Wall)*NormalizedVec2Wall
    if verbose:
        print("New direction is: ", new_direction)

    if rand_angle:
        theta = np.arctan2(new_direction[1], new_direction[0])
        if verbose:
            print("Theta is: " + str(theta))
        if np.random.random() > 0.5:
            new_theta = theta + RAND_ANGLE*pi/180
        else:
            new_theta = theta - RAND_ANGLE*pi/180
        
        new_direction = [np.cos(new_theta), np.sin(new_theta)]
        if verbose:
            print("New direction with random angle change is: ", new_direction)
        # Multiply by the same factor that is used in rand_vel0 to get consistent velocities after collisions
        robot.x_vel = new_direction[0]*0.5
        robot.y_vel = new_direction[1]*0.5
        return


    robot.x_vel = new_direction[0]
    robot.y_vel = new_direction[1]
    robot.recent_collision = True

def cleaning_percentage(win, initial_red_pixels, verbose = False):
    green_pixels = 0
    imgdata = pygame.surfarray.array3d(win)
    imgdata = np.array(imgdata)
    green_pixels = np.count_nonzero(imgdata[30:743,54:640,:] == (69, 245, 99))
    clean_percentage = green_pixels/initial_red_pixels * 100
    if verbose:
        print("Total red pixels: " + str(initial_red_pixels))
        print("Total green pixels: " + str(green_pixels))
        print("Clean percentage: " + str(clean_percentage))

    return clean_percentage



    
    




# collision, normal_vec = collision_scan(WALL_CORNERS, (147,149), 10)


# # # collision, normal_vec = detect_line_collision((300,-300),((400,0),(400,800)), 30)

# print("")
# print("Collision: ", collision)
# print("")
# print("Collided wall normal vector:", normal_vec)