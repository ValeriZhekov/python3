import requests
from bs4 import BeautifulSoup
import json
import os

url="https://en.wikipedia.org/wiki/ASEAN"
def fetch_and_parse(site_url):
    response=requests.get(site_url)
    response.raise_for_status()
    bs=BeautifulSoup(response.content,"html.parser")
    tables=bs.find_all("table")
    for curr in tables:
        if "Metropolitan area" in curr.get_text():
            return curr
    return None

def table_to_dict(table):
    rows=table.find_all("tr")
    headers=[th.text.strip() for th in rows[0].find_all("th")]

    if "Country" not in headers or "Core city" not in headers or "Population" not in headers:
        raise ValueError("missing columns")
    
    country_col=headers.index("Country")
    city_col=headers.index("Core city")
    population_col=headers.index("Population")
    area_col=headers.index("Area(km2)")
    dict={}
    for row in rows[1:]:
        cols=row.find_all(["td","th"])
        if len(cols)>population_col:
            country=cols[country_col].text.strip()
            city=cols[city_col].text.strip()
            population=int(cols[population_col].text.strip().replace(",",""))
            area=float(cols[area_col].text.strip().replace(",",""))
            density=round(population/area,2) if area>0 else None
            if country not in dict:
                dict[country]=[]
            dict[country].append({"city":city,"population":population,"area":area,"density":density})
    return dict

def save_to_file(data, filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
        
        if existing_data == data:
            print("No changes in data. File not updated.")
            return
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print("Data updated and saved to file.")

url="https://en.wikipedia.org/wiki/ASEAN"
filename="f1"
dictionary=table_to_dict(fetch_and_parse(url))
print(str(dictionary))
save_to_file(dictionary,filename)



