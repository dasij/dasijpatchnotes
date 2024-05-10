import requests
from bs4 import BeautifulSoup
import json

url = "https://heroesofthestorm.fandom.com/wiki/Li_Li"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

talent_table = soup.find("div", class_="talent-table")
talent_tiers = talent_table.find_all("div", class_="talent-tier")

talent_data = {}

for tier in talent_tiers:
    level = tier.find("div", class_="talent-tier-label").text.strip()
    talent_data[level] = []

    talents = tier.find_all("div", class_="matched-height talent")
    for talent in talents:
        name = talent.find("div", class_="talent-name").text.strip()
        description = talent.find("div", class_="talent-description").find("p").text.strip()
        talent_data[level].append({"name": name, "description": description, "image": "talent1.png"})

with open("lili.json", "w") as file:
    json.dump(talent_data, file, indent=2)