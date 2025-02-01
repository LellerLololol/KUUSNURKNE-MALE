#// fort format     j       j       if9oi   or  o+          jik     open    gh          uyi UnicodeDecodeErrorui        breakvf tgc pass    hasattr yh  UnboundLocalError   hasattrj    nonlocalln  ifhb    IOErrorp    ö   hjh globalv yvyi        hasattrhi   binl    nonlocalkl  finallytf   diriopo j   jljknlnk        hg  gyu defdrttrd   vhbvkn  breakkjbbk  j   
# Script will take care of the logic for the chess_bot move - return whatever the bot thinks is awesome to move

import random
import chess_piece_movement
import copy

def rando_move():
    """Evil combusate will take a move (0.001%) chek amte"""

    possible_moves = []
    taking_moves = {}
    score_system = {'bp': 10, 'b': 30, 'n': 30, 'r': 50, 'q': 90, 'k': 800}
    all_positions = map(lambda x: x.position, chess_piece_movement.Chessp.chess_pieces)
    for piece in chess_piece_movement.Chessp.chess_pieces:
        if piece.color == 'white':
            stlfm = piece.type  # something_to_look_for_moves
            for move in eval(f'chess_piece_movement.Chessp.{stlfm}_move(piece)')[0]:
                possible_moves.append([piece, move]) if move not in possible_moves else None
                if move in all_positions:
                    try:
                        taking_moves[score_system.get(stlfm)].append((piece, move))
                    except:
                        taking_moves[score_system.get(stlfm)] = [(piece, move)]

    if taking_moves != {}:
        all_cool_stuff = taking_moves.get(max(taking_moves.keys()))
        print(all_cool_stuff)
        print(random.choice(all_cool_stuff))
        return random.choice(all_cool_stuff) 
    elif possible_moves != []:
        return random.choice(possible_moves)
    else:
        raise Exception("No more pieces are on board - player won")
    
def evaluate_position(chess_pieces, bot_color):
    score_system = {'wp': 10, 'bp': 10, 'b': 30, 'n': 30, 'r': 50, 'q': 90, 'k': 800}
    score = 0
    for p in chess_pieces:
        val = score_system.get(p.type, 0)
        score += val if p.color == bot_color else -val
    return score

def generate_all_moves(chess_pieces, color):
    moves = []
    for piece in chess_pieces:
        if piece.color == color:
            for move in eval(f'chess_piece_movement.Chessp.{piece.type}_move(piece)')[0]:
                moves.append((piece, move))
    return moves

def move_piece(piece, new_position, chess_pieces):
    captured_piece = None
    # Check if there is a piece to capture
    for p in chess_pieces:
        if p.position == new_position and p.color != piece.color:
            captured_piece = p
            chess_pieces.remove(p)
            break
    # Update piece position
    piece.position = new_position
    return captured_piece

def undo_move(piece, old_position, captured_piece, chess_pieces):
    # Restore old position
    piece.position = old_position
    # Reinsert captured piece if needed
    if captured_piece:
        chess_pieces.append(captured_piece)

def minimax(chess_pieces, bot_color, depth, alpha, beta, is_maximizing):
    if depth == 0:
        return evaluate_position(chess_pieces, bot_color), None
    
    best_move = None
    not_bot_color = 'black' if bot_color == 'white' else 'white'
    if is_maximizing:
        max_eval = float('-inf')
        # Generate all possible moves for the maximizing side
        for piece, move in generate_all_moves(chess_pieces, bot_color):  # define generate_all_moves
            # Make hypothetical move
            old_position = piece.position
            captured = move_piece(piece, move, chess_pieces)  # define move_piece
            eval_val, _ = minimax(chess_pieces, bot_color, depth - 1, alpha, beta, False)
            # Undo move
            undo_move(piece, old_position, captured, chess_pieces)  # define undo_move
            
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = (piece, move)
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        # Generate all possible moves for the minimizing side
        for piece, move in generate_all_moves(chess_pieces, not_bot_color):
            old_position = piece.position
            captured = move_piece(piece, move, chess_pieces)
            eval_val, _ = minimax(chess_pieces, bot_color, depth - 1, alpha, beta, True)
            undo_move(piece, old_position, captured, chess_pieces)

            if eval_val < min_eval:
                min_eval = eval_val
                best_move = (piece, move)
            beta = min(beta, eval_val)
            if beta <= alpha:
                break
        return min_eval, best_move

def find_best_move(chess_pieces, bot_color):
    # Look 4 moves ahead
    chess_pieces = copy.deepcopy(chess_pieces)
    _, best = minimax(chess_pieces, bot_color, depth=2, alpha=float('-inf'), beta=float('inf'), is_maximizing=True)
    return best