# Script will create a window whether the opponent is a bot or a player

import tkinter
import draw_board
import drag_and_drop

def acitivate(seth_magic_man):
    """whimsical board"""
    
    draw_board.draw_board(canvas)
    draw_board.load_pieces(
        seth_magic_man,
        white_pawn_image, white_bishop_image, white_knight_image, 
        white_rook_image, white_queen_image, white_king_image, 
        black_pawn_image, black_bishop_image, black_knight_image, 
        black_rook_image, black_queen_image, black_king_image
    )

def load_pvp():
    
    # Load dnd
    something = drag_and_drop.Example(window, canvas, draw_board.BOARD_LAYOUT, draw_board.BOARD_LENGTH, True)
    
    # Load board
    acitivate(something)

    # Remove current buttons
    player_button.destroy()
    bot_button.destroy()

def load_bot():
    
    # Load dnd
    something = drag_and_drop.Example(window, canvas, draw_board.BOARD_LAYOUT, draw_board.BOARD_LENGTH, False)

    # Load board
    acitivate(something)

    # Remove current buttons
    player_button.destroy()
    bot_button.destroy()

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