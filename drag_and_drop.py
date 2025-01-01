import tkinter
import hexagons

class Example(tkinter.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, parent, cnvas, layout, bsize):
        tkinter.Frame.__init__(self, parent)

        # create a canvas
        self.canvas = cnvas
        self.canvas.pack(fill="both", expand=True)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None, 'previous': [0, 0]}

        self.layout = layout
        self.bsize = bsize

        # create a couple of movable objects
        #self.create_image_token(300, 100, self.image)

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

    def create_image_token(self, x, y, image):
        '''Create a token at the given coordinate with the given image'''
        self.canvas.create_image(
            x,
            y,
            image=image,
            tags=('token')
        )

    def drag_start(self, event):
        """Begin drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_data['previous'] = self.canvas.coords(self._drag_data['item'])

    def drag_stop(self, event):
        """End drag of an object"""
        # Lock the object on a hexagon
        current_hex = hexagons.pixel_to_hex(self.layout, hexagons.Point(self._drag_data['x'], self._drag_data['y']))
        cur_coords = self.canvas.coords(self._drag_data['item'])
        if -self.bsize <= current_hex.q <= self.bsize and -self.bsize <= current_hex.r <= self.bsize and -self.bsize <= current_hex.s <= self.bsize and self.canvas.type(self._drag_data['item']) != 'polygon':
            # object is in boundaries: lock it in the middle of hex
            # object itself is also not a hex
            lock_coords = hexagons.hex_to_pixel(self.layout, current_hex)
            self.canvas.move(self._drag_data['item'], 
                             lock_coords[0] - cur_coords[0],
                             lock_coords[1] - cur_coords[1])
        else:
            # object is out of boundaries: move it back to the place it started
            self.canvas.move(self._drag_data['item'], 
                             self._drag_data['previous'][0] - cur_coords[0],
                             self._drag_data['previous'][1] - cur_coords[1])

        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        self._drag_data['previous'] = [0, 0]

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