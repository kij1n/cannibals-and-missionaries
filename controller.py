import pygame
from model import Model
from view import View
import settings


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.running = False

        self.fps = pygame.time.Clock()

    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


        self.fps.tick(settings.FRAMERATE)