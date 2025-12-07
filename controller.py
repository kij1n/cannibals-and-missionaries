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

    def event_handler(self, button=None, action=None):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if self.action == "menu":
                        self.quit()
                    elif self.action == "pause":
                        self.resume()
                    else:
                        self.pause()

            if event.type == pygame.QUIT:
                self.running = False

            if (event.type == pygame.MOUSEBUTTONUP and
                    button is not None):
                # if event.button == 1:
                #     print(pygame.mouse.get_pos())

                if event.button == 1 and button == "menu_start":
                    self.play()
                elif event.button == 1 and button == "menu_rules":
                    self.rules()
                elif event.button == 1 and button == "menu_quit":
                    self.quit()
                elif event.button == 1 and button == "pause_resume":
                    self.resume()
                elif event.button == 1 and button == "pause_rules":
                    self.rules()
                elif event.button == 1 and button == "pause_quit":
                    self.quit()

    def play(self):
        self.action = "listen"

    def rules(self):
        self.action = "rules"

    def quit(self):
        self.running = False

    def resume(self):
        self.action = "listen"

    def pause(self):
        self.action = "pause"

    def input_handler(self):
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_ESCAPE]:
        #     if self.action == "menu":
        #         self.quit()
        #     elif self.action == "pause":
        #         print("pause")
        #         self.resume()
        #     else:
        #         self.pause()
        pass


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

            if self.action == "menu" or self.action == "pause":
                hovered_button = self.model.game_state.collisions.get_hovered_button(
                    self.model.menu_state,
                    pygame.mouse.get_pos(),
                    self.action
                )
                if hovered_button is not None:
                    self.model.menu_state.set_button_color(hovered_button, True)

                self.event_handler(hovered_button, self.action)
                self.input_handler()

            elif self.action == "rules":
                self.event_handler(None, self.action)
                self.input_handler()

            elif self.action == "listen":
                self.event_handler(None, self.action)
                self.input_handler()

            elif self.action == "ferry":
                self.event_handler(None, self.action)
                self.input_handler()

            # self.event_handler()
            # self.input_handler()
            self.fps.tick(settings.FRAMERATE)