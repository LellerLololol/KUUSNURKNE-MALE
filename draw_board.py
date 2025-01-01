import tkinter
import random
from hexagons import *
import drag_and_drop

# layout_flat/layout_pointy; size; origin point
BOARD_LAYOUT = Layout(layout_flat, Point(45, 45), Point(500, 450))
BOARD_LENGTH = 5

# Shades for board (later on change to actually appealing static colors)
# Shades are stored as hex values
shade1 = "#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
shade2 = "#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
shade3 = "#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
shady_list = [shade1, shade2, shade3]

# Hexagons must reach 5 with q, r and s in all directions
# s = -q-r because of q + r + s = 0
# hexagons gets appended all valid x, y coordinates for the corresponding Hex
# hex_corners gets appended all valid q, r, s coordinates + the color
# More on the coordinate system: https://www.redblobgames.com/grids/hexagons/#coordinates-cube
hexagons = {}
hex_corners = []
for q in range(-BOARD_LENGTH, BOARD_LENGTH + 1):
    r1 = max(-BOARD_LENGTH, -q - BOARD_LENGTH)
    r2 = min(BOARD_LENGTH, -q + BOARD_LENGTH)
    for r in range(r1, r2 + 1):
        s = -q-r
        cur_hex = Hex(q, r, s)
        hexagons[cur_hex] = hex_to_pixel(BOARD_LAYOUT, cur_hex)
        hex_corners.append([polygon_corners(BOARD_LAYOUT, cur_hex), shady_list[(s - r) % 3]])

# Tkinter window
window = tkinter.Tk()

# Tkinter canvas
canvas = tkinter.Canvas(window, width=1000, height=900, bg='light gray')
canvas.pack()

# Load the images
# Image sizes 60x60 (?)
white_pawn_image = tkinter.PhotoImage(file="white_pawn.png")

# Stuff to draw on canvas
for hex in hex_corners:
    canvas.create_polygon(hex[0], fill=hex[1])
something = drag_and_drop.Example(window, canvas, BOARD_LAYOUT, BOARD_LENGTH)
white_pawn = something.create_image_token(300, 100, white_pawn_image)

window.mainloop()