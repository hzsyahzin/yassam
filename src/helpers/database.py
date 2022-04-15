import json


def LoadSettings():
    with open("./settings.json") as settingsFile:
        data = json.load(settingsFile)
    return data


def SaveSettings(data):
    with open("./settings.json", "w") as settingsFile:
        settingsFile.write(json.dumps(data))
