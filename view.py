import pygame
import settings

class View:
    def __init__(self):
        pygame.init()
        self.main_view = MainView()
        self.menu_renderer = MenuRenderer()
        self.game_renderer = GameRenderer()
        self.sprite_loader = SpriteLoader()
        self.font = pygame.font.Font(settings.FONT, settings.FONT_SIZE)

class MainView:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            settings.SIZE
        )
        pygame.display.set_caption(settings.SCREEN_TITLE)

class MenuRenderer:
    pass

class GameRenderer:
    pass

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

        self.sprites["background"] = self.load_sprite(
            settings.BACKGROUND_PATH,
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
