import pygame
import settings

class View:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            settings.SIZE
        )
        pygame.display.set_caption(settings.SCREEN_TITLE)

        self.menu_renderer = MenuRenderer()
        self.game_renderer = GameRenderer()
        self.sprite_loader = SpriteLoader()
        self.font = pygame.font.Font(settings.FONT, settings.FONT_SIZE)

    def render(self, game_state, menu_state, action, end=None):
        self.render_background()

        if action == "menu":
            self.render_dim()
            self.menu_renderer.render_menu(
                menu_state,
                self.screen,
                pygame.font.Font(settings.BUTTON_FONT, settings.BUTTON_FONT_SIZE)
            )
        elif action == "listen" or action == "ferry" or action == "pause":
            self.game_renderer.render(game_state, self.screen, self.sprite_loader)
            if action == "pause":
                self.render_dim()
                self.screen = self.menu_renderer.render_pause(
                    menu_state,
                    self.screen,
                    pygame.font.Font(settings.BUTTON_FONT, settings.BUTTON_FONT_SIZE)
                )
        elif action == "rules":
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
        elif end is not None:
            self.render_end(end)

        self.flip()

    def render_dim(self):
        dim_overlay = pygame.Surface(settings.SIZE)
        dim_overlay.fill("black")
        dim_overlay.set_alpha(settings.SCREEN_DIM)
        self.screen.blit(dim_overlay, (0, 0))

    def render_end(self, end: str):
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

    def render_background(self):
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
        py_font = pygame.font.Font(font, size)
        text_surface = py_font.render(text, True, color)
        text_box = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_box)


class MenuRenderer:
    def render_menu(self, menu_state, screen, font: pygame.font.Font):
        screen = self.show_button(menu_state.buttons["menu_start"], font, screen)
        screen = self.show_button(menu_state.buttons["menu_rules"], font, screen)
        screen = self.show_button(menu_state.buttons["menu_quit"], font, screen)
        return screen

    def render_pause(self, menu_state, screen, font: pygame.font.Font):
        screen = self.show_button(menu_state.buttons["pause_resume"], font, screen)
        screen = self.show_button(menu_state.buttons["pause_quit"], font, screen)
        screen = self.show_button(menu_state.buttons["pause_rules"], font, screen)
        return screen

    @staticmethod
    def render_rules(screen, pos, color, size, font, text_height, text_spacing):
        py_font = pygame.font.Font(font, size)
        multiplier = 1
        for line in settings.RULES:
            text_surface = py_font.render(line, True, color)
            text_box = text_surface.get_rect(center=(pos[0], pos[1] + text_height*multiplier + text_spacing*multiplier))
            screen.blit(text_surface, text_box)
            multiplier += 1

        return screen

    @staticmethod
    def show_button(btn, button_font, screen):
        pygame.draw.rect(screen, btn.color, btn.get_dimensions())

        text_surface = button_font.render(btn.text, False, btn.text_color)
        text_box = text_surface.get_rect()
        text_box.center = btn.get_center()
        screen.blit(text_surface, text_box)
        return screen

class GameRenderer:
    def render(self, game_state, screen, sprite_loader):
        #render left side
        # self.render_side("left", game_state.left_side, screen, sprite_loader, game_state)
        self.render_entities(game_state, screen, sprite_loader)

        #render right side
        # self.render_side("right", game_state.right_side, screen, sprite_loader, game_state)

        #render boat
        self.render_boat(game_state.entities.boat, screen, sprite_loader, game_state)

    def render_boat(self, boat, screen, sprite_loader, game_state):
        self.render_entity(
            game_state.entities.boat, screen, sprite_loader
        )
        entities_on_boat = boat.get_held_entity_names()
        index = 0
        for name in entities_on_boat:
            entity = game_state.entities.ents[name]
            self.render_entity(entity, screen, sprite_loader, True, index, boat.get_position())
            index += 1

    def render_entities(self, game_state, screen, sprite_loader):
        for entity in game_state.entities.ents.values():
            if entity.on_boat:
                continue
            self.render_entity(entity, screen, sprite_loader)


    @staticmethod
    def render_entity(entity, screen, sprite_loader, on_boat=False, index=None, boat_pos=None):
        image = sprite_loader.sprites[
            entity.sprite_name[0]
        ]
        if not on_boat:
            screen.blit(
                image,
                entity.get_position()
            )
        else:
            screen.blit(
                image,
                settings.BOAT_ENTITY_POS(boat_pos, index)
            )

class SpriteLoader:
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
