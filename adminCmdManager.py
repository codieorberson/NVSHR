import json
import os

command_data = {
    "Command1": "None",
    "Command2": "None",
    "Command3": "None",
    "Command4": "None"
}


class AdminCmdManager:
    def __init__(self):
        exists = os.path.exists("command.json")
        if exists:
            with open("command.json", encoding='utf-8', errors='ignore') as cmdJson:
                self.commandJson = json.load(cmdJson, strict=False)
                # print(self.commandJson)
                self.action = {}

                for x in range(1, 5):
                    self.action[x] = command_data["Command" + str(x)]

                cmdJson.close()
        else:
            with open("command.json", "w+") as write_file:
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

        with open("command.json", "r+") as write_file:

            write_file.seek(0)  # rewind
            json.dump(command_data, write_file)
            write_file.truncate()
            write_file.close()

    def read_from_file(self):
        json.load("command.json")
        self.action[1] = command_data["Command1"]
        self.action[2] = command_data["Command2"]
        self.action[3] = command_data["Command3"]
        self.action[4] = command_data["Command4"]
