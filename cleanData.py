import json

data = []
newData = []

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

def createStudioList(studioData):
    studios = []
    for studio in studioData:
        studios.append(studio["name"])
    return studios

def findYear(item):
    if item["year"] is not None:
        return item["year"]
    elif item["aired"]["prop"]["from"]["year"] is not None:
        return item["aired"]["prop"]["from"]["year"]
    else:
        return None

def cleanData():
    global data, newData
    for item in data:
        new_entries = {}
        new_entries["mal_id"] = item["mal_id"]
        new_entries["title"] = item["title"]
        new_entries["type"] = item["type"]
        new_entries["airing"] = item["airing"]
        new_entries["score"] = item["score"]
        new_entries["year"] = findYear(item)
        new_entries["rank"] = item["rank"]
        new_entries["popularity"] = item["popularity"]
        new_entries["favorites"] = item["favorites"]
        new_entries["studio"] = createStudioList(item["studios"]) if "studios" in item else []
        new_entries["genres"] = [genre["name"] for genre in item["genres"]] if "genres" in item else []
        new_entries["theme"] = [theme["name"] for theme in item["themes"]] if "themes" in item else []
        newData.append(new_entries)

#cleanData()

def save_cleaned_data(file_name):
    global newData
    with open(file_name, 'w') as file:
        json.dump(newData, file, indent=4)
    print("Cleaned data saved to 'movies.json'")

#save_cleaned_data()

def final_clean():
    global newData, data
    for item in data:
        del item["female_lead"]
        del item["male_lead"]
        print(item)
        newData.append(item)



def main():
    load_data('old-module_1_files/every.json')
    cleanData()
    save_cleaned_data('anime.json')
    print("Data cleaning process completed.")

main()