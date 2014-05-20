"""
Module that carries out the possible game actions
"""
import json


def saveGame(currentLevel):
    """
    saveGame(currentLevel) -> saves the current game state to a json file named "game.json"
    This means all the objects that are in the current level
    """
    saveStructure = {}

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



def loadGame():
    pass
