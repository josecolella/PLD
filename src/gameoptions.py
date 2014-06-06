"""
Module that carries out the possible game actions
"""
import json
from sys import exit
import pygame


class GameOption:
    """
    Class that represents the management options allowed to the user
    when in the game. This includes saving the game and loading the game
    """

    @staticmethod
    def saveGame(currentLevel):
        """
        saveGame(currentLevel) -> saves the current game state to a json
        file named "game.json"
        This means all the objects that are in the current level
        Parameters
        -----------
        currentLevel
        saveGame(currentLevel) -> The game state is saved in game.json
        """
        saveStructure = {'level': currentLevel['levelIndex']}

        for className, classNameSet in currentLevel['objects'].items():

            if className == "enemy" or className == "player":
                character = currentLevel['built_objects'][next(iter(classNameSet))][0]
                saveStructure[className] = {
                    'x': character.x,
                    'y': character.y,
                    'direction': character.direction,
                    'health': character.health,
                    'gun': character.currentGun,
                    'isTreasureCaptured': character.treasureCaptured
                }
            elif className == "robot":
                robots = currentLevel['built_objects']
                robotsArray = []

                for robot in robots[next(iter(classNameSet))]:
                    robotsArray.append({
                        'x': robot.x,
                        'y': robot.y,
                        'direction': robot.direction,
                        'health': robot.health,
                        'isTreasureCaptured': robot.treasureCaptured
                    })
                saveStructure[className] = robotsArray
            elif className == "object":
                treasure = currentLevel['built_objects'][next(iter(classNameSet))][0]
                saveStructure[className] = {
                    'x': treasure.x,
                    'y': treasure.y
                }
            elif className == "door":
                doorsArray = []
                doorIter = (i for i in iter(classNameSet))
                for doorSymb in doorIter:
                    doorsArray.append({
                        'id': doorSymb,
                        'toggled': currentLevel['built_objects'][doorSymb][0].toggled
                    })
                saveStructure[className] = doorsArray

            elif className == "lever":
                leversArray = []
                leverIdIter = (i for i in iter(classNameSet))
                for leverSymb in leverIdIter:
                    for lever in currentLevel['built_objects'][leverSymb]:
                        leversArray.append({
                            'id': leverSymb,
                            'off': lever.off
                        })

                saveStructure[className] = leversArray

        with open("game.json", "w") as f:
            json.dump(saveStructure, f, indent=4)

    @staticmethod
    def loadGame(currentLevelList, currentLevel):
        """
        loadGame() -> loads the game state that is present in the game.json
        and sets up the game board, as stated in the file
        """

        game_state = {}
        taken = False
        with open("game.json", "r") as f:
            game_state = json.load(f)

        current = currentLevelList.buildLevelObject(currentLevel)
        for key in game_state:
            if key == "robot":
                for jsonRobot, pythonRobot in zip(game_state[key], current['built_objects']['r']):
                    pythonRobot.x = jsonRobot['x']
                    pythonRobot.y = jsonRobot['y']
                    pythonRobot.direction = jsonRobot['direction']
                    pythonRobot.health = jsonRobot['health']
            elif key == "player":
                current['built_objects']['j'][0].x = game_state[key]['x']
                current['built_objects']['j'][0].y = game_state[key]['y']
                current['built_objects']['j'][0].direction = game_state[key]['direction']
                current['built_objects']['j'][0].health = game_state[key]['health']
                current['built_objects']['j'][0].gun = game_state[key]['gun']
                current['built_objects']['j'][0].treasureCaptured = game_state[key]['isTreasureCaptured']
            elif key == "lever":
                for lever in game_state[key]:
                    current['built_objects'][lever['id']][0].off = lever['off']
            elif key == "door":
                for door in game_state[key]:
                    current['built_objects'][door['id']][0].toggled = door['toggled']
            elif key == "object":
                current['built_objects']['a'][0].x = game_state[key]['x']
                current['built_objects']['a'][0].y = game_state[key]['y']

        return current

    @staticmethod
    def exitGame():
        """
        exitGame() -> The game is exited
        """
        pygame.quit()
        exit(0)
