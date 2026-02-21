import os
import requests
from bs4 import BeautifulSoup
import json
import html
import re

def normalize_name(name):
    """Normalize the name to match the image file naming convention."""
    return name.lower().replace(" ", "").replace("(", "").replace(")", "").replace("'", "").replace(".", "").replace("-", "")

def normalize_ability_name(name):
    """Normalize ability name to match image file naming convention (uses underscores)."""
    return name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace(".", "").replace("-", "_")

def clean_description(description):
    """Remove unwanted Unicode characters and clean up the description."""
    description = description.replace("\u00a0", " ")
    # Remove extra whitespace
    description = re.sub(r'\s+', ' ', description).strip()
    return description

def extract_mana_and_cooldown(description):
    """Extract mana cost and cooldown from the description."""
    mana_cost = None
    cooldown = None

    # Regular expressions to find mana cost and cooldown
    mana_match = re.search(r'Mana:\s*(\d+)', description)
    cooldown_match = re.search(r'Cooldown:\s*(\d+s)', description)

    if mana_match:
        mana_cost = f"{mana_match.group(1)} Mana"
        description = description.replace(mana_match.group(0), "").strip()

    if cooldown_match:
        cooldown = cooldown_match.group(1)
        description = description.replace(cooldown_match.group(0), "").strip()

    return description, mana_cost, cooldown

def scrape_hero_talents(hero_name):
    # Define the base directory for images
    base_image_dir = os.path.join("src", "assets", "talents", hero_name)
    if not os.path.exists(base_image_dir):
        os.makedirs(base_image_dir)

    # Construct the URL based on the hero name
    url = f"https://psionic-storm.com/en/heroes/{hero_name}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape talents
    talent_section = soup.find("div", class_="talent-tree live active")
    talent_links = talent_section.find_all("a", class_="talent-info") if talent_section else []

    talent_data = {}
    talent_images = {}

    for talent in talent_links:
        level = talent.get("data-tier-level")
        if level not in talent_data:
            talent_data[level] = []

        name = talent.get("data-original-title")
        if not name:  # Check if name is empty
            img_tag = talent.find("img")
            if img_tag and img_tag.has_attr('alt'):
                name = img_tag['alt']  # Use the alt attribute of the img tag as a fallback

        description_html = talent.get("data-content")
        if description_html:
            decoded_html = html.unescape(description_html)
            description = BeautifulSoup(decoded_html, "html.parser").text.strip()
            description = clean_description(description)  # Clean the description
            description, mana_cost, cooldown = extract_mana_and_cooldown(description)  # Extract mana and cooldown
        else:
            description = ""
            mana_cost = None
            cooldown = None

        img_tag = talent.find("img")
        if img_tag:
            image_url = img_tag['src']
            # Ensure the URL is absolute
            if image_url.startswith('/'):
                image_url = f"https://psionic-storm.com{image_url}"
            elif not image_url.startswith('http'):
                image_url = f"https://psionic-storm.com/{image_url}"
                
            try:
                image_response = requests.get(image_url, headers=headers)
                image_response.raise_for_status()
                image_name = os.path.basename(image_url)
                image_path = os.path.join(base_image_dir, image_name)
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                normalized_name = normalize_name(name)
                talent_images[normalized_name] = image_name  # Map normalized talent name to image name
            except Exception as e:
                print(f"Warning: Could not download image for talent '{name}': {e}")
                image_name = "default_talent.png"
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

    # Scrape abilities
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
                name_elem = ability.find("h3", class_="ability-name")
                if not name_elem:
                    continue
                name = name_elem.text.strip()
                
                stats = ability.find("p", class_="ability-stats")
                stats_text = stats.text.strip() if stats else ""
                
                desc_elem = ability.find("p", class_="ability-description")
                description = desc_elem.text.strip() if desc_elem else ""
                
                description = clean_description(description)  # Clean the description
                description, mana_cost, cooldown = extract_mana_and_cooldown(stats_text + " " + description)  # Extract mana and cooldown
                
                # Remove the part in parentheses for image naming
                name_without_parentheses = name.split(" (")[0]
                normalized_name = normalize_ability_name(name_without_parentheses)
                image_name = f"{hero_name}_{normalized_name}.png"  # Construct the image name

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

    # Combine talents and abilities data
    hero_data = {
        "abilities": abilities_data
    }

    # Add talents data directly to hero_data (levels "1", "4", "7", "10", "13", "16", "20")
    hero_data.update(talent_data)

    # Save the talents data to a JSON file named after the hero
    json_filename = os.path.join("src", "data", "heroes", "talents", f"{hero_name}_talents_vanilla.json")
    if not os.path.exists(os.path.dirname(json_filename)):
        os.makedirs(os.path.dirname(json_filename))
    
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(hero_data, file, indent=2, ensure_ascii=False)
    
    print(f"[OK] Successfully scraped and saved data for {hero_name}")
    print(f"  - JSON saved to: {json_filename}")
    print(f"  - Images saved to: {base_image_dir}")
    
    return hero_data

# Example usage
if __name__ == "__main__":
    hero_name = "muradin"  # This can be dynamically changed
    scrape_hero_talents(hero_name)



