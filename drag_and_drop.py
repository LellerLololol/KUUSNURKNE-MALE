import tkinter
import hexagons
import chess_piece_movement as cpm
import chess_bot


class ChessBoardInteraction(tkinter.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(
        self,
        parent,
        canvas: tkinter.Canvas,
        layout: hexagons.Layout,
        board_size: int,
        opponent_player: bool,
    ):
        tkinter.Frame.__init__(self, parent)

        # create a canvas
        self.canvas: tkinter.Canvas = canvas
        self.canvas.pack(fill="both", expand=True)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {
            "x": 0,
            "y": 0,
            "item": None,
            "previous": [0, 0],
            "moves": [],
            "object": "",
        }

        self.piece_sprites = {}

        self.layout: hexagons.Layout = layout
        self.board_size: int = board_size

        # List for the chess pieces (chess pices are loaded in draw_board.py)
        self.chess_pieces: list[cpm.Chessp] = []  #
        cpm.Chessp.chess_pieces = self.chess_pieces
        # self.obj_to_id = {} # TODO: Otsustada kas on vaja

        # Load the image
        self.move_image = tkinter.PhotoImage(file=r"assets/select.png")

        # Define the first colour to move
        self.color_to_move = "white"

        # Whether the opponent is a player or not
        self.opponent_player = opponent_player

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("piece", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.drag)

    def create_image_token(
        self, xy: hexagons.Hex, image: tkinter.PhotoImage, token: str
    ):
        """Create a token at the given coordinate with the given image"""
        self.canvas.create_image(xy[0], xy[1], image=image, tags=("piece", token))

    def create_temp_image(self, xy, image):
        """Create an image with a "remove" token"""
        self.canvas.create_image(xy[0], xy[1], image=image, tags=("remove"))

    def move_object(self, item, cur_coords, current_hex):
        lock_coords = hexagons.hex_to_pixel(self.layout, current_hex)
        self.canvas.move(
            item,
            lock_coords[0] - cur_coords[0],
            lock_coords[1] - cur_coords[1],
        )

    def take_piece(self, current_hex):
        takeable = [i for i in self.chess_pieces if i.position == current_hex]
        if takeable != []:
            self.canvas.delete(takeable[0].token)
            self.chess_pieces.remove(takeable[0])

    def drag_start(self, event):
        """Begin drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_data["previous"] = self.canvas.coords(self._drag_data["item"])

        # Get the chess piece object
        start_coords = hexagons.pixel_to_hex(
            self.layout,
            hexagons.Point(
                self._drag_data["previous"][0], self._drag_data["previous"][1]
            ),
        )
        for obj in self.chess_pieces:
            if (
                start_coords == obj.position
                and self.color_to_move == obj.color
                and (self.opponent_player or self.color_to_move == "black")
            ):
                self._drag_data["moves"], _ = eval(f"obj.{obj.type}_move()")
                self._drag_data["object"] = obj
                for move in self._drag_data[
                    "moves"
                ]:  # Draws all possible spaces for a move
                    self.create_temp_image(
                        hexagons.hex_to_pixel(self.layout, move), self.move_image
                    )
                break

    def drag_stop(self, event):
        """End drag of an object"""
        current_hex = hexagons.pixel_to_hex(
            self.layout, hexagons.Point(event.x, event.y)
        )
        cur_coords = self.canvas.coords(self._drag_data["item"])
        inbounds = all(
            map(lambda x: -self.board_size <= x <= self.board_size, current_hex)
        )

        # Lock the object on a hexagon
        if (
            inbounds
            and self.canvas.type(self._drag_data["item"]) != "polygon"
            and current_hex in self._drag_data["moves"]
            and self._drag_data["object"].color == self.color_to_move
            and (self.opponent_player or self.color_to_move == "black")
        ):
            # eval(f'cur_object.{cur_type}_move()'):
            # object is in boundaries: lock it in the middle of hex
            # object also does a legal move
            # object itself is also not a hex
            # gamemode is either pvp or it's black's turn

            self.move_object(self._drag_data["item"], cur_coords, current_hex)
            self.take_piece(current_hex)

            # Update moved chess piece data
            self._drag_data["object"].position = current_hex
            self._drag_data["object"].first_move = False

            # TODO: Add check for checkmate and stalemate here
            # Not working
            # print(can_target_king)
            enemy_can_move = self.check_if_enemy_can_move()
            # print(enemy_can_move)
            if not enemy_can_move:
                if self.current_side_can_attack_king():
                    ptext = "Checkmate"
                else:
                    ptext = "Stalemate"
                self.canvas.delete("piece")
                self.canvas.delete("board")
                self.canvas.create_text(
                    300, 320, text=ptext, font=("Comic Sans MS", 80)
                )
                self.chess_pieces = []

            # Check for pawn promotion
            if self.can_promote():
                self.promote_pawn_ui(self._drag_data["object"])

            # Cycle the color to move
            self.color_to_move = "black" if self.color_to_move == "white" else "white"

        else:
            # object is out of boundaries: move it back to the place it started
            self.canvas.move(
                self._drag_data["item"],
                self._drag_data["previous"][0] - cur_coords[0],
                self._drag_data["previous"][1] - cur_coords[1],
            )

        # Remove all move indicators
        self.canvas.delete("remove")

        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        self._drag_data["previous"] = [0, 0]
        self._drag_data["moves"] = []

        # Computer's turn
        if not self.opponent_player and self.color_to_move == "white":
            piece, move = chess_bot.find_best_move(self.chess_pieces)

            # move piece, update color
            self.move_object(
                piece.token, hexagons.hex_to_pixel(self.layout, piece.position), move
            )
            self.take_piece(move)
            if self.can_promote():
                self.promote_bot(piece)
            self.color_to_move = "black" if self.color_to_move == "white" else "white"

            # Update moved chess piece data
            piece.position = move
            piece.first_move = False

    def check_if_enemy_can_move(self) -> bool:
        """Check if the enemy can move"""
        can_move = False
        for obj in self.chess_pieces:
            if obj.color != self.color_to_move:
                moves, _ = eval(f"obj.{obj.type}_move()")
                if len(moves) != 0:
                    can_move = True
                    break
        return can_move

    def can_promote(self) -> bool:
        """Check if a pawn can be promoted"""
        if self._drag_data["object"].type == "wp":
            if (
                self._drag_data["object"].position[1] == -5
                or self._drag_data["object"].position[2] == 5
            ):
                return True
        elif self._drag_data["object"].type == "bp":
            if (
                self._drag_data["object"].position[1] == 5
                or self._drag_data["object"].position[2] == -5
            ):
                return True
        return False

    def current_side_can_attack_king(self) -> bool:
        """Check if the current side can attack the king"""
        can_target_king = False
        for obj in self.chess_pieces:
            if obj.color == self.color_to_move:
                _, can_target_king = eval(f"obj.{obj.type}_move()")
                if can_target_king:
                    break
        return can_target_king

    def drag(self, event):
        """Handle dragging of an object"""
        # check if the object is not polygon (board)
        if (
            self.canvas.type(self._drag_data["item"]) != "polygon"
            and self._drag_data["object"].color == self.color_to_move
        ):
            # compute how much the mouse has moved
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            # move the object the appropriate amount
            self.canvas.move(self._drag_data["item"], delta_x, delta_y)
            # record the new position
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

    def promote_bot(self, piece):
        """Promote a pawn for the bot to queen."""
        new_type = "q"
        position = piece.position
        color = piece.color
        token = piece.token
        self.take_piece(position)
        self.chess_pieces.append(
            cpm.Chessp(
                new_type,
                color,
                self.create_image_token(
                    (hexagons.hex_to_pixel(self.layout, position)),
                    self.piece_sprites[color][new_type],
                    token,
                ),
                position,
                True,
                token,
            )
        )

    def promote_pawn_ui(self, piece):
        import tkinter

        promotion_window = tkinter.Toplevel()
        promotion_window.title("Promote Pawn")
        label = tkinter.Label(
            promotion_window,
            text="Choose the piece to which you want to promote the pawn:",
            font=("Comic Sans MS", 12),
        )
        label.pack(pady=10)

        def promote(new_type):
            position = piece.position
            color = piece.color
            token = piece.token
            self.take_piece(position)
            self.chess_pieces.append(
                cpm.Chessp(
                    new_type[0],
                    color,
                    self.create_image_token(
                        (hexagons.hex_to_pixel(self.layout, position)),
                        self.piece_sprites[color][new_type[0]],
                        token,
                    ),
                    position,
                    True,
                    token,
                )
            )
            promotion_window.destroy()

        for new_type in ["queen", "rook", "bishop", "knight"]:
            btn = tkinter.Button(
                promotion_window,
                text=new_type.capitalize(),
                command=lambda nt=new_type: promote(nt),
            )
            btn.pack(anchor="w", padx=10, pady=5)
