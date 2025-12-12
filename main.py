"""
Main file to run the MVC game.
"""

from controller import Controller
from model import Model
from view import View


def main():
    """
    Initializes the MVC components and
    runs the game.
    :return: None
    """
    model = Model()
    view = View()
    game = Controller(model, view)
    game.run()


if __name__ == "__main__":
    main()
