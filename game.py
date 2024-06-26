from gfs.image import Image

from jam.main_menu import MainMenu
from jam.in_game import InGame
from jam.option_menu import OptionMenu
from jam.defeat_menu import DefeatMenu
from jam.select_level_menu import SelectLevelMenu
from jam.victory_menu import VictoryMenu
from jam.custom_level_menu import CustomLevelMenu

from jam.states import MAIN_MENU, DEFEAT_MENU, LEVEL_SELECTION, IN_GAME, OPTION_MENU, CUSTOM_LEVEL_SELECTION


class Game:
    def __init__(self, width, height):
        self.surface_configuration = (width, height)

        self.state = [
            MainMenu(width, height),
            OptionMenu(width, height),
            InGame(width, height),
            VictoryMenu(width, height),
            DefeatMenu(width, height),
            SelectLevelMenu(width, height),
            CustomLevelMenu(width, height)
        ]

        self.current_state = MAIN_MENU

    def next_state(self):
        next_state = self.state[self.current_state].next_state
        if next_state is not None:
            self.state[self.current_state].next_state = None
            self.current_state = next_state

    def update(self):
        if self.current_state == OPTION_MENU:
            self.state[OPTION_MENU].update()
        else:
            self.state[self.current_state].update(self.state[OPTION_MENU])

        self.next_state()

    def keyboard_input(self, event):

        if self.current_state == LEVEL_SELECTION:
            self.state[LEVEL_SELECTION].keyboard_input(event, self.state[IN_GAME])
        elif self.current_state == CUSTOM_LEVEL_SELECTION:
            self.state[CUSTOM_LEVEL_SELECTION].keyboard_input(event, self.state[IN_GAME])
        else:
            self.state[self.current_state].keyboard_input(event)

        self.next_state()

    def mouse_input(self, event):
        self.state[self.current_state].mouse_input(event)
        self.next_state()

    def mouse_motion(self, event):
        self.state[self.current_state].mouse_motion(event)
        self.next_state()

    def render(self, surface):
        self.state[self.current_state].render(surface)
