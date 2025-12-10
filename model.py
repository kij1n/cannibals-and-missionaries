import pygame
import settings
from math import sin, cos, atan, atan2

class Model:
    def __init__(self):
        self.game_state = GameState()
        self.menu_state = MenuState()

class GameState:
    def __init__(self):
        self.collisions = CollisionManager()
        self.entities = EntityManager()
        self.gamestate = (3, 3, 0)
        self.game_graph = self.get_game_graph()
        self.moves_made = 0

    def lose(self):
        side = "left"

        cannibals, missionaries = self.get_ent_on_shore(side)

        if not self.were_rules_broken(cannibals, missionaries):
            side = "right"
            cannibals, missionaries = self.get_ent_on_shore(side)

        assigned_missionaries = []

        for cannibal_name in cannibals:
            cannibal = self.entities.ents[cannibal_name]

            if cannibal.missionary_to_eat is None:
                cannibal.assign_missionary_to_eat(missionaries, assigned_missionaries)
                assigned_missionaries.append(cannibal.missionary_to_eat)

                cannibal.sprite_name = ["CANNIBAL_MOUTH"]

                cannibal.pos = cannibal.get_position(self.entities.boat.get_position())
            if not self.collisions.check_collision(
                    cannibal,
                    self.entities.ents[cannibal.missionary_to_eat],
                    self.entities.boat.get_position()
            ):
                self.entities.move_to_missionary(cannibal)

        for cannibal_name in cannibals:
            cannibal = self.entities.ents[cannibal_name]
            if not self.collisions.check_collision(
                    cannibal,
                    self.entities.ents[cannibal.missionary_to_eat],
                    self.entities.boat.get_position()
            ):
                return False
        return True

    def get_ent_on_shore(self, side):
        cannibals = [ent.name for ent in self.entities.ents.values() if ent.type == "cannibal" and (ent.which_shore == side or (ent.on_boat and self.entities.boat.which_shore == side))]
        missionaries = [ent.name for ent in self.entities.ents.values() if ent.type == "missionary" and (ent.which_shore == side or (ent.on_boat and self.entities.boat.which_shore == side))]
        return cannibals, missionaries

    @staticmethod
    def were_rules_broken(cannibals, missionaries):
        return len(cannibals) > len(missionaries) > 0

    def check_win_lose(self):
        move = self.identify_move()
        if move in self.game_graph[self.gamestate].keys():
            self.append_gamestate(move)
            if self.gamestate == (0, 0, 1):
                return "win"
            else:
                return "pass"
        return "lose"

    def append_gamestate(self, move):
        self.gamestate = self.game_graph[self.gamestate][move]

    def identify_move(self):
        held_entities = self.entities.get_entities_on_boat()
        move = (0, 0)
        for ent_name in held_entities:
            if ent_name[0:-1] == "cannibal":
                move = (move[0]+1, move[1])
            else:
                move = (move[0], move[1]+1)
        return move

    def get_game_graph(self):
        max_missionaries = 3
        max_cannibals = 3
        gamestate = (max_cannibals, max_missionaries, 0) # cannibals on the left, missionaries on the left, boat: 0: left 1: right
        moves = [
            (1, 0), (2, 0), # cannibals
            (0, 1), (0, 2), # missionaries
            (1, 1)
        ]

        graph = {}
        for state in self.get_all_valid_states(max_missionaries, max_cannibals):
            graph[state] = self.get_next_gamestates(state, moves)

        return graph

    def get_next_gamestates(self, gamestate, moves):
        cannibals, missionaries, boat = gamestate
        direction = -1 if boat == 0 else 1
        next_states = {}
        for move in moves:
            next_state = (
                cannibals + move[0] * direction,
                missionaries + move[1] * direction,
                1-boat
            )
            if self.is_valid_gamestate(next_state):
                next_states[move] = next_state
        return next_states

    def get_all_valid_states(self, max_missionaries, max_cannibals):
        states = []
        for missionary in range(max_missionaries+1):
            for cannibal in range(max_cannibals+1):
                for boat in [0, 1]:
                    state = (cannibal, missionary, boat)
                    if self.is_valid_gamestate(state):
                        states.append(state)
        return states

    @staticmethod
    def is_valid_gamestate(gamestate):
        left_cannibals, left_missionaries, boat = gamestate
        if left_cannibals < 0 or left_missionaries < 0:
            return False

        right_cannibals = 3 - left_cannibals
        right_missionaries = 3 - left_missionaries
        if right_cannibals < 0 or right_missionaries < 0:
            return False

        # Check left shore
        if left_cannibals > left_missionaries > 0:
            return False
        if right_cannibals > right_missionaries > 0:
            return False

        return True


class CollisionManager:
    @staticmethod
    def check_collision(entity1, entity2, boat_pos=None):
        return entity1.get_hitbox(boat_pos).colliderect(entity2.get_hitbox(boat_pos))

    @staticmethod
    def get_hovered_button(menu_state, mouse_pos, action):
        for key, value in menu_state.buttons.items():
            if value.rect.collidepoint(mouse_pos) and action == "menu"\
                    and key in ["menu_start", "menu_rules", "menu_quit"]:
                return key
            elif value.rect.collidepoint(mouse_pos) and action == "pause"\
                    and key in ["pause_resume", "pause_quit", "pause_rules"]:
                return key
        return None

    @staticmethod
    def get_hovered_entity(game_state, mouse_pos):
        for entity in game_state.entities.get_all_entities():
            if entity.on_boat:
                boat_pos = game_state.entities.boat.get_position()
                rect = entity.get_hitbox(boat_pos)
            else:
                rect = entity.get_hitbox()
            if rect.collidepoint(mouse_pos):
                return entity.name
        if game_state.entities.boat.get_hitbox(None).collidepoint(mouse_pos):
            return "boat"

        return None


class EntityManager:
    def __init__(self):
        self.ents = {
            "cannibal1": self.add_entity("cannibal", "cannibal1", 0),
            "cannibal2": self.add_entity("cannibal", "cannibal2", 1),
            "cannibal3": self.add_entity("cannibal", "cannibal3", 2),
            "missionary1": self.add_entity("missionary", "missionary1", 3),
            "missionary2": self.add_entity("missionary", "missionary2", 4),
            "missionary3": self.add_entity("missionary", "missionary3", 5)
        }
        self.boat = Boat(settings.BOAT_LEFT_POS)
        self.ferry_moving = None

    def move_to_missionary(self, cannibal):
        if cannibal.movement is None:
            cannibal_pos = cannibal.get_position(self.boat.get_position())
            miss_pos = self.ents[cannibal.missionary_to_eat].get_position(self.boat.get_position())

            angle = atan2((miss_pos[1]-cannibal_pos[1]), (miss_pos[0]-cannibal_pos[0]))
            cannibal.movement = (
                cos(angle) * cannibal.step,
                sin(angle) * cannibal.step
            )

        cannibal.move(
            cannibal.movement
        )

    def is_ferry_done(self):
        return self.ferry_moving is None

    def start_ferry(self, side):
        self.ferry_moving = side

    def stop_ferry(self):
        self.boat.which_shore = self.ferry_moving
        self.ferry_moving = None


    def ferry(self):
        boat_pos = self.boat.get_position()
        if self.ferry_moving == "left":
            if boat_pos[0] >= settings.BOAT_LEFT_POS[0]:
                self.move_boat("left")
                return False
        else:
            if boat_pos[0] <= settings.BOAT_RIGHT_POS[0]:
                self.move_boat("right")
                return False
        # Arrived at the shore
        return True

    def move_boat(self, side):
        if side == "left":
            self.boat.pos = (
                self.boat.pos[0] - self.boat.speed,
                self.boat.pos[1]
            )
        else:
            self.boat.pos = (
                self.boat.pos[0] + self.boat.speed,
                self.boat.pos[1]
            )

    def set_hovering(self, ent_name):
        for name, obj in self.ents.items():
            if name == ent_name:
                obj.hovered_over = True
            else:
                obj.hovered_over = False

    def move_entity_to_boat(self, entity_name):
        held_entities = self.boat.held_entities
        if len(held_entities) == 2:
            return  # Boat is full
        if len(held_entities) == 1:
            other_index = self.ents[held_entities[0]].get_index_on_boat()
            self.boat.held_entities.append(entity_name)
            self.ents[entity_name].move_to_boat(1-other_index)

        if len(held_entities) == 0:
            self.boat.held_entities.append(entity_name)
            self.ents[entity_name].move_to_boat(0)

    def remove_entity_from_boat(self, entity_name):
        self.ents[entity_name].remove_from_boat(self.boat.which_shore)
        self.boat.held_entities.remove(entity_name)

    def get_entities_on_boat(self):
        return self.boat.held_entities

    def get_all_entities(self):
        items: list = list(self.ents.values())
        items.append(self.boat)
        return self.ents.values()

    @staticmethod
    def add_entity(type_of_entity, name, pos_index):
        entity = Entity(
            name,
            type_of_entity,
            settings.ENTITY_LEFT_POSITIONS[pos_index],
            settings.ENTITY_RIGHT_POSITIONS[pos_index]
        )
        return entity


class Boat:
    def __init__(self, pos):
        self.pos = pos
        self.held_entities = []
        self.which_shore = "left" # holds entity names on the boat
        self.speed = settings.BOAT_SPEED
        self.sprite_name = ["BOAT_1"]
        self.name = "boat"

    def get_entity_pos(self, index):
        return settings.BOAT_ENTITY_POS(self.pos, index)

    def get_held_entity_names(self):
        return self.held_entities

    def get_position(self):
        return self.pos

    def get_hitbox(self, boat_pos=None):
        rect = pygame.Rect(self.get_position(), settings.BOAT_SPRITE_SCALE)
        return rect


class Entity:
    def __init__(self, name, type_of_entity, left_shore_pos, right_shore_pos):
        self.index_boat_pos = None
        self.name = name
        self.type = type_of_entity

        self.sprite_name = []
        if type_of_entity == "cannibal":
            self.sprite_name = ["CANNIBAL"]
        elif type_of_entity == "missionary":
            self.sprite_name = ["MISSIONARY"]

        self.on_boat = False
        self.hovered_over = False

        self.which_shore = "left"
        self.left_shore_pos = left_shore_pos
        self.right_shore_pos = right_shore_pos
        self.pos = None
        self.movement = None

        self.step = 1
        self.missionary_to_eat = None

    def get_position(self, boat_pos=None):
        if self.pos is not None:
            return self.pos
        elif self.on_boat:
            return settings.BOAT_ENTITY_POS(boat_pos, self.index_boat_pos)
        elif self.which_shore == "left":
            return self.left_shore_pos
        elif self.which_shore == "right":
            return self.right_shore_pos
        else:
            return None

    def move_to_boat(self, index):
        self.which_shore = None
        self.on_boat = True
        self.index_boat_pos = index

    def remove_from_boat(self, shore):
        self.which_shore = shore
        self.on_boat = False
        self.index_boat_pos = None

    def get_index_on_boat(self):
        return self.index_boat_pos

    def get_hitbox(self, boat_pos=None):
        pos = self.get_position(boat_pos)

        if self.on_boat:
            sprite_size = settings.ENTITY_ON_BOAT_SCALE
        else:
            sprite_size = settings.ENTITY_SPRITE_SCALE

        hitbox_size = (sprite_size[0], sprite_size[1])
        hitbox_pos = pos

        rect = pygame.Rect(hitbox_pos, hitbox_size)
        rect.scale_by_ip(settings.HITBOX_SCALE)
        return rect

    def assign_missionary_to_eat(self, missionaries, missionaries_assigned):
        if self.missionary_to_eat is not None:
            return
        else:
            missionaries_to_assign = [m for m in missionaries if m not in missionaries_assigned]
            if len(missionaries_to_assign) > 0:
                self.missionary_to_eat = missionaries_to_assign[0]
            else:
                self.missionary_to_eat = missionaries[0]

    def move(self, movement):
        self.pos = (
            self.pos[0] + movement[0],
            self.pos[1] + movement[1]
        )


class MenuState:
    def __init__(self):
        self.buttons = {
            "pause_resume": self.create_button("Resume", True, 0),
            "pause_quit": self.create_button("Quit", True, 2),
            "pause_rules": self.create_button("Rules", True, 1),
            "menu_start": self.create_button("Start", False, 0),
            "menu_rules": self.create_button("Rules", False, 1),
            "menu_quit": self.create_button("Quit", False, 2),
        }

    def set_button_color(self, button_name, is_hover):
        for key, value in self.buttons.items():
            if key == button_name:
                value.set_hover_color(is_hover)
            else:
                value.set_hover_color(False)

    @staticmethod
    def create_button(text, is_pause, multiplier):
        distance = settings.BUTTON_HEIGHT + settings.DIST_BETWEEN_BUTTONS
        if not is_pause:
            start_pos = (
                settings.MENU_BUTTON_START_POS_X,
                settings.MENU_BUTTON_START_POS_Y +
                distance * multiplier
            )
        else:
            start_pos = (
                settings.PAUSE_BUTTON_START_POS_X,
                settings.PAUSE_BUTTON_START_POS_Y +
                distance * multiplier
            )
        return Button(
            start_pos,
            settings.BUTTON_WIDTH,
            settings.BUTTON_HEIGHT,
            settings.BUTTON_COLOR,
            settings.BUTTON_HOVER_COLOR,
            text,
            settings.BUTTON_TEXT_COLOR,
            settings.BUTTON_FONT_SIZE
        )


class Button:
    """
    Button class to represent a clickable button in the menu.
    Attributes:
        rect (Rect): The rectangle (object from pygame)
        representing the button.
        not_hover_color (tuple): The color of the button
        when not hovered over (R, G, B).
        hover_color (tuple): The color of the button
        when hovered over (R, G, B).
        text (str): The text displayed on the button.
        text_color (tuple): The color of the button text (R, G, B).
        font_size (int): The font size of the button text.
        color (tuple): The current color of the button (R, G, B).
    """

    def __init__(self, start_pos, width, height, not_hover_color,
                 hover_color, text, text_color, font_size):
        """
        Initialize the Button with position, size, colors, text, and font size.
        :param start_pos: Starting position of the button (x, y).
        :param width: Width of the button.
        :param height: Height of the button.
        :param not_hover_color: Color displayer when not hovered over.
        :param hover_color: Color displayed when hovered over.
        :param text: Text displayed on the button.
        :param text_color: Color of the displayed text.
        :param font_size: Font size of the displayed text.
        """
        self.rect = pygame.Rect(start_pos[0], start_pos[1], width, height)
        self.not_hover_color = not_hover_color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.color = not_hover_color

    def get_dimensions(self):
        """
        Get the dimensions of the button.
        :return: pygame Rect object representing button's dimensions.
        """
        return self.rect

    def get_center(self):
        """
        Get the center position of the button.
        :return: pygame Rect center variable (x, y).
        """
        return self.rect.center

    def set_hover_color(self, is_hover):
        """
        Set the button's color based on the hover state.
        :param is_hover: Boolean indicating whether the button is hovered over.
        :return: None
        """
        if is_hover:
            self.color = self.hover_color
        else:
            self.color = self.not_hover_color
