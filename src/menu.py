#!/usr/bin/env python3
"""
Module that manages the creating of GUI menus for the game
"""
import pygame
import os


class Message:

    @staticmethod
    def showGeneralGameInformation(screen, interactionKeys):
        """
        Shows the general game control according to the keys that are defined
        by the game
        """
        # General Game Information
        initialX = 800
        initialY = -1
        isHelpMenu = type(interactionKeys) == dict
        key = None
        value = None
        for interactionKey in interactionKeys:
                if isHelpMenu:
                    key, value = interactionKey, interactionKeys[interactionKey]
                else:
                    key, value = interactionKey[0], interactionKey[1]
                outputString = "Press {}: {}".format(key, value)
                Message.text_to_screen(screen, outputString, initialX, initialY, 18)
                initialY += 20

    @staticmethod
    def showCredits(screen):
        screen.blit(pygame.image.load("img/credits.png"), (0, 0))
        pygame.display.update()


    @staticmethod
    def showGameOverMessage(screen):
        pass

    @staticmethod
    def showGameWonMessage(screen):
        positionX = screen.get_width() / 2
        positionY = screen.get_height() / 2
        Message.text_to_screen(screen, "Game Won", positionX, positionY, 36)


    @staticmethod
    def write(msg="pygame is cool", size=15, color=(255, 255, 255), bold = False, font_type = "None"):
        myfont = pygame.font.SysFont(font_type, size, bold)
        mytext = myfont.render(msg, True, color)
        mytext = mytext.convert_alpha()
        return mytext

    @staticmethod
    def text_to_screen(screen, text, x, y, size = 16, color = (255, 255, 255), font_type = 'couriernew'):
        try:
            text = str(text)
            font = pygame.font.SysFont(font_type, size)
            text = font.render(text, True, color)
            screen.blit(text, (x, y))

        except Exception:
            print('Font Error, saw it coming')


class Menu:
    """
    Represents Game Menu that include the menu that is shown to the user
    at the beginning of the game, and the menu that the user can access
    while in the game in order to save the game state
    """

    def __init__(self):
        """
        Defines all the menu configurations possible for the game.
        For example one menu configuration is the initial game menu.
        """

        # Configuration for the initial game menu associating a key to a button
        self.initialMenuButtons = (
            ('play_game', Button("Play Game Now!")),
            ('load_game', Button("Load Saved Game")),
            ('exit_game', Button("Exit Game")),
            ('show_credits', Button("Show Credits")),
            ('game_music', Button("Game Music: On"))
        )
        # Configuration for the pause menu
        self.pauseMenuButtons = (
            ('resume_game', Button("Resume Game")),
            ('save_game', Button("Save Game")),
            ('exit_game', Button("Exit Game"))
        )
        # Identifiers that associated to the tuple of menu configuration
        self.identifiers = {
            'initialMenu': self.initialMenuButtons,
            'pauseMenu': self.pauseMenuButtons
        }

    def _initializeMenu(self, screen, menuString):
        """
        _initializeMenu(screen, menuString) -> Initializes the button as
        well as the menu title
        """
        # Clear screen and create menu title text surface
        screen.fill((42, 54, 64))
        menu_title = Message.write(
            "Treasure Hunters", 40, (84, 183, 215), True, "couriernew")
        # Put menu title centered
        srect = screen.get_rect()
        mtrect = menu_title.get_rect()
        screen.blit(menu_title, ((srect.width - mtrect.width) / 2, 50))

        # Create Button objects and assign its meaning
        buttonList = [i[1] for i in self.identifiers[menuString]]
        buttonKeys = [i[0] for i in self.identifiers[menuString]]

        return buttonKeys, buttonList

    def show_menu(self, screen, FPS, menuString="initialMenu"):
        ''' This function shows a menu and returns the user selections '''
        menu = True
        selections = {}

        button_keys, button_list = self._initializeMenu(screen, menuString)

        # Create selections dictionary
        selections = dict([(key, False) for key in button_keys])
        if menuString == "initialMenu":
            selections['game_music'] = True
        # First button will be selected at beginning (unselected by default)
        button_list[0].toggle()
        # Control selected button
        selected = 0
        # Draw buttons on screen (will set position for each one)
        for i, b in enumerate(button_list):
            b.draw_centered(screen, 200 + i * 50)

        clock = pygame.time.Clock()
        showCredits = False
        while menu:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    selections['exit_game'] = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu = False
                        selections['exit_game'] = True
                    elif event.key == pygame.K_UP:
                        if selected > 0:
                            button_list[selected].toggle()
                            button_list[selected - 1].toggle()
                            selected -= 1
                    elif event.key == pygame.K_DOWN:
                        if selected < (len(button_list) - 1):
                            button_list[selected].toggle()
                            button_list[selected + 1].toggle()
                            selected += 1
                    elif event.key == pygame.K_RETURN:
                        if selected > 2:
                            selections[button_keys[selected]] = not selections[
                                button_keys[selected]]
                            if menuString == "initialMenu":
                                # Change button label (on/off buttons)
                                if button_keys[selected] == 'game_music':
                                    if selections[button_keys[selected]]:
                                        button_list[selected].set_label(
                                            "Game Music: On")
                                    else:
                                        button_list[selected].set_label(
                                            "Game Music: Off")
                                if button_keys[selected] == "show_credits":
                                    showCredits = True

                        else:
                            selections[button_keys[selected]] = True
                            menu = False
            # Calculate buttons area on screen and clear it
            width = max([button.width for button in button_list]) + 100
            height = button_list[len(button_list) - 1].pos[1] - button_list[
                0].pos[1] + button_list[len(button_list) - 1].height + 100
            buttons_area = pygame.Surface((width, height))
            buttons_area.fill((58, 78, 94))
            buttons_area = buttons_area.convert()

            if showCredits and menuString == "initialMenu":
                screen.blit(pygame.image.load("img/credits.png"), (0, 0))
                pygame.display.flip()
                pygame.time.wait(3500)
                self._initializeMenu(screen, menuString)
                showCredits = False

            screen.blit(buttons_area, (min([button.pos[0] for button in button_list]) - 50, button_list[0].pos[1] - 50))
            # Draw buttons on screen
            for i, b in enumerate(button_list):
                b.draw_centered(screen, 200 + i * 50)

            pygame.display.flip()

        return selections


class Button:
    initialized = False

    def __init__(self, text, min_width=200, selected=False):
        if not Button.initialized:
            # Load button shape from file (requires pygame.display initialized)
            button_sheet = pygame.image.load(
                os.path.join('img', 'menu_button.png')).convert_alpha()
            Button.unselected_head = button_sheet.subsurface((0, 0, 482, 34))
            Button.unselected_tail = button_sheet.subsurface((483, 34, 17, 34))
            Button.selected_head = button_sheet.subsurface((0, 68, 481, 34))
            Button.selected_tail = button_sheet.subsurface((483, 102, 17, 34))
            Button.initialized = True

        self.min_width = min_width
        self.set_label(text)
        self.is_selected = selected

    def draw_centered(self, screen, y_pos):
        self.pos = ((screen.get_rect().width - self.width) / 2, y_pos)

        if self.is_selected:
            screen.blit(self.selected, self.pos)
        else:
            screen.blit(self.unselected, self.pos)

    def toggle(self):
        self.is_selected = not self.is_selected

    def set_label(self, text):
        self.text_surface = Message.write(text, 20, (0, 0, 0), True, "couriernew")
        self.selected = Button.make_button(
            self.text_surface, self.min_width, (Button.selected_head, Button.selected_tail))
        self.unselected = Button.make_button(
            self.text_surface, self.min_width, (Button.unselected_head, Button.unselected_tail))
        rect = self.selected.get_rect()
        self.width = rect.width
        self.height = rect.height

    @staticmethod
    def make_button(text_surface, min_width, button_shape):
        trect = text_surface.get_rect()
        bhrect = button_shape[0].get_rect()
        btrect = button_shape[1].get_rect()
        width = max(min_width, trect.width)
        # Create empty button surface
        button = pygame.Surface((width + 2 * btrect.width, bhrect.height))
        button.set_colorkey((0, 0, 0))
        button = button.convert_alpha()
        # Fill surface with button shape and centered text
        button.blit(button_shape[0].subsurface(
            0, 0, btrect.width + width, bhrect.height), (0, 0))
        button.blit(button_shape[1], (btrect.width + width, 0))
        button.blit(
            text_surface, (btrect.width + (width - trect.width) / 2, 5))
        return button
