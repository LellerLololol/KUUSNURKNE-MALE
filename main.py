# Script will create a window whether the opponent is a bot or a player

import tkinter
from draw_board import draw_board, load_pieces, BOARD_LAYOUT, BOARD_LENGTH
import drag_and_drop

def acitivate(white_starts):
    """whimsical board"""
    
    # Load dnd
    something = drag_and_drop.ChessBoardInteraction(window, canvas, BOARD_LAYOUT, BOARD_LENGTH, against_player, white_starts)
    something.piece_sprites["white"] = white_piece_sprites
    something.piece_sprites["black"] = black_piece_sprites

    draw_board(canvas)
    load_pieces(
        something, white_starts,
        white_pawn_image, white_bishop_image, white_knight_image, 
        white_rook_image, white_queen_image, white_king_image, 
        black_pawn_image, black_bishop_image, black_knight_image, 
        black_rook_image, black_queen_image, black_king_image
    )
    

def bow_buttons():
    global white_button
    global black_button

    white_button = tkinter.Button(window, text='Play as white', command=load_white)
    black_button = tkinter.Button(window, text='Play as black', command=load_black)

    white_button.place(x=50, y=50)
    black_button.place(x=50, y=100)

def load_pvp():
    global against_player

    against_player = True

    # Remove current buttons
    player_button.destroy()
    bot_button.destroy()

    bow_buttons()

def load_bot():
    global against_player

    against_player = False

    # Remove current buttons
    player_button.destroy()
    bot_button.destroy()

    bow_buttons()

def load_white():
    
    # Remove current buttons
    white_button.destroy()
    black_button.destroy()

    acitivate(True)

def load_black():

    # Remove current buttons
    white_button.destroy()
    black_button.destroy()

    acitivate(False)

# Tkinter window
window = tkinter.Tk()


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
black_piece_sprites: dict[str, tkinter.PhotoImage] = {
    "bp": black_pawn_image,
    "wp": black_pawn_image,
    "b": black_bishop_image,
    "n": black_knight_image,
    "r": black_rook_image,
    "q": black_queen_image,
    "k": black_king_image,
}
white_piece_sprites: dict[str, tkinter.PhotoImage] = {
    "wp": white_pawn_image,
    "bp": white_pawn_image,
    "b": white_bishop_image,
    "n": white_knight_image,
    "r": white_rook_image,
    "q": white_queen_image,
    "k": white_king_image,
}

# Tkinter canvas
canvas = tkinter.Canvas(window, width=600, height=640, bg="light gray")
canvas.pack()

# Load buttons
player_button = tkinter.Button(window, text='Play against yourself', command=load_pvp)
bot_button = tkinter.Button(window, text='Play against a bot', command=load_bot)

# Place buttons
player_button.place(x=50, y=50)
bot_button.place(x=50, y=100)

# endregion
window.mainloop()