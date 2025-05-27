import random
from engine import Engine
from sprites import sprites


# ======================================================================================================================
# Helpers + Constants
# ======================================================================================================================


def move_player(direction):
    match direction:
        case 'left':
            # move 1 unit left in the x direction
            return {'x': -1}
        case 'right':
            # move 1 unit right in the x direction
            return {'x': 1}
        case _:
            return {'x': 0}


mappings = {
    'spike': 'dsfadfgsdfg',
    'player': 'dfgsdfgds'
}

game_sprites = sprites

# ======================================================================================================================
# Game Objects
# ======================================================================================================================

SPIKE = {'spike': {
    'sprite': sprites['SPIKE'],
    'in_game_dimensions': {'w': 1, 'l': 1},
    'starting_position': {'x': 2, 'y': 3},
    'per_tick_movement_callback': lambda _: {'y': -1},
    'check_collision_with_player': True}
}

# ======================================================================================================================
# Player Object
# ======================================================================================================================

PLAYER = {
    'player': {
        'sprite': sprites['PLAYER'],
        'in_game_dimensions': {'w': 1, 'l': 1},
        'starting_position': {'x': 2, 'y': 0},
        'per_tick_movement_callback': move_player,
    }
}


# ======================================================================================================================
# Game Class
# ======================================================================================================================


class Game:
    """
    The Game object will spell out the particulars of the game (its features, the player movement system, refresh rate,
    etc.). It will hand most these off to the Engine object for calculation of everything's position in each frame which
    then is passed off to the Screen object to render it all on each tick."""

    DEFAULT_START_POSITION = {'x': 0}
    PIXEL_SIZE = 10
    NUMBER_OF_COLUMNS = 5
    NUMBER_OF_ROWS = 5
    REFRESH_RATE = 500 * 1.0 / 1000  # 500 milliseconds
    KEY_BINDINGS = {
        'left': 'left',
        'right': 'right'

    }

    # Instance variables ===============================================

    def __init__(self, sprites, player_movement, mappings):
        self.game_over = False
        self.options = {
            'player_start_position': self.DEFAULT_START_POSITION
        }
        self.player_position_index = 0
        self.spike_grid = [[0] * self.NUMBER_OF_COLUMNS for _ in range(self.NUMBER_OF_ROWS)]  # ex: [[0,0,0],[0,0,0]]
        self.count = 0
        self.engine = Engine(player_movement=move_player, key_bindings=self.KEY_BINDINGS)

    def play(self):
        self.engine.run()


# ======================================================================================================================
# Spike Game Subclass
# ======================================================================================================================

class SpikeGame(Game):
    DEFAULT_START_POSITION = {'x': 3}
    NUMBER_OF_COLUMNS = 3
    NUMBER_OF_ROWS = 6
    KEY_BINDINGS = Game.KEY_BINDINGS.update({
        'a': 'left',
        'd': 'right'
    })

    MOVES = {
        'dash_jump': {'x': 2, 'y': 4}
    }

    SPIKE_DELAY_AT_START = 10  # seconds

    def __init__(self, sprites, player_movement):
        super().__init__(sprites=sprites, player_movement=player_movement)


# ======================================================================================================================
# Running the code
# ======================================================================================================================

def main():
    spike_game = SpikeGame(sprites=sprites, player_movement=move_player)
    spike_game.play()


if __name__ == "__main__":
    main()
