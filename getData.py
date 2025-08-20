import requests
import json

pageCount = 1
masterList = []

def addToMasterList(data):
    for d in data:
        masterList.append(d)

while True:
    try:
        ## api_url = f"https://api.jikan.moe/v4/anime?page={pageCount}&type=tv" - The call to get all the tv series.
        api_url = f"https://api.jikan.moe/v4/anime?page={pageCount}&type=movie" # this one is the movies
        response = requests.get(api_url)
        addToMasterList(response.json()["data"])
        print(f"Page {pageCount} Completed!")
        pageCount += 1
        if not response.json()["pagination"]["has_next_page"]:
            print("Done!")
            break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

with open("movieData.json", "w") as f:
    json.dump(masterList, f, indent=4)