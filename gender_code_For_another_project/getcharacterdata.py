import requests
import json

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

# This is the URL for the AniList GraphQL API
ANILIST_API = "https://graphql.anilist.co"

charactersAll = []

# This is the GraphQL query for fetching main character details including their gender
query = """
query ($idMal: Int) {
  Media(idMal: $idMal, type: ANIME) {
    id
    title {
      romaji
      english
    }
    characters(role: MAIN) {
      edges {
        node {
          id
          name {
            full
          }
          gender
        }
      }
    }
  }
}
"""

def get_main_characters_with_gender(mal_id):
    global charactersAll
    try:
        variables = {"idMal": mal_id}
        response = requests.post(ANILIST_API, json={"query": query, "variables": variables})
        response.raise_for_status()  # Raise an error for HTTP errors
        data = response.json()
        
        media = data["data"]["Media"]
        title = media["title"]["romaji"]
        characters = media["characters"]["edges"]

        for char in characters:
            charactersAll.append({
                "id": char["node"]["id"],
                "anime": title,
                "character": char["node"]["name"]["full"],
                "gender": char["node"]["gender"]
            })
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching MAL ID {mal_id}: {http_err}")
    except Exception as err:
        print(f"An error occurred while fetching MAL ID {mal_id}: {err}")

def save_cleaned_data():
    global charactersAll
    with open('character.json', 'w') as file:
        json.dump(charactersAll, file, indent=4)
    print("Cleaned data saved to 'character.json'")

def main():
    global charactersAll
    load_data = loadData()
    for anime in load_data:
        mal_id = anime.get("mal_id")
        get_main_characters_with_gender(mal_id)
    # After fetching all characters, you can now use charactersAll as needed
    print(f"Total characters fetched: {len(charactersAll)}")
    save_cleaned_data()


main()
