import os
import requests
from bs4 import BeautifulSoup
import json
import html

def scrape_hero_talents(hero_name):
    # Define the base directory for images
    base_image_dir = os.path.join("src", "assets", "talents", hero_name)
    if not os.path.exists(base_image_dir):
        os.makedirs(base_image_dir)

    # Construct the URL based on the hero name
    url = f"https://psionic-storm.com/en/heroes/{hero_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    talent_section = soup.find("div", class_="talent-tree live active")
    talent_links = talent_section.find_all("a", class_="talent-info") if talent_section else []

    talent_data = {}

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
        decoded_html = html.unescape(description_html)
        description = BeautifulSoup(decoded_html, "html.parser").text.strip()

        img_tag = talent.find("img")
        if img_tag:
            image_url = img_tag['src']
            image_response = requests.get(f"https://psionic-storm.com{image_url}")
            image_path = os.path.join(base_image_dir, os.path.basename(image_url))
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
        else:
            image_path = os.path.join(base_image_dir, "default_talent.png")

        talent_data[level].append({
            "name": name,
            "description": description,
            "image": image_path
        })

    # Save the data to a JSON file named after the hero
    json_filename = os.path.join("src", "data", "heroes", "talents", f"{hero_name}_talents.json")
    if not os.path.exists(os.path.dirname(json_filename)):
        os.makedirs(os.path.dirname(json_filename))
    with open(json_filename, "w") as file:
        json.dump(talent_data, file, indent=2)

# Example usage
hero_name = "lt-morales"  # This can be dynamically changed
scrape_hero_talents(hero_name)