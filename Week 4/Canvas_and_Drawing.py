# first example of drawing on the canvas

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# define draw handler
def draw(canvas):
    canvas.draw_circle([100, 100], 50, 2, "Red", "Pink")
    canvas.draw_circle([300, 300], 50, 2, "Red", "Pink")
    canvas.draw_line([100, 100],[300, 300], 2, "Black")
    canvas.draw_circle([100, 300], 50, 2, "Green", "Lime")
    canvas.draw_circle([300, 100], 50, 2, "Green", "Lime")
    canvas.draw_line([100, 300],[300, 100], 2, "Black")
    canvas.draw_polygon([[150, 150], [250, 150], [250, 250], [150, 250]], 2, 
          "Blue", "Aqua")
    canvas.draw_text("An example of drawing", [60, 385], 24, "Black")

# create frame
frame = simplegui.create_frame("Text drawing", 400, 400)

# register draw handler    
frame.set_draw_handler(draw)
frame.set_canvas_background("Yellow")

# start frame
frame.start()