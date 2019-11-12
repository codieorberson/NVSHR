import json
import os

# json data structure that stores the smart home actions
command_data = {
    "Command1": "None",
    "Command2": "None",
    "Command3": "None",
    "Command4": "None"
}

_file_name = "./dynamic_data/command.json"

class CommandManager:
    def __init__(self):
        exists = os.path.exists(_file_name)
        if exists:
            with open(_file_name, encoding='utf-8', errors='ignore') as cmdJson:
                self.commandJson = json.load(cmdJson, strict=False)
                # print(self.commandJson)
                self.action = {}

                for x in range(1, 5):
                    self.action[x] = self.commandJson["Command" + str(x)]

                cmdJson.close()
        else:
            with open(_file_name, "w+") as write_file:
                json.dump(command_data, write_file)
                write_file.close()

    def write_to_file(self, optionNum, action):
        if optionNum == 1:
            command_data["Command1"] = action
        elif optionNum == 2:
            command_data["Command2"] = action
        elif optionNum == 3:
            command_data["Command3"] = action
        else:
            command_data["Command4"] = action

        with open(_file_name, "r+") as write_file:

            # Start from the beginning of the file and save the needed data
            write_file.seek(0)
            json.dump(command_data, write_file)
            write_file.truncate()
            write_file.close()

    def read_from_file(self):
        json.load(_file_name)

        for x in range(1, 5):
            self.action[x] = self.commandJson["Command" + str(x)]
