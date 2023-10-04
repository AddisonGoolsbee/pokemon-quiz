import json
import re

data = []

while True:
    try:
        # Get user input for name and true/false value
        answer = input("Pokemon: ")
        newSet = answer[-1] != '.'
        name = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', answer)
        print(name, newSet)

        # Create a dictionary to store the data
        data.append({
            "name": name,
            "set": newSet
        })
    except KeyboardInterrupt:
        with open("pokemon.json", "w") as json_file:
            # Convert the dictionary to JSON format
            json_data = json.dumps(data, indent=4)
            json_file.write(json_data)
            print("Data written to pokemon.json")
            break


