from time import sleep


def valid_dimensions(dimensions):
    try:
        if dimensions['width'] and dimensions['height']:
            return True
    except IndexError:
        return False
    # sprite width in characters x number of columns <= pixels
    # how to determine which sprite? if a sprite can be in each column of a row,
    # we need to know how much **game** space each sprite takes up e.g. {'w': 1, 'l': 1} for a spike
    # and maybe {'w': 2, 'l': 1} for a really wide spike


class Screen:
    """
    Screen handles the actual process of outputting ASCII characters or codes to the terminal.
    Given an initial dimension of pixels to start
    Give it sprites and pixels
    """

    # How will it handle the difference between pixel positions and sprite positions?
    # Should screen determine for itself how many pixels to be?? Maybe it just gets rows and columns
    # Or should it be really low level and be handed exact pixel data and just deal with outputting it?

    HIDE_CURSOR_CODE = '\033[2J'
    INVERT_COLORS_CODE = '\033[7m'
    DEFAULT_PIXEL_WIDTH = 10
    DEFAULT_PIXEL_HEIGHT = 10
    DEFAULT_DIMENSIONS = {'width: '}

    def __init__(self, dimensions: dict[str: int], sprites, pixel_size):
        self.sprites = sprites
        self.timeout = False
        self.dimensions = dimensions
        self.pixel_size = pixel_size

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        if valid_dimensions(dimensions):
            self._dimensions = dimensions

    def clear_screen(self):
        print(self.HIDE_CURSOR_CODE)

    def render_to_screen(self, game_objects: dict[dict]) -> None:
        line_count = 0
        positions = [{}]
        line = ''

        for line in range(self.dimensions['height']):


        for game_object in game_objects:
            # get all the positions
            # figure out their sizes
            # start rendering the screen one line at a time

            # if their vertical position is this row, we have to render it
            pixels_on_this_line = game_object['sprite']
            #  add their horizontal position to the list
            if game_object['position']['y'] == line_count:
                positions.append(game_object['position']['x'])
            line = game_object['']

        self.render_line(line)

        print('rendering pixels')

    def render_line(self, line):
        pass

    def pixel_size(self):
        pass

    def build_blank_screen(self):
        width = self.dimensions['width'] * " " * self.pixel_size

    def paint_spikes(self):
        print(self.sprites.SPIKE)

    def convert_game_positions_to_pixel_positions(self):
        # ex: the game says okay there's a spike in the 2nd row 1st column => each spike is 2 parts, one on each line
        # so the 2nd row is really lines 3 and 4 of the screen
        # the top spike has to be one space farther right than the bottom
        pass

    def generate_line(self):
        pass
