import random

SIZE = (1600, 900)
SCREEN_TITLE = "cannibals and missionaries"
FRAMERATE = 60
SCREEN_DIM = 100

# game end
GAME_WIN = "You won"
GAME_LOSE = "You lost"
GAME_END_FONT_SIZE = 100
GAME_END_FONT = "Poppins-Bold.ttf"
GAME_END_DELAY = 3000  # milliseconds
GAME_END_POS = (SIZE[0] / 2, SIZE[1] / 2)

# sprites
BACKGROUND_PATH = {
    "BACKGROUND1": "images/background1.png",
    "BACKGROUND2": "images/background2.png",
    "BACKGROUND3": "images/background3.png",
    "BACKGROUND4": "images/background4.png"
}

BOAT_ASSET_PATHS = {
    "BOAT_1": "images/boat/boat_pos1.png",
    "BOAT_2": "images/boat/boat_pos2.png",
    "BOAT_3": "images/boat/boat_pos3.png",
    "BOAT_4": "images/boat/boat_pos4.png",
}

ENTITY_ASSET_PATHS = {
    "CANNIBAL": "images/cannibal/cannibal_standing.png",
    "CANNIBAL_MOUTH": "images/cannibal/cannibal_mouth-open.png",
    "CANNIBAL_TURN_LEFT_1": "images/cannibal/cannibal_turn_left_1.png",
    "CANNIBAL_TURN_LEFT_2": "images/cannibal/cannibal_turn_left_2.png",
    "CANNIBAL_TURN_RIGHT_1": "images/cannibal/cannibal_turn_right_1.png",
    "CANNIBAL_TURN_RIGHT_2": "images/cannibal/cannibal_turn_right_2.png",
    "MISSIONARY": "images/missionary/missionary_standing.png",
    "MISSIONARY_TURN_LEFT_1": "images/missionary/missionary_turn_left_1.png",
    "MISSIONARY_TURN_LEFT_2": "images/missionary/missionary_turn_left_2.png",
    "MISSIONARY_TURN_RIGHT_1": "images/missionary/missionary_turn_right_1.png",
    "MISSIONARY_TURN_RIGHT_2": "images/missionary/missionary_turn_right_2.png"
}

# scaling for sprites
ENTITY_SPRITE_SCALE = (130, 200)
BOAT_SPRITE_SCALE = (200, 100)
BACKGROUND_SPRITE_SCALE = SIZE

# entity positions
BOAT_DIST_FROM_EDGE = 20
# BOAT_LEFT_POS = (SIZE[0] / 2 - BOAT_SPRITE_SCALE[0] + BOAT_DIST_FROM_EDGE, SIZE[1] / 2 - BOAT_SPRITE_SCALE[1])
# BOAT_RIGHT_POS = (SIZE[0] / 2 + BOAT_SPRITE_SCALE[0] - BOAT_DIST_FROM_EDGE, SIZE[1] / 2 - BOAT_SPRITE_SCALE[1])

# boat settings
BOAT_SPEED = 10
BOAT_MOVE_LEFT = (-30, 0)
BOAT_MOVE_RIGHT = (0, 0)
BOAT_LEFT_POS = (527 + BOAT_MOVE_LEFT[0], 444 + BOAT_MOVE_LEFT[1])
BOAT_RIGHT_POS = (975 + BOAT_MOVE_RIGHT[0], 444 + BOAT_MOVE_RIGHT[1])

# entity rendering constants
LEFT_MOVE = (-40, -100)
RIGHT_MOVE = (0, 0)

ENTITY_LEFT_POSITIONS = [
    (24 + LEFT_MOVE[0], 401 + LEFT_MOVE[1]), (70  + LEFT_MOVE[0], 511 + LEFT_MOVE[1]), (188  + LEFT_MOVE[0], 406 + LEFT_MOVE[1]),
    (268  + LEFT_MOVE[0], 484 + LEFT_MOVE[1]), (330  + LEFT_MOVE[0], 403 + LEFT_MOVE[1]), (399  + LEFT_MOVE[0], 475 + LEFT_MOVE[1])
]
ENTITY_RIGHT_POSITIONS = [
    (1149 + RIGHT_MOVE[0], 388 + RIGHT_MOVE[1]), (1230 + RIGHT_MOVE[0], 468 + RIGHT_MOVE[1]), (1316 + RIGHT_MOVE[0], 388 + RIGHT_MOVE[1]),
    (1374 + RIGHT_MOVE[0], 484 + RIGHT_MOVE[1]), (1435 + RIGHT_MOVE[0], 377 + RIGHT_MOVE[1]), (1514 + RIGHT_MOVE[0], 483 + RIGHT_MOVE[1])
]

# rules
RULES = ["Lorem ipsum dolor sit amet, consectetur adipiscing ",
         "elit. In blandit at erat sed varius. Nunc dolor nunc, ",
         "posuere et massa et, venenatis pellentesque libero. ",
         "In hac habitasse platea dictumst. Curabitur id nisi ",
         "vitae augue accumsan ultrices. Morbi convallis velit ",
         "non nisi congue, eget ultricies massa molestie. Aliquam ",
         "convallis tellus risus, nec pellentesque ex tempor in. ",
         "Aenean ipsum metus, lobortis ac elementum nec, semper ",
         "eu magna. Nunc eu tellus ut nisl lacinia consequat ut ",
         "ac urna. Sed convallis vel sem id fermentum. Curabitur ",
         "fermentum maximus tortor sed sagittis. Donec at feugiat ",
         "nunc. Sed ut vulputate leo. Nunc quam diam, commodo at ",
         "ex non, tempor aliquam tortor."]
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
