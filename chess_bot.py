#// fort format     j       j       if9oi   or  o+          jik     open    gh          uyi UnicodeDecodeErrorui        breakvf tgc pass    hasattr yh  UnboundLocalError   hasattrj    nonlocalln  ifhb    IOErrorp    ö   hjh globalv yvyi        hasattrhi   binl    nonlocalkl  finallytf   diriopo j   jljknlnk        hg  gyu defdrttrd   vhbvkn  breakkjbbk  j   
# Script will take care of the logic for the chess_bot move - return whatever the bot thinks is awesome to move

import random
import chess_piece_movement

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