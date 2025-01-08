import tkinter
import random
from hexagons import *
import drag_and_drop
import chess_piece_movement as cpm

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
# Current sizes 60x60
white_pawn_image = tkinter.PhotoImage(file=r'assets\white_pawn.png')
white_bishop_image = tkinter.PhotoImage(file=r'assets\white_pawn.png')
white_knight_image = tkinter.PhotoImage(file=r'assets\white_knight.png')
white_rook_image = tkinter.PhotoImage(file=r'assets\white_rook.png')
white_queen_image = tkinter.PhotoImage(file=r'assets\white_queen.png')
white_king_image = tkinter.PhotoImage(file=r'assets\white_king.png')

# Draw the chess board
for hex in hex_corners:
    canvas.create_polygon(hex[0], fill=hex[1])
something = drag_and_drop.Example(window, canvas, BOARD_LAYOUT, BOARD_LENGTH)

# Load the chess pieces (this code will be optimized after all chess pieces will be loaded in the correct positions)
white_pawn = cpm.Chessp('p', something.create_image_token((hex_to_pixel(BOARD_LAYOUT, Hex(0, 0, 0))), white_pawn_image), Hex(0, 0, 0), True)
white_bishop = cpm.Chessp('b', something.create_image_token((hex_to_pixel(BOARD_LAYOUT, Hex(1, 0, -1))), white_bishop_image), Hex(1, 0, -1), True)
white_knight = cpm.Chessp('n', something.create_image_token((hex_to_pixel(BOARD_LAYOUT, Hex(2, -1, -1))), white_knight_image), Hex(2, -1, -1), True)
white_rook = cpm.Chessp('r', something.create_image_token((hex_to_pixel(BOARD_LAYOUT, Hex(-1, 1, 0))), white_rook_image), Hex(-1, 1, 0), True)
white_queen = cpm.Chessp('q', something.create_image_token((hex_to_pixel(BOARD_LAYOUT, Hex(-2, 1, 1))), white_queen_image), Hex(-2, 1, 1), True)
white_king = cpm.Chessp('k', something.create_image_token((hex_to_pixel(BOARD_LAYOUT, Hex(0, 3, -3))), white_king_image), Hex(0, 3, -3), True)

something.chess_pieces.append(white_pawn)
something.chess_pieces.append(white_bishop)
something.chess_pieces.append(white_knight)
something.chess_pieces.append(white_rook)
something.chess_pieces.append(white_queen)
something.chess_pieces.append(white_king)

window.mainloop()