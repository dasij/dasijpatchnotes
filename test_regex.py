import re
from bs4 import BeautifulSoup

# Ler o arquivo HTML
with open('Muradin Abilities and Strategy - Heroes of the Storm - Icy Veins.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Testar o extract_text_from_spans com debug
def extract_text_from_spans_debug(element):
    """Extract text from spans, keeping numbers but removing scaling info."""
    if not element:
        return ""
    
    # Clone the element to not modify original
    text = str(element)
    print("Texto original:")
    print(text[:500])
    print("---")
    
    # Remove <small> tags content (scaling info like "(+4% per level)")
    text = re.sub(r'<small>.*?</small>', '', text, flags=re.DOTALL)
    
    # Replace Quest/Reward spans with formatted tags following site pattern
    text = re.sub(
        r'<span class="heroes_tooltip_description_quest">\s*Quest:\s*</span>',
        '{quest}Quest:{/quest} ',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'<span class="heroes_tooltip_description_quest">\s*Reward:\s*</span>',
        '{reward}Reward:{/reward} ',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'<span class="heroes_tooltip_description_quest">\s*Repeatable Quest:\s*</span>',
        '{repeatable_quest}Repeatable Quest:{/repeatable_quest} ',
        text,
        flags=re.IGNORECASE
    )
    
    # Replace Mythic Reward - match img tag followed immediately by "Mythic Reward:"
    print("Antes do regex Mythic:")
    print(text[:500])
    print("---")
    
    text = re.sub(
        r'<img[^>]*>\s*Mythic Reward:\s*',
        '{mythic_reward}Mythic Reward:{/mythic_reward} ',
        text,
        flags=re.IGNORECASE
    )
    
    print("Depois do regex Mythic:")
    print(text[:500])
    print("---")
    
    # Get text content
    soup = BeautifulSoup(text, 'html.parser')
    result = soup.get_text()
    
    # Clean up
    result = result.replace("\u00a0", " ")
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

# Encontrar o Storm Bolt tooltip
soup = BeautifulSoup(html, 'html.parser')
ability_containers = soup.find_all('div', class_='heroes_tooltip heroes_ability_tooltip')

for container in ability_containers:
    name_elem = container.find('span', class_='heroes_tooltip_name')
    if name_elem and name_elem.get_text(strip=True) == 'Storm Bolt':
        print("Encontrou Storm Bolt!")
        desc_elems = container.find_all('p', class_='heroes_tooltip_description')
        for i, desc in enumerate(desc_elems):
            print(f"\n--- Descrição {i+1} ---")
            result = extract_text_from_spans_debug(desc)
            print(f"Resultado final: {result[:200]}")
        break
