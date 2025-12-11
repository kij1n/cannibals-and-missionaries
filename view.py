"""
View component of the MVC architecture for the game.
Handles all rendering and visual presentation using Pygame.
"""

import pygame
import settings


class View:
    """
    Manages the visual presentation of the game using Pygame.
    It handles rendering of game states, menus, entities, and text.

    Attributes:
        screen (pygame.Surface): The main display surface.
        menu_renderer (MenuRenderer): Helper for rendering menu elements.
        game_renderer (GameRenderer): Helper for rendering game entities.
        sprite_loader (SpriteLoader): Manages loading and storage of sprites.
        font (pygame.font.Font): Default font for rendering text.
    """

    def __init__(self):
        """
        Initializes the Pygame environment, sets up the display window,
        and instantiates necessary renderers and asset loaders.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(
            settings.SIZE
        )
        pygame.display.set_caption(settings.SCREEN_TITLE)

        self.menu_renderer = MenuRenderer()
        self.game_renderer = GameRenderer()
        self.sprite_loader = SpriteLoader()
        self.font = pygame.font.Font(settings.FONT, settings.FONT_SIZE)

    def render(self, game_state, menu_state, action, moves_made):
        """
        Main rendering method called every frame.
        Delegates rendering to specific methods based on the current game action.
        :param game_state: GameState object containing game data.
        :param menu_state: MenuState object containing menu button data.
        :param action: String representing the current game action.
        :param moves_made: Integer counter for the number of moves made.
        :return: None
        """
        self.render_background()

        if action == "menu":
            self.render_menu(menu_state)

        elif action in ["listen", "ferry", "pause", "win", "lose"]:
            self.render_game_actions(game_state, menu_state, action, moves_made)

        elif action == "rules":
            self.render_rules()

        self.flip()

    def render_menu(self, menu_state):
        """
        Renders the main menu screen with a dimmed background.
        :param menu_state: MenuState object containing menu button data.
        :return: None
        """
        self.render_dim()
        self.menu_renderer.render_menu(
            menu_state,
            self.screen,
            pygame.font.Font(settings.BUTTON_FONT, settings.BUTTON_FONT_SIZE)
        )

    def render_game_actions(self, game_state, menu_state, action, moves_made):
        """
        Renders the active game state, including entities and UI elements.
        Handles rendering for 'listen', 'ferry', 'pause', 'win', and 'lose' actions.
        :param game_state: GameState object containing game data.
        :param menu_state: MenuState object containing menu button data.
        :param action: String representing the current game action.
        :param moves_made: Integer counter for the number of moves made.
        :return: None
        """
        self.game_renderer.render(game_state, self.screen, self.sprite_loader)
        if action == "pause":
            self.render_dim()
            self.menu_renderer.render_pause(
                menu_state,
                self.screen,
                pygame.font.Font(settings.BUTTON_FONT, settings.BUTTON_FONT_SIZE)
            )
        else:
            self.display_text(
                f"Moves: {moves_made}",
                settings.MOVES_MADE_POS,
                settings.TEXT_COLOR,
                settings.MOVES_MADE_FONT_SIZE,
                settings.FONT
            )

    def render_rules(self):
        """
        Renders the rules screen overlay.
        """
        self.render_dim()
        self.menu_renderer.render_rules(
            self.screen,
            settings.RULES_START_POS,
            settings.TEXT_COLOR,
            settings.RULES_FONT_SIZE,
            settings.RULES_FONT,
            settings.RULES_TEXT_HEIGHT,
            settings.RULES_TEXT_SPACING
        )

    def render_dim(self):
        """
        Draws a semi-transparent black overlay on the screen to dim the background.
        Used for menus and overlays.
        """
        dim_overlay = pygame.Surface(settings.SIZE)
        dim_overlay.fill("black")
        dim_overlay.set_alpha(settings.SCREEN_DIM)
        self.screen.blit(dim_overlay, (0, 0))

    def render_end(self, end: str, moves_made):
        """
        Renders the game over screen (win or lose) with the final move count.
        :param end: String representing the game end condition ("win" or "lose").
        :param moves_made: Integer counter for the number of moves made.
        :return: None
        """
        self.render_dim()

        text = None
        if end == "win":
            text = settings.GAME_WIN
        elif end == "lose":
            text = settings.GAME_LOSE

        self.display_text(
            text,
            settings.GAME_END_POS,
            settings.TEXT_COLOR,
            settings.GAME_END_FONT_SIZE,
            settings.GAME_END_FONT
        )
        text = f"Moves: {moves_made}"

        self.display_text(
            text,
            settings.GAME_END_MOVES_MADE_POS,
            settings.TEXT_COLOR,
            settings.MOVES_MADE_FONT_SIZE,
            settings.GAME_END_FONT
        )

        self.flip()

    def render_background(self):
        """
        Draws the static background image onto the screen.
        """
        self.screen.blit(
            self.sprite_loader.sprites["BACKGROUND1"],
            (0, 0)
        )

    @staticmethod
    def flip():
        """
        Flip the display with the pygame display flip method.
        :return: None
        """
        pygame.display.flip()

    def display_text(self, text, pos, color, size, font):
        """
        Renders and blits text onto the screen at a specified position.
        :param text: String of text to be displayed.
        :param pos: Tuple representing the (x, y) position for the text center.
        :param color: Color of the text.
        :param size: Size of the font.
        :param font: String representing the font file path.
        :return: None
        """
        py_font = pygame.font.Font(font, size)
        text_surface = py_font.render(text, True, color)
        text_box = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_box)


class MenuRenderer:
    """
    Handles the rendering of menu-related elements, such as buttons and rule text.
    """

    def render_menu(self, menu_state, screen, font: pygame.font.Font):
        """
        Renders the buttons for the main menu (Start, Rules, Quit).
        """
        self.show_button(menu_state.buttons["menu_start"], font, screen)
        self.show_button(menu_state.buttons["menu_rules"], font, screen)
        self.show_button(menu_state.buttons["menu_quit"], font, screen)

    def render_pause(self, menu_state, screen, font: pygame.font.Font):
        """
        Renders the buttons for the pause menu (Resume, Quit, Rules).
        """
        self.show_button(menu_state.buttons["pause_resume"], font, screen)
        self.show_button(menu_state.buttons["pause_quit"], font, screen)
        self.show_button(menu_state.buttons["pause_rules"], font, screen)

    @staticmethod
    def render_rules(screen, pos, color, size, font, text_height, text_spacing):
        """
        Renders the list of game rules on the screen.
        :param screen: Pygame screen object.
        :param pos: Tuple representing the (x, y) position for the text center.
        :param color: Color of the text.
        :param size: Size of the font.
        :param font: String representing the font file path.
        :param text_height: Height of each line of text.
        :param text_spacing: Spacing between lines of text.
        :return: None
        """
        py_font = pygame.font.Font(font, size)
        multiplier = 1
        for line in settings.RULES:
            text_surface = py_font.render(line, True, color)
            text_box = text_surface.get_rect(
                center=(pos[0], pos[1] + text_height * multiplier + text_spacing * multiplier))
            screen.blit(text_surface, text_box)
            multiplier += 1

    @staticmethod
    def show_button(btn, button_font, screen):
        """
        Draws a single button with its text onto the screen.
        :param btn: Button object representing the button to be rendered.
        :param button_font: Pygame font object used to render the button text.
        :param screen: Screen object on which to render the button.
        :return: None
        """
        pygame.draw.rect(screen, btn.color, btn.get_dimensions())

        text_surface = button_font.render(btn.text, False, btn.text_color)
        text_box = text_surface.get_rect()
        text_box.center = btn.get_center()
        screen.blit(text_surface, text_box)


class GameRenderer:
    """
    Handles the rendering of gameplay elements, including the boat and characters (entities).
    """

    def render(self, game_state, screen, sprite_loader):
        """
        Orchestrates the rendering of all game entities and the boat.
        :param game_state: GameState object containing game data.
        :param screen: Pygame screen object.
        :param sprite_loader: SpriteLoader object used to load and cache game assets.
        :return: None
        """
        self.render_entities(game_state, screen, sprite_loader)

        # render boat
        self.render_boat(game_state.entities.boat, screen, sprite_loader, game_state)

    def render_boat(self, boat, screen, sprite_loader, game_state):
        """
        Renders the boat and any entities currently on board.
        :param boat: Boat object representing the boat to be rendered.
        :param screen: Pygame screen object.
        :param sprite_loader: SpriteLoader object used to load and cache game assets.
        :param game_state: GameState object containing game data.
        :return: None
        """
        self.render_entity(
            game_state.entities.boat, screen, sprite_loader
        )
        entities_on_boat = boat.get_held_entity_names()
        for name in entities_on_boat:
            entity = game_state.entities.ents[name]
            self.render_entity(entity, screen, sprite_loader, True, entity.get_index_on_boat(), boat.get_position())

    def render_entities(self, game_state, screen, sprite_loader):
        """
        Renders all entities that are currently on the shores (not on the boat).
        :param game_state: GameState object containing game data.
        :param screen: Pygame screen object.
        :param sprite_loader: SpriteLoader object used to load and cache game assets.
        :return: None
        """
        for entity in game_state.entities.ents.values():
            if entity.on_boat:
                continue
            self.render_entity(entity, screen, sprite_loader)

    @staticmethod
    def render_entity(entity, screen, sprite_loader, on_boat=False, index=None, boat_pos=None):
        """
        Draws a single entity's sprite at its current position.
        Handles scaling differences for entities on the boat vs. on shore.
        :param entity: Entity object representing the entity to be rendered.
        :param screen: Pygame screen object.
        :param sprite_loader: SpriteLoader object used to load and cache game assets.
        :param on_boat: (optional) Boolean flag indicating whether the entity is on the boat.
        :param index: (optional) Integer representing the index of the entity on the boat.
        :param boat_pos: (optional) Tuple representing the position of the boat (x, y).
        :return:
        """
        image = sprite_loader.sprites[
            entity.sprite_name[0]
        ]
        if not on_boat:
            screen.blit(
                image,
                entity.get_position(),
            )
        else:
            if entity.missionary_to_eat is not None:
                rect = pygame.Rect((0, 0), settings.ENTITY_SPRITE_SCALE)
            else:
                rect = pygame.Rect((0, 0), settings.ENTITY_ON_BOAT_SCALE)
            screen.blit(
                image,
                entity.get_position(boat_pos),
                area=rect
            )

        # render hitboxes
        # if entity.name == "boat":
        #     color = "white"
        # else:
        #     color = "red"
        #
        # hitbox_rect = pygame.Rect(entity.get_hitbox(boat_pos))
        # pygame.draw.rect(screen, color, hitbox_rect)


class SpriteLoader:
    """
    Responsible for loading and caching game assets (sprites) from disk.
    """

    def __init__(self):
        self.sprites = {}
        for name in settings.ENTITY_ASSET_PATHS.keys():
            self.sprites[name] = self.load_sprite(
                settings.ENTITY_ASSET_PATHS[name],
                "entity"
            )

        for name in settings.BOAT_ASSET_PATHS.keys():
            self.sprites[name] = self.load_sprite(
                settings.BOAT_ASSET_PATHS[name],
                "boat"
            )

        for name in settings.BACKGROUND_PATH.keys():
            self.sprites[name] = self.load_sprite(
                settings.BACKGROUND_PATH[name],
                "background"
            )

    @staticmethod
    def load_sprite(path, sprite_type):
        """
        Loads an image from a file path, converts it for Pygame, and scales it according to its type.
        :param path: String of a file path to the image asset.
        :param sprite_type: String representing the type of sprite being loaded ("entity", "boat", or "background").
        :return: Pygame Surface object representing the loaded sprite.
        """
        image = pygame.image.load(path)
        image = image.convert_alpha()

        if sprite_type == "entity":
            image = pygame.transform.smoothscale(
                image,
                settings.ENTITY_SPRITE_SCALE
            )
        elif sprite_type == "boat":
            image = pygame.transform.smoothscale(
                image,
                settings.BOAT_SPRITE_SCALE
            )
        else:
            image = pygame.transform.smoothscale(
                image,
                settings.BACKGROUND_SPRITE_SCALE
            )

        return image
