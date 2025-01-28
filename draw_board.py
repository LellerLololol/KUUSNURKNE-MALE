import tkinter
import random
from hexagons import *
import drag_and_drop
import chess_piece_movement as cpm

# layout_flat/layout_pointy; size; origin point
BOARD_LAYOUT = Layout(layout_flat, Point(30, 30), Point(300, 320))
BOARD_LENGTH = 5

# Shades for board (later on change to actually appealing static colors)
# Shades are stored as hex values
shade1 = "#%02x%02x%02x" % (
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255),
)
shade2 = "#%02x%02x%02x" % (
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255),
)
shade3 = "#%02x%02x%02x" % (
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255),
)
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
        s = -q - r
        cur_hex = Hex(q, r, s)
        hexagons[cur_hex] = hex_to_pixel(BOARD_LAYOUT, cur_hex)
        hex_corners.append(
            [polygon_corners(BOARD_LAYOUT, cur_hex), shady_list[(s - r) % 3]]
        )

# Tkinter window
window = tkinter.Tk()

# Tkinter canvas
canvas = tkinter.Canvas(window, width=600, height=640, bg="light gray")
canvas.pack()


# Draw the chess board
for hex in hex_corners:
    canvas.create_polygon(hex[0], fill=hex[1])
something = drag_and_drop.Example(window, canvas, BOARD_LAYOUT, BOARD_LENGTH)

# region Chess piece loading
# Load the images
# Current sizes 32x32
# TODO: Filepath slashes for linux x windows gex
white_pawn_image = tkinter.PhotoImage(file=r"assets\white_pawn.png")
white_bishop_image = tkinter.PhotoImage(file=r"assets\white_bishop.png")
white_knight_image = tkinter.PhotoImage(file=r"assets\white_knight.png")
white_rook_image = tkinter.PhotoImage(file=r"assets\white_rook.png")
white_queen_image = tkinter.PhotoImage(file=r"assets\white_queen.png")
white_king_image = tkinter.PhotoImage(file=r"assets\white_king.png")
black_pawn_image = tkinter.PhotoImage(file=r"assets\black_pawn.png")
black_bishop_image = tkinter.PhotoImage(file=r"assets\black_bishop.png")
black_knight_image = tkinter.PhotoImage(file=r"assets\black_knight.png")
black_rook_image = tkinter.PhotoImage(file=r"assets\black_rook.png")
black_queen_image = tkinter.PhotoImage(file=r"assets\black_queen.png")
black_king_image = tkinter.PhotoImage(file=r"assets\black_king.png")

# Create dict of black piece positions and their images.
black_piece_postions: dict[str, (tkinter.PhotoImage, list[Hex])] = {}

black_piece_postions["bp"] = (
    black_pawn_image,
    [
        Hex(0, 1, -1),
        Hex(1, 1, -2),
        Hex(2, 1, -3),
        Hex(3, 1, -4),
        Hex(4, 1, -5),
        Hex(-1, 2, -1),
        Hex(-2, 3, -1),
        Hex(-3, 4, -1),
        Hex(-4, 5, -1),
    ],
)
black_piece_postions["bb"] = (
    black_bishop_image,
    [Hex(0, 3, -3), Hex(0, 4, -4), Hex(0, 5, -5)],
)
black_piece_postions["bn"] = (black_knight_image, [Hex(-2, 5, -3), Hex(2, 3, -5)])
black_piece_postions["br"] = (black_rook_image, [Hex(-3, 5, -2), Hex(3, 2, -5)])
black_piece_postions["bq"] = (black_queen_image, [Hex(-1, 5, -4)])
black_piece_postions["bk"] = (black_king_image, [Hex(1, 4, -5)])


# Create dict of white piece positions and their images.
# Possible to just do the same but with Hex r,s coords inverted but ehh DRY is overrated.
white_piece_postions: dict[str, (tkinter.PhotoImage, list[Hex])] = {}

white_piece_postions["wp"] = (
    white_pawn_image,
    [
        Hex(0, -1, 1),
        Hex(-1, -1, 2),
        Hex(-2, -1, 3),
        Hex(-3, -1, 4),
        Hex(-4, -1, 5),
        Hex(1, -2, 1),
        Hex(2, -3, 1),
        Hex(3, -4, 1),
        Hex(4, -5, 1),
    ],
)
white_piece_postions["wb"] = (
    white_bishop_image,
    [Hex(0, -3, 3), Hex(0, -4, 4), Hex(0, -5, 5)],
)
white_piece_postions["wn"] = (white_knight_image, [Hex(2, -5, 3), Hex(-2, -3, 5)])
white_piece_postions["wr"] = (white_rook_image, [Hex(3, -5, 2), Hex(-3, -2, 5)])
white_piece_postions["wq"] = (white_queen_image, [Hex(1, -5, 4)])
white_piece_postions["wk"] = (white_king_image, [Hex(-1, -4, 5)])

for piece, (image, positions) in black_piece_postions.items():
    for i, position in enumerate(positions):
        token = f"{piece}{i}"  # id to use as a token
        cpm.Chessp.chess_pieces.append(
            cpm.Chessp(
                piece,
                "black",
                something.create_image_token(
                    (hex_to_pixel(BOARD_LAYOUT, position)), image, token
                ),
                position,
                True,
                token,
            )
        )
for piece, (image, positions) in white_piece_postions.items():
    for i, position in enumerate(positions):
        token = f"{piece}{i}"  # id to use as a token
        cpm.Chessp.chess_pieces.append(
            cpm.Chessp(
                piece,
                "white",
                something.create_image_token(
                    (hex_to_pixel(BOARD_LAYOUT, position)), image, token
                ),
                position,
                True,
                token,
            )
        )

something.chess_pieces = cpm.Chessp.chess_pieces
# endregion


window.mainloop()
