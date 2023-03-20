import json

def change(file, dataDic_type):
    with open(file) as f:
        data = json.load(f)[dataDic_type
        return data]
