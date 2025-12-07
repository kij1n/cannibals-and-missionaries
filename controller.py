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

    def event_handler(self, button=None, hovered_entity=None, action=None):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if self.action == "menu":
                        self.quit()
                    elif self.action == "pause":
                        self.resume()
                    elif self.action == "rules":
                        if settings.GAME_STARTED:
                            self.pause()
                        else:
                            self.action = "menu"
                    else:
                        self.pause()

            if event.type == pygame.QUIT:
                self.running = False

            if (event.type == pygame.MOUSEBUTTONUP and
                    button is not None):
                if event.button == 1 and button == "menu_start" and action == "menu":
                    self.play()
                elif event.button == 1 and button == "menu_rules" and action == "menu":
                    self.rules()
                elif event.button == 1 and button == "menu_quit" and action == "menu":
                    self.quit()
                elif event.button == 1 and button == "pause_resume" and action == "pause":
                    self.resume()
                elif event.button == 1 and button == "pause_rules" and action == "pause":
                    self.rules()
                elif event.button == 1 and button == "pause_quit" and action == "pause":
                    self.quit()

            if (event.type == pygame.MOUSEBUTTONUP and
                    button is None and
                    hovered_entity is not None and
                    self.action == "listen"):
                if hovered_entity == "boat":
                    pass
                elif event.button == 1:
                    self.model.game_state.entities.move_entity_to_boat(
                        hovered_entity
                    )

    def play(self):
        self.action = "listen"
        settings.GAME_STARTED = True

    def rules(self):
        self.action = "rules"

    def quit(self):
        self.running = False

    def resume(self):
        self.action = "listen"

    def pause(self):
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

            if self.action == "menu" or self.action == "pause":
                hovered_button = self.model.game_state.collisions.get_hovered_button(
                    self.model.menu_state,
                    pygame.mouse.get_pos(),
                    self.action
                )
                if hovered_button is not None:
                    self.model.menu_state.set_button_color(hovered_button, True)

                self.event_handler(hovered_button, None, self.action)

            elif self.action == "rules":
                self.event_handler(None, None, self.action)

            elif self.action == "listen":
                hovered_entity = self.model.game_state.collisions.get_hovered_entity(
                    self.model.game_state,
                    pygame.mouse.get_pos()
                )

                print(hovered_entity)
                
                self.event_handler(None, hovered_entity)

            elif self.action == "ferry":
                self.event_handler(None, self.action)


            self.fps.tick(settings.FRAMERATE)