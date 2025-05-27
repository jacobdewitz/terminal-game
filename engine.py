import time
from screen import Screen
from collections.abc import Iterator, Callable
import random


# ======================================================================================================================
# GAME OBJECT CLASSES
# ======================================================================================================================


class GameObject:

    def __init__(self, starting_position, sprite, in_game_dimensions):
        pass


class Player(GameObject):
    def __init__(self, starting_position, sprite, in_game_dimensions, movement_function):
        super().__init__(starting_position, sprite, in_game_dimensions)
        self.movement_function = movement_function

    def move(self, key_input: str):
        self.movement_function(key_input)


class Enemy(GameObject):
    pass


# ======================================================================================================================
# ENGINE CLASS
# ======================================================================================================================

# An engine needs to get keyboard inputs, count time, and calculate physics to determine the placement of pixels


class Engine:
    """
    The Engine to run a game.
    player_movement should be a callback function that accepts standardized keyboard inputs and returns an adjustment to
    the player position i.e.
    game_objects = {
    'spike': {
        'sprite': "|>",
        'in_game_dimensions': {'w': 1, 'l': 1},
        'starting_position': {'x': 2, 'y': 3},
        'per_tick_movement_callback': lambda _: {'y': -1},
        'check_collision_with_player': True
    },
    'bullet': {
        'sprite': "o",
        'in_game_dimensions': {'w': 1, 'l': 1},
        'starting_position': ???,
        'on_mount': lambda player_position: f
        'per_tick_movement_callback': lambda player_position: {'x': -1}, # How to do this where we give the player position to the callback so it knows where the shot comes from and direction it goes, but then after that it doesn't?
        'check_collision_with_player': True
    """

    # This is basically how the spikes will move
    # Another object might care about each tick
    # Or maybe the engine can also pass the player object location in the current tick
    # So the game can pass in some function to handle movement with those arguments as long as it returns a dict with
    # x and y to calculate the movement

    per_tick_movement = lambda _: {'y': -1}

    DEFAULT_REFRESH_RATE = 1 / 24  # seconds
    DEFAULT_SCREEN_DIMENSIONS = {'width': 100, 'length': 100}
    DEFAULT_KEY_BINDINGS = {
        'a': 'left',
        'd': 'right',
        'space': 'jump'
    }
    DEFAULT_GRID_ROWS = 3
    DEFAULT_GRID_COLUMNS = 3
    # Does the engine need this AND the game? Or just the game has a default

    # grid space gives the 2D structure of the occupiable space in indivisible units - like the squares on a chess board
    # each space can typically only be occupied by one object and no positioning partially between spaces is allowed
    DEFAULT_GRID_SPACE = [[0] * DEFAULT_GRID_COLUMNS for i in range(DEFAULT_GRID_ROWS)]
    DEFAULT_PLAYER_POSITION = {'x': 0, 'y': 0}

    @staticmethod
    def validate_data_shape(data):
        isinstance(data, list)
        pass

    @staticmethod
    def validate_in_bounds(grid: list[list], coordinates: dict[str: int]):
        try:
            if grid[coordinates.x][coordinates.y]:
                return True
        except IndexError:
            return False

    def __init__(self,
                 player_movement: Callable[[str], dict[str: int]],
                 refresh_rate=DEFAULT_REFRESH_RATE,
                 screen_settings=None,
                 # This could just go into the game objects
                 player_object=None,
                 player_start_position=None,
                 grid_space=None,
                 game_objects=None,
                 options=None,
                 player_grid=None,
                 object_grid=None,
                 key_bindings=None):

        self.game_objects = game_objects
        self.player_object = player_object

        # the subset of the full game grid the player/objects can move in
        # ex: [[1, 1, 1], [0, 0, 0]] - the player can only move anywhere in the first row, nowhere in the second row
        self.player_grid = player_grid
        self.object_grid = object_grid

        # Merge key bindings from argument with defaults, overwriting the defaults where they clash
        self.key_bindings = key_bindings
        self.refresh_rate = refresh_rate

        self.player_start_position = player_start_position

        self.grid_space = grid_space

        if game_objects is None:
            self.game_objects = []
        else:
            # TODO- make sure it is the right shape
            pass

        if options is None:
            self.options = {}
        else:
            # TODO- make sure it is the right shape
            pass

        if self.player_object['player_start_position'] is None:
            self.player_start_position = self.DEFAULT_PLAYER_POSITION
        else:
            self.validate_in_bounds(self.player_object['player_start_position'])
            # TODO- make sure it is the right shape
            pass

        if 'player_start_position' in options.keys():
            self.player_start_position = options['player_start_position']

        self.tick_count = 0
        self.player_movement_callback = player_movement
        self.instruction_set = []
        self.screen = screen_settings

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, settings):
        if 'dimensions' in settings.keys():
            self._screen = Screen(settings['dimensions'])
        else:
            self._screen = Screen(self.DEFAULT_SCREEN_DIMENSIONS)

    @property
    def grid_space(self):
        return self._grid_space

    @grid_space.setter
    def grid_space(self, grid):
        # Instantiate instance variables if none are passed to constructor
        if grid is None:
            self._grid_space = self.DEFAULT_GRID_SPACE
        else:
            # TODO- make sure it is the right shape
            if not self.validate_data_shape(grid): raise TypeError('need a standard grid')

            self._grid_space = grid

    @property
    def player_start_position(self):
        return self._player_start_position

    @player_start_position.setter
    def player_start_position(self, value):

        if self.player_object['player_start_position'] is None:
            self._player_start_position = self.DEFAULT_PLAYER_POSITION
        else:
            self.validate_in_bounds(self.player_object['player_start_position'])
            # TODO- make sure it is the right shape
            pass

        if 'player_start_position' in options.keys():
            self.player_start_position = options['player_start_position']

    @property
    def grid_space(self):
        return self._grid_space

    @property
    def player_object(self):
        return self._player_object

    @player_object.setter
    def player_object(self, value):
        if value is None:
            raise Exception('you need a player for a game, usually.')
        else:
            self._player_object = value

    @property
    def key_bindings(self):
        return self._key_bindings

    @key_bindings.setter
    def key_bindings(self, bindings):
        self._key_bindings = self.DEFAULT_KEY_BINDINGS.update(bindings)

    @property
    def game_objects(self):
        return self._game_objects

    @game_objects.setter
    def game_objects(self, value):
        if not value:
            self._game_objects = {}
        elif not isinstance(value, dict):
            self._game_objects = {}
        else:
            self._game_objects = value

    def instantiate_objects(self):
        for obj in self.game_objects:
            # track all objects on a basic grid to check for collisions and things
            self.object_grid[obj.starting_position.x][obj.starting_position.y] = 1
            # keep track of each individual object's position
            obj.current_position = obj.starting_position
        pass

    def instantiate_object(self, object):
        if callable(object['starting_position']):
            object['starting_position'](self.pla)

    def place_player(self):
        self.grid_space
        pass

    def initialize_game_grid(self):
        self.player_grid = self.grid_space.copy()
        self.place_player()
        self.instantiate_objects()

    def move_game_objects(self):
        for obj in self.game_objects:
            pass

    def move_player(self, input) -> None:
        # this should give a position adjustment that the engine can use to calculate the new player coordinates
        player_position_adjustment = self.player_movement_callback(input)

    def get_player_input(self):
        player_input = 'get_input'
        # Processing of the input
        return self.key_bindings[player_input]
        #
        pass

    def tick(self):

        time.sleep(self.DEFAULT_REFRESH_RATE)
        self.tick_count += 1

        # In here or in Screen?

    def valid_dimensions(self, dimensions):
        dimensions['width']

    def paint_screen(self):

        pass
        # get character position
        # get spike positions from grid
        # merge the two into one set of characters

    def next_frame(self):
        pass

    def paint_character(self):
        spacing = ' ' * self.COLUMN_SIZE * self.player_position_index
        print(f"#{spacing} ACSII art of player")

        # Have the SCREEN do this

    # TODO - make abstract
    def paint_spikes(self):
        new_spike_column_index = round((random.random() * self.NUMBER_OF_COLUMNS - 1))
        self.COLUMN_SIZE = 1
        self.update_spike_grid(new_spike_column_index)

        # Moves the spikes up 1 row toward the player at the top

    # TODO - make abstract
    def update_spike_grid(self, new_spike_index):

        # instantiate a new empty row at the bottom
        self.spike_grid[self.NUMBER_OF_ROWS - 1] = [0] * self.NUMBER_OF_COLUMNS
        # add the spike(s) to it
        self.spike_grid[-1][new_spike_index] = 1

        for index, array in enumerate(self.spike_grid):
            if index == 0:
                continue

            self.spike_grid[index - 1] = array  # row 2 moves to row 1, row 3 to 2, etc.

    # Have the ENGINE do this
    def check_collision(self):
        # we need to know what collisions to pay attention to
        # maybe include in game object?
        # is our player overlapping with a spike
        self.game_objects
        if self.spike_grid[0][self.player_position_index] == 1:
            self.game_over = True

    # TODO - make abstract
    def score(self):
        self.count *= 5

    # The main game loop
    def run(self):
        self.initialize_game_grid()

        while True:
            # Be always lsitening for input and then process it
            action = self.get_player_input()

            position_adjustment = self.move_player(action)

            self.screen.render()

            self.tick()

            # position in the game space grid i.e. 3,2 (row 4, column 3)
