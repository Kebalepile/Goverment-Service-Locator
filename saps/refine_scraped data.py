import json
from itertools import groupby

# File names.
scraped_data = 'contacts_data.json'
cleaned_data = 'refined_data.json'

with open(scraped_data) as file:

    data_list = json.load(file)
    data_list.sort(key=lambda data: data["province"])

    refined_data = [
        max(g, key=lambda data: data["police_stations"]["total"]) for k, g in groupby(data_list, key=lambda data: data["province"])
    ]
    
with open(cleaned_data, 'w') as file:
    json.dump(refined_data, file, indent=4)
