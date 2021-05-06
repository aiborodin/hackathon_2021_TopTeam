import json

class Entry:
    entries = []
    def __init__(self, output: str, inputs: [str], isAi: bool, next: [int]):
        # next: Entry
        self.output = output
        self.inputs = inputs
        self.next = next
        self.isAi = isAi

    def parseJson(jsonText: str):
        decoded = json.loads(jsonText)
        Entry.entries = list(map(
            lambda dict: Entry(dict["output"], dict["inputs"], dict["isAi"], dict["next"]),
            decoded))



