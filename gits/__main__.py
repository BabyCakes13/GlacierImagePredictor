from utils import arguments
from ui import gui


def main():
    arguments.activate_arguments()


if __name__ == "__main__":
    # main()
    ui = gui.GUI()
    ui.start()
