import json
def write(path, obj):
    json.dump(obj, open(path, 'w'), default=str, indent=2)
