import os
import requests
from bs4 import BeautifulSoup
import json
import html
import re

def hero_name_with_underscore(hero_name):
    return f"{hero_name.lower()}_"

def normalize_name(name):
    """Normalize the name to match the image file naming convention."""
    return name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace(".", "").replace("-", "_")

def clean_description(description):
    """Remove unwanted Unicode characters from the description."""
    return description.replace("\u00a0", " ")

def extract_mana_and_cooldown(description):
    """Extract mana cost and cooldown from the description."""
    mana_cost = None
    cooldown = None

    mana_match = re.search(r'Mana:\s*(\d+)', description)
    cooldown_match = re.search(r'Cooldown:\s*(\d+s)', description)

    if mana_match:
        mana_cost = f"{mana_match.group(1)} Mana"
        description = description.replace(mana_match.group(0), "").strip()

    if cooldown_match:
        cooldown = cooldown_match.group(1)
        description = description.replace(cooldown_match.group(0), "").strip()

    return description, mana_cost, cooldown

def scrape_hero_data(hero_name):
    base_image_dir = os.path.join("src", "assets", "talents", hero_name)
    if not os.path.exists(base_image_dir):
        os.makedirs(base_image_dir)

    url = f"https://psionic-storm.com/en/heroes/{hero_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    talent_section = soup.find("div", class_="talent-tree live active")
    talent_links = talent_section.find_all("a", class_="talent-info") if talent_section else []

    talent_data = {}
    talent_images = {}

    for talent in talent_links:
        level = talent.get("data-tier-level")
        if level not in talent_data:
            talent_data[level] = []

        name = talent.get("data-original-title")
        if not name:
            img_tag = talent.find("img")
            if img_tag and img_tag.has_attr('alt'):
                name = img_tag['alt']

        description_html = talent.get("data-content")
        decoded_html = html.unescape(description_html)
        description = BeautifulSoup(decoded_html, "html.parser").text.strip()
        description = clean_description(description)
        description, mana_cost, cooldown = extract_mana_and_cooldown(description)

        img_tag = talent.find("img")
        if img_tag:
            image_url = img_tag['src']
            image_response = requests.get(f"https://psionic-storm.com{image_url}")
            image_name = os.path.basename(image_url)
            image_path = os.path.join(base_image_dir, image_name)
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
            normalized_name = normalize_name(name)
            talent_images[normalized_name] = image_name
        else:
            image_name = "default_talent.png"

        talent_entry = {
            "name": name,
            "description": description,
            "image": image_name,
            "talentChanged": False
        }

        if mana_cost:
            talent_entry["manaCost"] = mana_cost
        if cooldown:
            talent_entry["cooldown"] = cooldown

        talent_data[level].append(talent_entry)

    abilities_data = {
        "basic": [],
        "heroic": [],
        "trait": {}
    }

    def scrape_abilities(ul_class, ability_type):
        abilities_section = soup.find("ul", class_=ul_class)
        if abilities_section:
            abilities = abilities_section.find_all("li")
            for ability in abilities:
                name = ability.find("h3", class_="ability-name").text.strip()
                stats = ability.find("p", class_="ability-stats")
                stats_text = stats.text.strip() if stats else ""
                description = ability.find("p", class_="ability-description").text.strip()
                description = clean_description(description)
                description, mana_cost, cooldown = extract_mana_and_cooldown(stats_text + " " + description)
                name_without_parentheses = name.split(" (")[0]
                normalized_name = normalize_name(f"{hero_name}_{name_without_parentheses}")
                image_name = f"{normalized_name}.png"

                ability_data = {
                    "name": name,
                    "description": description,
                    "image": image_name,
                    "abilityChanged": False
                }

                if mana_cost:
                    ability_data["manaCost"] = mana_cost
                if cooldown:
                    ability_data["cooldown"] = cooldown

                if ability_type == "trait":
                    abilities_data[ability_type] = ability_data
                else:
                    abilities_data[ability_type].append(ability_data)

    scrape_abilities("abilities-list js-abilities-regular", "basic")
    scrape_abilities("abilities-list js-abilities-heroic", "heroic")
    scrape_abilities("abilities-list js-abilities-trait", "trait")

    hero_data = {
        "abilities": abilities_data
    }
    hero_data.update(talent_data)

    return hero_data

def generate_hero_json(hero_name):
    hero_underscore = hero_name_with_underscore(hero_name)
    return {
        "id": 999,
        "name": hero_name.upper(),
        "role": "",
        "image": f"heroes_portraits/{hero_name}.webp",
        "show": "false",
        "patchNotes": [
            {
                "id": 999,
                "title": "",
                "general": [
                    {
                        "change_id": f"{hero_underscore}",
                        "change": "",
                        "texts": [
                            {
                                "text": ""
                            }
                        ],
                        "developerCommentary": "",
                        "likes": 0,
                        "likedBy": {}
                    }
                ],
                "developerCommentary": "",
                "sections": [
                    {
                        "name": f"Level {level}",
                        "changes": [
                            {
                                "change_id": f"{hero_underscore}",
                                "name": "",
                                "texts": [
                                    {
                                        "text": "",
                                        "subtexts": [""]
                                    }
                                ],
                                "developerCommentary": "",
                                "likes": 0,
                                "likedBy": {}
                            }
                        ]
                    } for level in [1, 4, 7, 10, 13, 16, 20]
                ]
            }
        ]
    }


def scrape_and_save_hero_data(hero_name):
    hero_data = scrape_hero_data(hero_name)

    # Save vanilla talents
    vanilla_json_filename = os.path.join("src", "data", "heroes", "talents", f"{hero_name}_talents_vanilla.json")
    if not os.path.exists(os.path.dirname(vanilla_json_filename)):
        os.makedirs(os.path.dirname(vanilla_json_filename))
    with open(vanilla_json_filename, "w") as file:
        json.dump(hero_data, file, indent=2)

    # Save non-vanilla talents (same as vanilla for now)
    non_vanilla_json_filename = os.path.join("src", "data", "heroes", "talents", f"{hero_name}_talents.json")
    with open(non_vanilla_json_filename, "w") as file:
        json.dump(hero_data, file, indent=2)

    # Generate and save hero-specific JSON
    hero_json_data = generate_hero_json(hero_name)
    hero_json_filename = os.path.join("src", "data", "heroes", f"{hero_name}.json")
    if not os.path.exists(os.path.dirname(hero_json_filename)):
        os.makedirs(os.path.dirname(hero_json_filename))
    with open(hero_json_filename, "w") as file:
        json.dump(hero_json_data, file, indent=2)

    print(f"Data for {hero_name} has been scraped and saved successfully.")


heroes = [
    "Hogger", 
    "Deathwing"
]


# Example usage
for hero in heroes:
    try:
        print(f"Processing {hero}...")
        scrape_and_save_hero_data(hero.lower())
        print(f"Finished processing {hero}")
    except Exception as e:
        print(f"Error processing {hero}: {str(e)}")
        continue

print("All heroes have been processed.")

