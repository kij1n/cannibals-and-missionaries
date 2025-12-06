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


class EntityManager:
    def __init__(self):
        self.cannibals = {
            "cannibal1": self.add_entity("cannibal"),
            "cannibal2": self.add_entity("cannibal"),
            "cannibal3": self.add_entity("cannibal")
        }
        self.missionaries = {
            "missionary1": self.add_entity("missionary"),
            "missionary2": self.add_entity("missionary"),
            "missionary3": self.add_entity("missionary")
        }

    @staticmethod
    def add_entity(name):
        entity = Entity(
            name
        )
        return entity

class Entity:
    def __init__(self, name):
        self.name = name

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
