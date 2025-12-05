import pygame
from model import Model
from view import View
import settings


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.running = False
        self.action = "menu"

        self.fps = pygame.time.Clock()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def input_handler(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.action = "pause"


    def run(self):
        self.running = True
        self.action = "menu"

        while self.running:
            win = self.model.game_state.check_win_lose()

            self.view.render(
                self.model.game_state,
                self.model.menu_state,
                self.action,
                win
            )

            if self.action == "menu":
                pass
            elif self.action == "pause":
                pass
            elif self.action == "listen":
                pass
            elif self.action == "ferry":
                pass

            print("test")
            self.event_handler()
            self.fps.tick(settings.FRAMERATE)