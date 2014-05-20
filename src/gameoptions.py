"""
Module that carries out the possible game actions
"""
import json


def saveGame(currentLevel):
    saveStructure = {}

    for className, classNameSet in currentLevel['objects'].items():

        if className == "enemy" or className == "player":
            a = list(classNameSet)[0]

            character = currentLevel['built_objects'][a]
            print(character)
            saveStructure[className] = {
                'x': character.x,
                'y': character.y,
                'direction': character.direction,
                'health': character.health,
                'gun': character.currentGun,
                'isTreasureCaptured': character.treasureCaptured
            }
        elif className == "robot":
            robots = currentLevel['built_objects'][list(classNameSet)]
            robotsArray = []
            for robot in robots:
                robotsArray.append({
                    'x': robot.x,
                    'y': robot.y,
                    'direction': robot.direction,
                    'health': robot.health,
                    'gun': robot.currentGun
                })
            saveStructure[className] = robotsArray
        elif className == "object":
            a = list(classNameSet)[0]
            treasure = currentLevel['built_objects'][a]
            saveStructure[className] = {
                'x': treasure.x,
                'y': treasure.y
            }
        elif className == "door":
            doors = currentLevel['built_objects'][list(classNameSet)]
            doorsArray = []
            for door in doors:
                doorsArray.append({
                    'id': classNameSet,
                    'toggled': door.toogled
                })
        elif className == "lever":
            levers = currentLevel['built_objects'][list(classNameSet)]
            leversArray = []
            for level in levers:
                leversArray.append({
                    'id': classNameSet,
                    'off': level.off
                })
            saveStructure[className] = leversArray

    with open("game.json") as f:
        json.dump(saveStructure, f)



def loadGame():
    pass
