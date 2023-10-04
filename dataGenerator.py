# This file is for quickly adding pokemon to the pokemon.json data file, instead of having to manually enter data or sort out the pokemon apis

import json
import re

data = []
counter = 0

try:
    with open("pokemon.json", "r") as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    data = []

while True:
    try:
        answer = input("Pokemon: ")
        newSet = answer[-1] != "."
        name = re.sub(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$", "", answer)

        entry = {"name": name, "set": newSet}
        data.append(entry)
        counter += 1

    except KeyboardInterrupt:
        with open("pokemon.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"\nAdded {counter} entries")
        break
