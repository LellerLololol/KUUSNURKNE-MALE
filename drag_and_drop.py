import tkinter
import hexagons
import chess_piece_movement as cpm

class Example(tkinter.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, parent, cnvas, layout, bsize):
        tkinter.Frame.__init__(self, parent)

        # create a canvas
        self.canvas = cnvas
        self.canvas.pack(fill="both", expand=True)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None, 'previous': [0, 0], 'moves': [], 'object': ''}

        self.layout = layout
        self.bsize = bsize

        # List for the chess pieces (chess pices are loaded in draw_board.py)
        self.chess_pieces = []

        # Load the image
        self.move_image = tkinter.PhotoImage(file=r'assets\select.png')

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)

    def create_oval_token(self, x, y, color):
        """Create a token at the given coordinate in the given color"""
        self.canvas.create_oval(
            x - 25,
            y - 25,
            x + 25,
            y + 25,
            outline=color,
            fill=color,
            tags=("token",),
        )

    def create_image_token(self, xy, image):
        '''Create a token at the given coordinate with the given image'''
        self.canvas.create_image(
            xy[0],
            xy[1],
            image=image,
            tags=('token')
        )

    def create_temp_image(self, xy, image):
        '''Create an image with a different token'''
        self.canvas.create_image(
            xy[0],
            xy[1],
            image=image,
            tags=('remove')
        )

    def drag_start(self, event):
        """Begin drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_data['previous'] = self.canvas.coords(self._drag_data['item'])

        # Get the chess piece object
        start_coords = hexagons.pixel_to_hex(self.layout, hexagons.Point(self._drag_data['previous'][0], self._drag_data['previous'][1]))
        for obj in self.chess_pieces:
            if start_coords == obj.position:
                self._drag_data['moves'] = eval(f'obj.{obj.type}_move()')
                self._drag_data['object'] = obj
                for move in self._drag_data['moves']:  # Draws all possible spaces for a move
                    print(move)
                    self.create_temp_image(hexagons.hex_to_pixel(self.layout, move), self.move_image)
                break

    def drag_stop(self, event):
        """End drag of an object"""
        current_hex = hexagons.pixel_to_hex(self.layout, hexagons.Point(self._drag_data['x'], self._drag_data['y']))
        cur_coords = self.canvas.coords(self._drag_data['item'])
        inbounds = all(map(lambda x: -self.bsize <= x <= self.bsize, current_hex))
        
        '''
        # Find the object from the position; move?
        start_coords = hexagons.pixel_to_hex(self.layout, hexagons.Point(self._drag_data['previous'][0], self._drag_data['previous'][1]))
        for obj in self.chess_pieces:
            if start_coords == obj.position:
                cur_object = obj
                break
        '''
                           
        # Lock the object on a hexagon
        if inbounds and self.canvas.type(self._drag_data['item']) != 'polygon' and current_hex in self._drag_data['moves']:#eval(f'cur_object.{cur_type}_move()'):
            # object is in boundaries: lock it in the middle of hex
            # object also does a legal move
            # object itself is also not a hex
            lock_coords = hexagons.hex_to_pixel(self.layout, current_hex)
            self.canvas.move(self._drag_data['item'], 
                             lock_coords[0] - cur_coords[0],
                             lock_coords[1] - cur_coords[1])
            self._drag_data['object'].position = current_hex
            self._drag_data['object'].first_move = False
        else:
            # object is out of boundaries: move it back to the place it started
            self.canvas.move(self._drag_data['item'], 
                             self._drag_data['previous'][0] - cur_coords[0],
                             self._drag_data['previous'][1] - cur_coords[1])

        # Remove all move indicators
        self.canvas.delete('remove')

        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        self._drag_data['previous'] = [0, 0]
        self._drag_data['moves'] = []

    def drag(self, event):
        """Handle dragging of an object"""
        # check if the object is not polygon (board)
        if self.canvas.type(self._drag_data['item']) != 'polygon':
            # compute how much the mouse has moved
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            # move the object the appropriate amount
            self.canvas.move(self._drag_data["item"], delta_x, delta_y)
            # record the new position
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y