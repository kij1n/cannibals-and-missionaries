import pygame
import settings

class Model:
    def __init__(self):
        self.game_state = GameState()
        self.menu_state = MenuState()


class GameState:
    def __init__(self):
        self.collisions = CollisionManager()
        self.entities = EntityManager()
        self.left_side = [
            "cannibal1", "cannibal2", "cannibal3",
            "missionary1", "missionary2", "missionary3"
        ] # holds missionaries and cannibals on the left side
        self.right_side = []

    def check_win_lose(self):
        return None


class CollisionManager:
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

    def get_hovered_entity(self, game_state, mouse_pos, sprite_loader):
        # check left side positions
        find = self.check_for_hover(
            game_state.left_side, game_state.entities,
            settings.ENTITY_LEFT_POSITIONS,
            mouse_pos, sprite_loader
            )
        if find is not None:
            return find

        # check right side positions
        find = self.check_for_hover(
            game_state.right_side, game_state.entities,
            settings.ENTITY_RIGHT_POSITIONS,
            mouse_pos, sprite_loader
        )
        if find is not None:
            return find

        # check entities currently on the boat
        boat_pos = game_state.entities.boat.pos
        for name, ent in game_state.entities.ents.items():
            if ent.on_boat:
                image = sprite_loader.sprites[ent.sprite_name[0]]
                rect = image.get_rect(topleft=boat_pos)
                rect.scale_by_ip(settings.HITBOX_SCALE)
                if rect.collidepoint(mouse_pos):
                    return name

        return None

    @staticmethod
    def check_for_hover(side, entities, positions, mouse_pos, sprite_loader):
        for i, name in enumerate(side):
            image = sprite_loader.sprites[entities.ents[name].sprite_name[0]]
            rect = image.get_rect(topleft=positions[i])
            rect.scale_by_ip(settings.HITBOX_SCALE)
            if rect.collidepoint(mouse_pos):
                return name
        return None

class EntityManager:
    def __init__(self):
        self.ents = {
            "cannibal1": self.add_entity("cannibal", "cannibal1"),
            "cannibal2": self.add_entity("cannibal", "cannibal2"),
            "cannibal3": self.add_entity("cannibal", "cannibal3"),
            "missionary1": self.add_entity("missionary", "missionary1"),
            "missionary2": self.add_entity("missionary", "missionary2"),
            "missionary3": self.add_entity("missionary", "missionary3")
        }
        self.boat = Boat(settings.BOAT_LEFT_POS)

    def set_hovering(self, ent_name):
        for name, obj in self.ents.items():
            if name == ent_name:
                obj.hovered_over = True
            else:
                obj.hovered_over = False

    def get_hitbox(self, ent_name, sprite_loader):
        return sprite_loader.sprites[self.ents[ent_name].sprite_name[0]].get_rect()

    def move_entity_to_boat(self, entity_name):
        self.boat.held_entities.append(entity_name)
        self.ents[entity_name].on_boat = True

    def move_boat(self):
        pass

    def remove_entity_from_boat(self, entity_name):
        self.boat.held_entities.remove(entity_name)
        self.ents[entity_name].on_boat = False

    @staticmethod
    def add_entity(type_of_entity, name):
        pos = None
        if type_of_entity == "boat":
            pos = settings.BOAT_LEFT_POS

        entity = Entity(
            name,
            type_of_entity,
            False,
            pos
        )
        return entity


class Boat:
    def __init__(self, pos):
        self.pos = pos
        self.held_entities = []
        self.which_shore = "left" # holds entity names on the boat
        self.speed = settings.BOAT_SPEED
        self.sprite_name = ["BOAT_1"]


class Entity:
    def __init__(self, name, type_of_entity, on_boat, pos=None):
        self.name = name
        self.type = type_of_entity
        self.pos = pos
        self.sprite_name = []
        self.on_boat = on_boat
        self.hovered_over = False
        if type_of_entity == "cannibal":
            self.sprite_name = ["CANNIBAL"]
        elif type_of_entity == "missionary":
            self.sprite_name = ["MISSIONARY"]


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
