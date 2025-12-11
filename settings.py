"""
This module contains all the settings and constants for the
cannibals and missionaries game.
"""

GAME_STARTED = False
LOST = False

SIZE = (1600, 900)
SCREEN_TITLE = "cannibals and missionaries"
FRAMERATE = 60
SCREEN_DIM = 100

# game end
GAME_WIN = "You won"
GAME_LOSE = "You lost"
GAME_END_FONT_SIZE = 100
GAME_END_FONT = "Poppins-Light.ttf"
GAME_END_DELAY = 3000  # milliseconds
GAME_END_POS = (SIZE[0] / 2, SIZE[1] / 2)

GAME_END_MOVES_MADE_POS = (GAME_END_POS[0], GAME_END_POS[1] + 100)
MOVES_MADE_POS = (100, 50)
MOVES_MADE_FONT_SIZE = 20

# sprites
BACKGROUND_PATH = {
    "BACKGROUND1": "images/background1.png"
}

BOAT_ASSET_PATHS = {
    "BOAT_1": "images/boat/boat_pos1.png"
}

ENTITY_ASSET_PATHS = {
    "CANNIBAL": "images/cannibal/cannibal_standing.png",
    "CANNIBAL_MOUTH": "images/cannibal/cannibal_mouth-open.png",
    "MISSIONARY": "images/missionary/missionary_standing.png"
}

# scaling for sprites
ENTITY_SPRITE_SCALE = (130, 200)
ENTITY_ON_BOAT_SCALE = (130, 130)
BOAT_SPRITE_SCALE = (200, 100)
BACKGROUND_SPRITE_SCALE = SIZE
HITBOX_SCALE = 0.7

# boat settings
BOAT_SPEED = 10
BOAT_MOVE_LEFT = (-30, 0)
BOAT_MOVE_RIGHT = (40, -30)
BOAT_LEFT_POS = (527 + BOAT_MOVE_LEFT[0], 444 + BOAT_MOVE_LEFT[1])
BOAT_RIGHT_POS = (850 + BOAT_MOVE_RIGHT[0], 444 + BOAT_MOVE_RIGHT[1])

# rendering entities in the boat
DIST_FROM_EDGE_OF_BOAT = 0
DIST_BETWEEN_ENTS_IN_BOAT = 0


# boat_entity_pos = lambda boat_pos, index: (
#     boat_pos[0] + DIST_FROM_EDGE_OF_BOAT + (ENTITY_SPRITE_SCALE[0] / 2 + DIST_BETWEEN_ENTS_IN_BOAT) * index,
#     boat_pos[1] - 80
# )

def boat_entity_pos(boat_pos, index):
    return (
        boat_pos[0] + DIST_FROM_EDGE_OF_BOAT + (ENTITY_SPRITE_SCALE[0] / 2 + DIST_BETWEEN_ENTS_IN_BOAT) * index,
        boat_pos[1] - 80
    )


# entity rendering constants
LEFT_MOVE = (-40, -100)
RIGHT_MOVE = (-50, -50)

ENTITY_LEFT_POSITIONS = [
    (24 + LEFT_MOVE[0], 401 + LEFT_MOVE[1]), (70 + LEFT_MOVE[0], 511 + LEFT_MOVE[1]),
    (188 + LEFT_MOVE[0], 406 + LEFT_MOVE[1]),
    (268 + LEFT_MOVE[0], 484 + LEFT_MOVE[1]), (330 + LEFT_MOVE[0], 403 + LEFT_MOVE[1]),
    (399 + LEFT_MOVE[0], 475 + LEFT_MOVE[1])
]
ENTITY_RIGHT_POSITIONS = [
    (1149 + RIGHT_MOVE[0], 388 + RIGHT_MOVE[1]), (1230 + RIGHT_MOVE[0], 468 + RIGHT_MOVE[1]),
    (1316 + RIGHT_MOVE[0], 388 + RIGHT_MOVE[1]),
    (1374 + RIGHT_MOVE[0], 484 + RIGHT_MOVE[1]), (1435 + RIGHT_MOVE[0], 377 + RIGHT_MOVE[1]),
    (1514 + RIGHT_MOVE[0], 483 + RIGHT_MOVE[1])
]

# rules
RULES = ["The task is to move all of them to right side of the river rules: ",
         "1. The boat can carry at most two people ",
         "2. If cannibals num greater than missionaries then the cannibals would eat the missionaries ",
         "3. The boat cannot cross the river by itself with no people on board"]
RULES_START_POS = (SIZE[0] / 2, SIZE[1] / 3)
RULES_FONT_SIZE = 30
RULES_FONT = "Poppins-Light.ttf"
RULES_TEXT_SPACING = 20
RULES_TEXT_HEIGHT = 10

# button constants
BUTTON_HEIGHT = 75
BUTTON_WIDTH = 175
BUTTON_COLOR = (58, 58, 59)
BUTTON_HOVER_COLOR = (61, 61, 61)
BUTTON_TEXT_COLOR = "white"
BUTTON_FONT = "Poppins-Light.ttf"
BUTTON_FONT_SIZE = 30
DIST_BETWEEN_BUTTONS = 10

PAUSE_BUTTON_START_POS_X = SIZE[0] / 2 - BUTTON_WIDTH / 2
PAUSE_BUTTON_START_POS_Y = SIZE[1] / 2 - BUTTON_HEIGHT
MENU_BUTTON_START_POS_X = SIZE[0] / 2 - BUTTON_WIDTH / 2
MENU_BUTTON_START_POS_Y = SIZE[1] / 2 - BUTTON_HEIGHT

# text controls
TEXT_COLOR = (255, 255, 255)  # white
FONT_SIZE = 50
FONT = "Poppins-Light.ttf"
