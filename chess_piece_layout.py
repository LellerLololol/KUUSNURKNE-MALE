from hexagons import hex_to_pixel, Hex, Layout
from tkinter import PhotoImage
from chess_piece_movement import Chessp
from drag_and_drop import Example


def create_chess_pieces(something: Example, BOARD_LAYOUT: Layout) -> list[Chessp]:
    """
    Creates and initializes chess pieces for a hexagonal chess board layout.
    Args:
        something (Example): An instance of drag_and_drop.example class.
        BOARD_LAYOUT (Layout): The layout of the hexagonal chess board.
    Returns:
        list[Chessp]: A list of initialized chess pieces.
    """
    list_of_chess_pieces = []

    # Load the images
    # Current sizes 32x32
    white_pawn_image = PhotoImage(file=r"assets\white_pawn.png")
    white_bishop_image = PhotoImage(file=r"assets\white_bishop.png")
    white_knight_image = PhotoImage(file=r"assets\white_knight.png")
    white_rook_image = PhotoImage(file=r"assets\white_rook.png")
    white_queen_image = PhotoImage(file=r"assets\white_queen.png")
    white_king_image = PhotoImage(file=r"assets\white_king.png")
    black_pawn_image = PhotoImage(file=r"assets\black_pawn.png")
    black_bishop_image = PhotoImage(file=r"assets\black_bishop.png")
    black_knight_image = PhotoImage(file=r"assets\black_knight.png")
    black_rook_image = PhotoImage(file=r"assets\black_rook.png")
    black_queen_image = PhotoImage(file=r"assets\black_queen.png")
    black_king_image = PhotoImage(file=r"assets\black_king.png")

    # Create dict of white piece positions and their images.
    white_piece_postions: dict[str, (PhotoImage, list[Hex])] = {}
    white_piece_postions["wp"] = (
        white_pawn_image,
        [
            Hex(0, 1, -1),
            Hex(1, 1, -2),
            Hex(2, 1, -3),
            Hex(3, 1, -4),
            Hex(4, 1, -5),
            Hex(5, 1, -6),
            Hex(-1, 2, -1),
            Hex(-2, 3, -1),
            Hex(-3, 4, -1),
            Hex(-4, 5, -1),
            Hex(-5, 6, -1),
        ],
    )
    white_piece_postions["b"] = (
        white_bishop_image,
        [Hex(0, 3, -3), Hex(0, 4, -4), Hex(0, 5, -5)],
    )
    white_piece_postions["n"] = (white_knight_image, [Hex(-2, 5, -3), Hex(2, 3, -5)])
    white_piece_postions["r"] = (white_rook_image, [Hex(-3, 6, -3), Hex(3, 3, -6)])
    white_piece_postions["q"] = (white_queen_image, [Hex(-1, 5, -4)])
    white_piece_postions["k"] = (white_king_image, [Hex(1, 4, -5)])

    # Create dict of black piece positions and their images.
    # Possible to just do the same but with Hex r,s values inverted but ehh DRY is overrated.
    black_piece_postions: dict[str, (PhotoImage, list[Hex])] = {}
    black_piece_postions["wp"] = (
        black_pawn_image,
        [
            Hex(0, -1, 1),
            Hex(-1, -1, 2),
            Hex(-2, -1, 3),
            Hex(-3, -1, 4),
            Hex(-4, -1, 5),
            Hex(-5, -1, 6),
            Hex(1, -2, 1),
            Hex(2, -3, 1),
            Hex(3, -4, 1),
            Hex(4, -5, 1),
            Hex(5, -6, 1),
        ],
    )
    black_piece_postions["b"] = (
        black_bishop_image,
        [Hex(0, -3, 3), Hex(0, -4, 4), Hex(0, -5, 5)],
    )
    black_piece_postions["n"] = (black_knight_image, [Hex(2, -5, 3), Hex(-2, -3, 5)])
    black_piece_postions["r"] = (black_rook_image, [Hex(3, -6, 3), Hex(-3, -3, 6)])
    black_piece_postions["q"] = (black_queen_image, [Hex(1, -5, 4)])
    black_piece_postions["k"] = (black_king_image, [Hex(-1, -4, 5)])

    for piece, (image, positions) in black_piece_postions.items():
        for position in positions:
            list_of_chess_pieces.append(
                Chessp(
                    piece,
                    "black",
                    something.create_image_token(
                        (hex_to_pixel(BOARD_LAYOUT, position)), image
                    ),
                    position,
                    True,
                )
            )
    for piece, (image, positions) in white_piece_postions.items():
        for position in positions:
            list_of_chess_pieces.append(
                Chessp(
                    piece,
                    "white",
                    something.create_image_token(
                        (hex_to_pixel(BOARD_LAYOUT, position)), image
                    ),
                    position,
                    True,
                )
            )
    return list_of_chess_pieces
