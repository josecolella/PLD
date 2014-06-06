"""
Module that carries out the possible game actions
"""
import json
from sys import exit
import pygame
from AI import AgentServer


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
                        'gun': robot.currentGun,
                        'isTreasureCaptured': robot.treasureCaptured
                    })
                saveStructure[className] = robotsArray
            elif className == "object":
                treasure = currentLevel['built_objects'][next(iter(classNameSet))][0]
                saveStructure[className] = {
                    'x': treasure.x,
                    'y': treasure.y,
                    'isCaptured': treasure.isCaptured
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
                    pythonRobot.currentGun = jsonRobot['gun']
                    pythonRobot.treasureCaptured = jsonRobot['isTreasureCaptured']

            elif key == "player" or key == "enemy":
                for charactIdentifier in currentLevel['objects'][key]:
                    currentLevel['built_objects'][charactIdentifier][0].x = game_state[key]['x']
                    currentLevel['built_objects'][charactIdentifier][0].y = game_state[key]['y']
                    currentLevel['built_objects'][charactIdentifier][0].direction = game_state[key]['direction']
                    currentLevel['built_objects'][charactIdentifier][0].health = game_state[key]['health']
                    currentLevel['built_objects'][charactIdentifier][0].gun = game_state[key]['gun']
                    currentLevel['built_objects'][charactIdentifier][0].treasureCaptured = game_state[key]['isTreasureCaptured']
            elif key == "lever":
                for lever in game_state[key]:
                    current['built_objects'][lever['id']][0].off = lever['off']
            elif key == "door":
                for door in game_state[key]:
                    current['built_objects'][door['id']][0].toggled = door['toggled']
            elif key == "object":
                for strIdentifier in currentLevel['objects'][key]:
                    current['built_objects'][strIdentifier][0].x = game_state[key]['x']
                    current['built_objects'][strIdentifier][0].y = game_state[key]['y']
                    current['built_objects'][strIdentifier][0].isCaptured = game_state[key]['isCaptured']
        return current

    @staticmethod
    def exitGame():
        """
        exitGame() -> The game is exited
        """
        AgentServer.get().stopAll()
        pygame.quit()
        exit(0)
