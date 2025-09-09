import json
import requests

def loadData():
    data = []
    try:
        with open("anime.json", "r") as file:
            data = json.load(file)
        print("Data loaded successfully")
    except FileNotFoundError:
        print("Error: 'anime.json' file not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from 'movies.json'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return data

def get_main_characters(data):
    allMainCharacters = []
    for anime in data:
        id = anime.get("mal_id")
        print(id)
        api_url = f"https://api.jikan.moe/v4/anime/{id}/characters"
        resp = requests.get(api_url)
        allCharacter = resp.json().get("data", [])
        mainCharacters = [char for char in allCharacter if char.get("role") == "Main"]
        for char in mainCharacters:
            #print(char)
            char_info = {}
            char_info["id"] = char['character']['mal_id']
            char_info["name"] = char['character']['name']
            char_info["anime_id"] = id
            char_info["anime_title"] = anime.get("title")
            allMainCharacters.append(char_info)
            print(char_info)
    return allMainCharacters


def main():
    data = loadData()
    main_characters = get_main_characters(data)
    with open("malmaincharacter.json", "w") as file:
        json.dump(main_characters, file, indent=4)

main()
