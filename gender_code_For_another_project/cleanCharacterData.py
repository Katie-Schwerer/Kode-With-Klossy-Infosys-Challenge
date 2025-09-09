import json
import requests
import re

data = []
newData = []

ANILIST_API = "https://graphql.anilist.co"

anilist_query = """
   query ($id: Int) {
     Character(id: $id) {
       id
       name { full }
       gender
     }
   }
"""

def load_data(file_path):
    global data
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        print("Data loaded successfully")
        print(f"Total records: {len(data)}")
        # print(data)
    except FileNotFoundError:
        print(f"Error: '{file_path}' file not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def cleanData(character):
    try:
        mal_id = character.get("id")
        variables = {"id": mal_id}
        response = requests.post(ANILIST_API, json={"query": anilist_query, "variables": variables})
        data = response.json()
        if "errors" in data:
          return None
        return data["data"]["Character"]["gender"]
    except Exception as e:
        print(f'Error occurred while cleaning data for character {character["character"]}: {e}')

def loopThruCharacters():
    global newData, data
    for character in data:
        if character["gender"] is None or character["gender"] == "Other":
            character["gender"] = cleanData(character)
            print(f"Updated gender for character {character['character']} to {character['gender']}")
        newData.append(character)

def save_data(file_path):
    global newData
    try:
        with open(file_path, 'w') as file:
            json.dump(newData, file, indent=4)
        print(f"Data saved successfully to '{file_path}'")
    except Exception as e:
        print(f"Error: Failed to save data to '{file_path}'. {e}")

def main():
    load_data('character.json')
    loopThruCharacters()
    save_data('character.json')

main()