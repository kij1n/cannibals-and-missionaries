import pygame
from model import Model
from view import View
import settings


class Controller:
    """
    The main controller for the application. It manages the game loop, handles
    user input, and coordinates updates between the Model and View.

    Attributes:
        model (Model): The game logic model.
        view (View): The game view for rendering.
        running (bool): Flag to keep the game loop running.
        action (str): The current state of the game (e.g., "menu", "listen", "ferry").
        fps (pygame.time.Clock): Clock object to control the frame rate.
    """
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.running = False
        self.action = "menu"

        self.fps = pygame.time.Clock()

    def handle_escape(self):
        """
        Handles the logic when the ESC key is pressed.
        Depending on the current action (menu, pause, rules), it toggles the game state
        between pause, menu, and resume.
        :return: None
        """
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
        """
        Handles mouse click events when in the menu or pause screen.
        Checks which button was clicked and triggers the corresponding action.

        :param event: Pygame mouse event.
        :param button: String representing the name of the button clicked.
        :param action: String representing the current game action ("menu" or "pause").
        :return: None
        """
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
        """
        Handles mouse click events during gameplay (listen state).
        Manages logic for clicking on the boat (to move it) or entities (to load/unload).
        :param event: Pygame mouse event.
        :param hovered_entity: String representing the name of the entity hovered over.
        :return: None
        """
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
        """
        Processes the queue of pygame events.
        Delegates specific events (quit, keyup, mousebuttonup) to specialized handlers.
        :param button: String representing the name of the button clicked, if any.
        :param hovered_entity: String representing the name of the entity hovered over, if any.
        :param action: String representing the current game action ("menu", "pause", or "listen").
        :return: None
        """
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
        """
        Starts the game by setting the action to 'listen' and marking the game as started.
        """
        self.action = "listen"
        settings.GAME_STARTED = True

    def rules(self):
        """
        Switches the current action to 'rules' to display the rules screen.
        """
        self.action = "rules"

    def quit(self):
        """
        Sets the running flag to False, effectively stopping the game loop.
        """
        self.running = False

    def move_ferry(self):
        """
        Initiates the ferry movement sequence.
        Determines the destination shore based on current position and updates the model.
        """
        self.action = "ferry"
        side = self.model.game_state.entities.boat.which_shore
        if side == "left":
            side = "right"
        else:
            side = "left"
        self.model.game_state.entities.start_ferry(side)

    def resume(self):
        """
        Resumes the game from a paused state.
        Checks if the ferry was in motion to determine whether to return to 'ferry' or 'listen' state.
        """
        if not self.model.game_state.entities.is_ferry_done():
            self.action = "ferry"
        else:
            self.action = "listen"

    def pause(self):
        """
        Pauses the game by setting the action to 'pause'.
        """
        self.action = "pause"

    def win(self):
        """
        Handles the win condition.
        Triggers the win view and stops the game after a short delay.
        """
        self.view.render_end("win", self.model.game_state.moves_made)
        pygame.time.delay(settings.GAME_END_DELAY)
        self.running = False

    def lose(self):
        """
        Handles the lose condition.
        Checks if the loss animation logic is complete, then triggers the lose view.
        """
        settings.LOST = True
        if self.model.game_state.lose():
            self.view.render_end("lose", self.model.game_state.moves_made)
            pygame.time.delay(settings.GAME_END_DELAY)
            self.running = False

    def action_menu_pause(self):
        """
        Logic for the 'menu' and 'pause' states in the game loop.
        Updates button hover states and calls the event handler.
        """
        hovered_button = self.model.game_state.collisions.get_hovered_button(
            self.model.menu_state,
            pygame.mouse.get_pos(),
            self.action
        )
        if hovered_button is not None:
            self.model.menu_state.set_button_color(hovered_button, True)

        self.event_handler(hovered_button, None, self.action)

    def action_rules(self):
        """
        Logic for the 'rules' state in the game loop.
        Primarily listens for events (like ESC to exit rules).
        """
        self.event_handler(None, None, self.action)

    def action_listen(self):
        """
        Logic for the 'listen' state (active gameplay).
        Checks for hovered entities or the boat and calls the event handler.
        """
        hovered_entity = self.model.game_state.collisions.get_hovered_entity(
            self.model.game_state,
            pygame.mouse.get_pos()
        )

        self.event_handler(None, hovered_entity)

    def action_ferry(self):
        """
        Logic for the 'ferry' state (boat moving).
        Updates the boat position, checks for arrival, and determines the game outcome
        (win, lose, or continue listening).
        """
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
        """
        Logic for the 'win' state. Calls the win handler.
        """
        self.win()

    def action_lose(self):
        """
        Logic for the 'lose' state. Calls the lose handler and event handler
        to allow the lose animation to play out.
        """
        self.lose()
        self.event_handler()


    def run(self):
        """
        The main game loop.
        Continuously renders the game state and delegates logic execution
        based on the current `action` state.
        """
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