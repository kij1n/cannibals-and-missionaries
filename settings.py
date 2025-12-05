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
ENTITY_SPRITE_SCALE = (80, 150)
BOAT_SPRITE_SCALE = (200, 100)
BACKGROUND_SPRITE_SCALE = SIZE

# button constants
BUTTON_HEIGHT = 75
BUTTON_WIDTH = 175
BUTTON_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (61, 61, 61)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_FONT_SIZE = 15
DIST_BETWEEN_BUTTONS = 10

PAUSE_BUTTON_START_POS_X = SIZE[0] / 2 - BUTTON_WIDTH / 2
PAUSE_BUTTON_START_POS_Y = SIZE[1] / 2 - BUTTON_HEIGHT
MENU_BUTTON_START_POS_X = SIZE[0] / 2 - BUTTON_WIDTH / 2
MENU_BUTTON_START_POS_Y = SIZE[1] / 2 - BUTTON_HEIGHT

# text controls
TEXT_COLOR = (255, 255, 255)  # white
FONT_SIZE = 50
FONT = "Poppins-Light.ttf"
