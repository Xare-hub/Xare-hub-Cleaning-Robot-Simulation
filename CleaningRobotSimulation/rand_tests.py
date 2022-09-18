import numpy as np

WALL_CORNERS = [(30, 185),
(30, 396),
(109, 396),
(109, 512),
(213, 639),
(520, 639),
(520, 577),
(724, 577),
(724, 474),
(680, 474),
(680, 345),
(722, 345),
(724, 63),
(626, 63),
(626, 157),
(534, 157),
(534, 353),
(280, 353),
(280, 157),
(184, 157),
(184, 63),
(108, 63),
(108, 185),
(30, 185)]

def draw(win, borders, lines):
    win.fill(BLACK)
    
    for border in borders:
        border.draw(win)

    for line in lines:
        line.draw(win)