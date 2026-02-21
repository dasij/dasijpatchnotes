import os
import json
import re
import requests
from bs4 import BeautifulSoup


def normalize_name(name):
    """Normalize the name to match the image file naming convention."""
    return name.lower().replace(" ", "").replace("(", "").replace(")", "").replace("'", "").replace(".", "").replace("-", "")


def clean_description(description):
    """Remove unwanted Unicode characters and clean up the description."""
    description = description.replace("\u00a0", " ")
    # Remove extra whitespace
    description = re.sub(r'\s+', ' ', description).strip()
    return description


def extract_text_from_spans(element):
    """Extract text from spans, keeping numbers but removing scaling info."""
    if not element:
        return ""
    
    # Clone the element to not modify original
    text = str(element)
    # Remove <small> tags content (scaling info like "(+4% per level)")
    text = re.sub(r'<small>.*?</small>', '', text, flags=re.DOTALL)
    
    # Replace Quest/Reward spans with formatted tags following site pattern
    # {quest}Quest:{/quest}
    text = re.sub(
        r'<span class="heroes_tooltip_description_quest">\s*Quest:\s*</span>',
        '{quest}Quest:{/quest} ',
        text,
        flags=re.IGNORECASE
    )
    # {reward}Reward:{/reward}
    text = re.sub(
        r'<span class="heroes_tooltip_description_quest">\s*Reward:\s*</span>',
        '{reward}Reward:{/reward} ',
        text,
        flags=re.IGNORECASE
    )
    # {repeatable_quest}Repeatable Quest:{/repeatable_quest}
    text = re.sub(
        r'<span class="heroes_tooltip_description_quest">\s*Repeatable Quest:\s*</span>',
        '{repeatable_quest}Repeatable Quest:{/repeatable_quest} ',
        text,
        flags=re.IGNORECASE
    )
    
    # Replace Mythic Reward - match img tag followed immediately by "Mythic Reward:"
    # The img has path="@UI/StormTalentInTextQuestIcon" 
    text = re.sub(
        r'<img[^>]*>\s*Mythic Reward:\s*',
        '{mythic_reward}Mythic Reward:{/mythic_reward} ',
        text,
        flags=re.IGNORECASE
    )
    
    # Get text content
    soup = BeautifulSoup(text, 'html.parser')
    return clean_description(soup.get_text())



def parse_abilities_html(html_content, hero_name):
    """Parse abilities from the abilities HTML file."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    abilities_data = {
        "basic": [],
        "heroic": [],
        "trait": {}
    }
    
    # Find all ability tooltips
    ability_containers = soup.find_all('div', class_='heroes_tooltip heroes_ability_tooltip')
    
    for container in ability_containers:
        # Get name
        name_elem = container.find('span', class_='heroes_tooltip_name')
        if not name_elem:
            continue
        name = name_elem.get_text(strip=True)
        
        # Get key (Q, W, E, R, D, T)
        key_elem = container.find('span', class_='heroes_tooltip_key')
        key = key_elem.get_text(strip=True) if key_elem else ""
        
        # Full name with key
        full_name = f"{name} {key}" if key else name
        
        # Get description
        desc_elems = container.find_all('p', class_='heroes_tooltip_description')
        descriptions = []
        for desc in desc_elems:
            desc_text = extract_text_from_spans(desc)
            if desc_text:
                descriptions.append(desc_text)
        description = " ".join(descriptions)
        
        # Get mana and cooldown
        mana_cost = None
        cooldown = None
        
        attrs_elem = container.find('ul', class_='heroes_tooltip_attributes')
        if attrs_elem:
            for li in attrs_elem.find_all('li'):
                text = li.get_text(strip=True)
                if 'Mana:' in text:
                    mana_match = re.search(r'Mana:\s*(\d+)', text)
                    if mana_match:
                        mana_cost = f"{mana_match.group(1)} Mana"
                elif 'Cooldown:' in text:
                    cd_match = re.search(r'Cooldown:\s*([\d\.]+)\s*seconds?', text)
                    if cd_match:
                        cooldown = f"{cd_match.group(1)}s"
        
        # Get image
        img_elem = container.find('img', class_='heroes_tooltip_image')
        if img_elem:
            img_src = img_elem.get('src', '')
            img_name = os.path.basename(img_src)
            # Rename image to follow convention
            name_clean = normalize_name(name)
            image_name = f"{hero_name}_{name_clean}.png"
        else:
            image_name = f"{hero_name}_unknown.png"
        
        # Determine ability type
        ability_type = "basic"
        if attrs_elem:
            attrs_text = attrs_elem.get_text()
            if 'Heroic' in attrs_text or key == '(R)':
                ability_type = "heroic"
            elif 'Passive' in attrs_text or key == '(D)' or key == '(T)':
                ability_type = "trait"
        
        ability_entry = {
            "name": full_name,
            "description": description,
            "image": image_name,
            "abilityChanged": False
        }
        
        if mana_cost:
            ability_entry["manaCost"] = mana_cost
        if cooldown:
            ability_entry["cooldown"] = cooldown
        
        # Add to appropriate list
        if ability_type == "trait":
            abilities_data["trait"] = ability_entry
        elif ability_type == "heroic":
            abilities_data["heroic"].append(ability_entry)
        else:
            abilities_data["basic"].append(ability_entry)
    
    return abilities_data


def parse_talents_html(html_content, hero_name):
    """Parse talents from the talents HTML file."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    talent_data = {}
    
    # Build a lookup of talent tooltips by name
    talent_tooltips = {}
    tooltip_containers = soup.find_all('div', class_='heroes_tooltip heroes_talent_tooltip')
    
    for container in tooltip_containers:
        name_elem = container.find('span', class_='heroes_tooltip_name')
        if not name_elem:
            continue
        name = name_elem.get_text(strip=True)
        
        # Get description
        desc_elems = container.find_all('p', class_='heroes_tooltip_description')
        descriptions = []
        for desc in desc_elems:
            desc_text = extract_text_from_spans(desc)
            if desc_text:
                descriptions.append(desc_text)
        description = " ".join(descriptions)
        
        # Get image
        img_elem = container.find('img', class_='heroes_tooltip_image')
        if img_elem:
            img_src = img_elem.get('src', '')
            img_name = os.path.basename(img_src)
            # Convert jpg to png for consistency and remove storm_ui_icon_ prefix
            img_name = img_name.replace('.jpg', '.png')
            img_name = img_name.replace('storm_ui_icon_', '')
        else:
            img_name = "default_talent.png"
        
        # Check for cooldown in attributes
        cooldown = None
        attrs_elem = container.find('ul', class_='heroes_tooltip_attributes')
        if attrs_elem:
            for li in attrs_elem.find_all('li'):
                text = li.get_text(strip=True)
                if 'Cooldown:' in text:
                    cd_match = re.search(r'Cooldown:\s*([\d\.]+)\s*seconds?', text)
                    if cd_match:
                        cooldown = f"{cd_match.group(1)}s"
        
        talent_tooltips[name.lower()] = {
            "name": name,
            "description": description,
            "image": img_name,
            "cooldown": cooldown
        }
    
    # Parse talent table
    talent_table = soup.find('table', class_='talent_table')
    if talent_table:
        rows = talent_table.find_all('tr')
        for row in rows:
            # Get level
            level_elem = row.find('td', class_='talent_unlock')
            if not level_elem:
                continue
            level = level_elem.get_text(strip=True)
            
            # Get talents for this level
            talent_list = row.find('td', class_='talent_list')
            if not talent_list:
                continue
            
            talent_data[level] = []
            
            talent_containers = talent_list.find_all('span', class_='talent_container')
            for container in talent_containers:
                # Get talent name from alt text of image
                img_elem = container.find('img', class_='talent_image')
                if not img_elem:
                    continue
                
                talent_name = img_elem.get('alt', '')
                
                # Lookup full description from tooltips
                tooltip_info = talent_tooltips.get(talent_name.lower(), {})
                
                talent_entry = {
                    "name": talent_name,
                    "description": tooltip_info.get("description", ""),
                    "image": tooltip_info.get("image", "default_talent.png"),
                    "talentChanged": False
                }
                
                # Add cooldown from tooltip attributes (for active talents)
                if tooltip_info.get("cooldown"):
                    talent_entry["cooldown"] = tooltip_info["cooldown"]
                
                talent_data[level].append(talent_entry)
    
    return talent_data


def scrape_from_icy_veins(hero_name, download_images=True):
    """
    Scrape hero data directly from Icy Veins website.
    
    Args:
        hero_name: Hero name in URL format (e.g., 'muradin', 'artanis', 'li-ming')
        download_images: Whether to download talent images
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # URLs
    abilities_url = f"https://www.icy-veins.com/heroes/{hero_name}-abilities-strategy"
    talents_url = f"https://www.icy-veins.com/heroes/{hero_name}-talents"
    
    hero_data = {
        "abilities": {
            "basic": [],
            "heroic": [],
            "trait": {}
        }
    }
    
    # Fetch and parse abilities
    print(f"Fetching abilities from: {abilities_url}")
    try:
        response = requests.get(abilities_url, headers=headers, timeout=30)
        response.raise_for_status()
        hero_data["abilities"] = parse_abilities_html(response.text, hero_name)
        print(f"  Found {len(hero_data['abilities']['basic'])} basic abilities")
        print(f"  Found {len(hero_data['abilities']['heroic'])} heroic abilities")
        print(f"  Found trait: {bool(hero_data['abilities']['trait'])}")
    except Exception as e:
        print(f"  Error fetching abilities: {e}")
    
    # Fetch and parse talents
    print(f"Fetching talents from: {talents_url}")
    try:
        response = requests.get(talents_url, headers=headers, timeout=30)
        response.raise_for_status()
        talent_data = parse_talents_html(response.text, hero_name)
        hero_data.update(talent_data)
        print(f"  Found talents for levels: {', '.join(talent_data.keys())}")
        
        # Add mana/cooldown to level 10 heroics from abilities data
        if '10' in talent_data and hero_data['abilities']['heroic']:
            for i, heroic in enumerate(hero_data['abilities']['heroic']):
                for talent in talent_data['10']:
                    if talent['name'] in heroic['name']:
                        if 'manaCost' in heroic:
                            talent['manaCost'] = heroic['manaCost']
                        if 'cooldown' in heroic:
                            talent['cooldown'] = heroic['cooldown']
    except Exception as e:
        print(f"  Error fetching talents: {e}")
    
    # Download images if requested
    if download_images:
        download_talent_images(hero_name, hero_data, headers)
    
    # Save to JSON
    json_filename = os.path.join("src", "data", "heroes", "talents", f"{hero_name}_talents_vanilla.json")
    if not os.path.exists(os.path.dirname(json_filename)):
        os.makedirs(os.path.dirname(json_filename))
    
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(hero_data, file, indent=2, ensure_ascii=False)
    
    print(f"[OK] Successfully saved data to: {json_filename}")
    return hero_data


def download_talent_images(hero_name, hero_data, headers):
    """Download talent images from Icy Veins."""
    base_image_dir = os.path.join("src", "assets", "talents", hero_name)
    if not os.path.exists(base_image_dir):
        os.makedirs(base_image_dir)
    
    print(f"Downloading images to: {base_image_dir}")
    
    # Collect all images to download
    images_to_download = set()
    
    # From abilities
    for ability_type in ['basic', 'heroic']:
        for ability in hero_data['abilities'].get(ability_type, []):
            img_name = ability.get('image', '')
            if img_name and img_name != f"{hero_name}_unknown.png":
                # Map to Icy Veins image name
                ability_name = ability['name'].split('(')[0].strip()
                ability_key = normalize_name(ability_name)
                icy_veins_name = f"storm_ui_icon_{hero_name}_{ability_key}.jpg"
                images_to_download.add((icy_veins_name, img_name))
    
    # From trait
    trait = hero_data['abilities'].get('trait', {})
    if trait:
        img_name = trait.get('image', '')
        if img_name:
            trait_name = trait['name'].split('(')[0].strip()
            trait_key = normalize_name(trait_name)
            icy_veins_name = f"storm_ui_icon_{hero_name}_{trait_key}.jpg"
            images_to_download.add((icy_veins_name, img_name))
    
    # From talents
    for level, talents in hero_data.items():
        if level == 'abilities' or not isinstance(talents, list):
            continue
        for talent in talents:
            img_name = talent.get('image', '')
            if img_name and not img_name.startswith('talent_'):
                # This is a hero-specific talent image
                talent_key = normalize_name(talent['name'])
                icy_veins_name = f"storm_ui_icon_{hero_name}_{talent_key}.jpg"
                images_to_download.add((icy_veins_name, img_name))
            elif img_name and img_name.startswith('talent_'):
                # Generic talent image
                images_to_download.add((img_name.replace('.png', '.jpg'), img_name))
    
    # Download images
    base_url = "https://static.icy-veins.com/images/heroes/icons/"
    downloaded = 0
    failed = 0
    
    for icy_name, local_name in images_to_download:
        img_path = os.path.join(base_image_dir, local_name)
        if os.path.exists(img_path):
            continue
        
        img_url = base_url + icy_name
        try:
            response = requests.get(img_url, headers=headers, timeout=10)
            if response.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                downloaded += 1
            else:
                # Try with .png extension
                img_url = img_url.replace('.jpg', '.png')
                response = requests.get(img_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(response.content)
                    downloaded += 1
                else:
                    failed += 1
        except Exception as e:
            failed += 1
    
    print(f"  Downloaded: {downloaded}, Failed: {failed}")


if __name__ == "__main__":
    # Configuration - change this to the hero you want to scrape
    hero_name = "muradin"  # Examples: "muradin", "artanis", "li-ming", "kaelthas"
    
    scrape_from_icy_veins(hero_name, download_images=True)
