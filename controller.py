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

    def handle_escape(self):
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

    def handle_click_menu(self, event, button, action):
        if event.button != 1:
            return

        if action == "menu":
            if button == "menu_start": self.play()
            elif button == "menu_rules": self.rules()
            elif button == "menu_quit": self.quit()
        elif action == "pause":
            if button == "pause_resume": self.resume()
            elif button == "pause_rules": self.rules()
            elif button == "pause_quit": self.quit()

    def handle_click_entity(self, event, hovered_entity):
        if event.button != 1:
            return

        if hovered_entity == "boat":
            carried_entities = len(self.model.game_state.entities.boat.held_entities)
            if carried_entities != 0:
                self.move_ferry()
        else:
            on_boat = self.model.game_state.entities.ents[hovered_entity].on_boat
            if on_boat:
                self.model.game_state.entities.remove_entity_from_boat(hovered_entity)
            else:
                self.model.game_state.entities.move_entity_to_boat(hovered_entity)

    def event_handler(self, button=None, hovered_entity=None, action=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE and not settings.LOST:
                    self.handle_escape()

            if (event.type == pygame.MOUSEBUTTONUP and
                    button is not None):
                self.handle_click_menu(event, button, action)

            if (event.type == pygame.MOUSEBUTTONUP and
                    button is None and
                    hovered_entity is not None and
                    self.action == "listen"):
                self.handle_click_entity(event, hovered_entity)


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

    def win(self):
        self.view.render_end("win", self.model.game_state.moves_made)
        pygame.time.delay(settings.GAME_END_DELAY)
        self.running = False

    def lose(self):
        settings.LOST = True
        if self.model.game_state.lose():
            self.view.render_end("lose", self.model.game_state.moves_made)
            pygame.time.delay(settings.GAME_END_DELAY)
            self.running = False

    def action_menu_pause(self):
        hovered_button = self.model.game_state.collisions.get_hovered_button(
            self.model.menu_state,
            pygame.mouse.get_pos(),
            self.action
        )
        if hovered_button is not None:
            self.model.menu_state.set_button_color(hovered_button, True)

        self.event_handler(hovered_button, None, self.action)

    def action_rules(self):
        self.event_handler(None, None, self.action)

    def action_listen(self):
        hovered_entity = self.model.game_state.collisions.get_hovered_entity(
            self.model.game_state,
            pygame.mouse.get_pos()
        )

        self.event_handler(None, hovered_entity)

    def action_ferry(self):
        arrived = self.model.game_state.entities.ferry()
        if arrived:
            self.model.game_state.moves_made += 1
            self.model.game_state.entities.stop_ferry()
            output = self.model.game_state.check_win_lose()
            if output == "pass":
                self.action = "listen"
            elif output == "win":
                self.action = "win"
            else:
                self.action = "lose"

    def action_win(self):
        self.win()

    def action_lose(self):
        self.lose()
        self.event_handler()


    def run(self):
        self.running = True
        self.action = "menu"

        while self.running:

            self.view.render(
                self.model.game_state,
                self.model.menu_state,
                self.action,
                self.model.game_state.moves_made
            )

            if self.action == "menu" or self.action == "pause":
                self.action_menu_pause()

            elif self.action == "rules":
                self.action_rules()

            elif self.action == "listen":
                self.action_listen()

            elif self.action == "ferry":
                self.action_ferry()

            elif self.action == "win":
                self.action_win()

            elif self.action == "lose":
                self.action_lose()

            self.fps.tick(settings.FRAMERATE)