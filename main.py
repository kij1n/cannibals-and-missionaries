from controller import Controller
from model import Model
from view import View

def main():
    model = Model()
    view = View()
    game = Controller(model, view)
    game.run()

if __name__ == "__main__":
    main()