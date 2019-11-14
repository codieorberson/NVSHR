import json
import os

# json data structure that stores the smart home actions
command_data = {
    "Command1": [{"action": "None", "gestureSeq": "None"}],
    "Command2": [{"action": "None", "gestureSeq": "None"}],
    "Command3": [{"action": "None", "gestureSeq": "None"}],
    "Command4": [{"action": "None", "gestureSeq": "None"}]
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
                self.gestureSeq = {}

                i = 0
                for key in self.commandJson.keys():
                    data_item = self.commandJson[key]
                    if type(data_item) is dict:
                        self.action[i] = data_item['action']
                        self.gestureSeq[i] = data_item['gestureSeq']
                    i += 1
                cmdJson.close()
        else:
            with open(_file_name, "w+") as write_file:
                json.dump(command_data, write_file)
                write_file.close()

    def read_from_file(self):
        json.load(_file_name)

        for x in range(1, 5):
            for data_item in self.commandJson['Command' + str(x)]:
                self.action[x] = data_item['action']
                self.gestureSeq[x] = data_item['gestureSeq']

    def get_keys(self, itemNum):
        for data_item in self.commandJson['Command' + str(itemNum)]:
            self.action[itemNum] = data_item['action']
            self.gestureSeq[itemNum] = data_item['gestureSeq']

    def change_keys(self, itemNum, itemName, newItem):
        for data_item in self.commandJson['Command' + str(itemNum)]:
            if type(data_item) is dict:
                if itemName == 'action':
                    data_item['action'] = newItem
                    self.action[itemNum] = newItem
                    print(self.action[itemNum])
                else:
                    data_item['gestureSeq'] = newItem
                    self.gestureSeq[itemNum] = newItem

        with open(_file_name, "r+") as write_file:

            # Start from the beginning of the file and save the needed data
            write_file.seek(0)
            json.dump(self.commandJson, write_file)
            write_file.truncate()
            write_file.close()
