import json


def change_type(jsnFile, dicFile):
    with open(jsnFile) as f:
        data = json.load(f)[dicFile]
        return data