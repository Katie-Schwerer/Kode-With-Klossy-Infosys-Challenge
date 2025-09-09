import json

anime = []
animeNew = []
character = []

def load_data():
    global anime, character
    try:
        with open('anime.json', 'r') as f:
            anime = json.load(f)
        with open('character.json', 'r') as f:
            character = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")

def getGenderLead(item):
    matches = matches = list(filter(lambda d: d.get('anime') == item['title'], character))
    male = 0
    female = 0
    other = 0
    for match in matches:
        if match["gender"] == "Male":
            male += 1
        elif match["gender"] == "Female":
            female += 1
        else:
            other += 1

    if male > female and male > other:
        return "Male"
    elif female > male and female > other:
        return "Female"
    elif female == male:
        return "Both"
    else:
        return "Other"

def addLeadGender():
    global anime, character, animeNew
    for item in anime:
        del item["female_lead"]
        del item["male_lead"]
        item["lead_gender"] = getGenderLead(item)
        animeNew.append(item)

def save_data():
    global animeNew
    try:
        with open('character2.json', 'w') as f:
            json.dump(animeNew, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    load_data()
    addLeadGender()
    save_data()

main()