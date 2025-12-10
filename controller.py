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
                if event.button == 1 and hovered_entity == "boat":
                    carried_entities = len(self.model.game_state.entities.boat.held_entities)
                    if carried_entities != 0:
                        self.move_ferry()
                elif event.button == 1:
                    on_boat = self.model.game_state.entities.ents[hovered_entity].on_boat
                    if on_boat:
                        self.model.game_state.entities.remove_entity_from_boat(hovered_entity)
                    else:
                        self.model.game_state.entities.move_entity_to_boat(hovered_entity)

    def play(self):
        self.action = "listen"
        settings.GAME_STARTED = True

    def rules(self):
        self.action = "rules"

    def quit(self):
        self.running = False

    def move_ferry(self):
        self.action = "ferry"
        side = self.model.game_state.entities.boat.which_shore
        if side == "left":
            side = "right"
        else:
            side = "left"
        self.model.game_state.entities.start_ferry(side)

    def resume(self):
        if not self.model.game_state.entities.is_ferry_done():
            self.action = "ferry"
        else:
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
                
                self.event_handler(None, hovered_entity)

            elif self.action == "ferry":
                arrived = self.model.game_state.entities.ferry()
                if arrived:
                    self.model.game_state.entities.stop_ferry()
                    output = self.model.game_state.check_win_lose()
                    if output == "pass":
                        self.action = "listen"
                    elif output == "win":
                        self.action = "win"
                    else:
                        self.action = "lose"

                self.event_handler(None, self.action)
            elif self.action == "win":
                pass
            elif self.action == "lose":
                pass

            self.fps.tick(settings.FRAMERATE)