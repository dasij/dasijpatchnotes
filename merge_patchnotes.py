import json
import os

heroes = [
    "kaelthas", "kelthuzad", "kerrigan", "kharazim", "leoric", "li-ming", "lili",
    "lt-morales", "lucio", "lunara", "maiev", "malfurion", "malganis", "malthael",
    "medivh", "mei", "mephisto", "muradin", "murky", "nazeebo", "nova", "orphea"
]

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_talent_changes(patch_notes):
    """Extrai mudanças de talentos do patch notes, indexadas por nome do talento."""
    changes = {}
    
    for note in patch_notes.get('patchNotes', []):
        # Processar seções de mudanças
        for section in note.get('sections', []):
            for change in section.get('changes', []):
                name = change.get('name', '')
                texts = change.get('texts', [])
                developer_commentary = change.get('developerCommentary')
                
                # Extrair subtexts se existirem
                subtexts = None
                if texts and len(texts) > 0:
                    subtexts = texts[0].get('subtexts')
                
                # Juntar textos na descrição
                description = None
                if texts:
                    text_parts = []
                    for t in texts:
                        if 'text' in t:
                            text_parts.append(t['text'])
                    if text_parts:
                        description = ' '.join(text_parts)
                
                changes[name] = {
                    'developerCommentary': developer_commentary,
                    'subtexts': subtexts,
                    'description': description
                }
        
        # Processar mudanças gerais (abilities)
        for general in note.get('general', []):
            change_name = general.get('change', '')
            texts = general.get('texts', [])
            developer_commentary = general.get('developerCommentary')
            
            subtexts = None
            if texts and len(texts) > 0:
                subtexts = texts[0].get('subtexts')
            
            description = None
            if texts:
                text_parts = []
                for t in texts:
                    if 'text' in t:
                        text_parts.append(t['text'])
                if text_parts:
                    description = ' '.join(text_parts)
            
            changes[change_name] = {
                'developerCommentary': developer_commentary,
                'subtexts': subtexts,
                'description': description
            }
    
    return changes

def find_matching_change(talent_name, talent_desc, changes):
    """Encontra a mudança correspondente baseado no nome ou descrição."""
    # Procurar por match no nome
    for change_name, change_data in changes.items():
        # Verificar se o nome do talento está no change_name
        if talent_name.lower() in change_name.lower() or change_name.lower() in talent_name.lower():
            return change_data
    return None

def process_hero(hero):
    patch_path = f"src/data/heroes/{hero}.json"
    talents_path = f"src/data/heroes/talents/{hero}_talents.json"
    
    if not os.path.exists(patch_path):
        return hero, f"Arquivo não encontrado: {patch_path}"
    if not os.path.exists(talents_path):
        return hero, f"Arquivo não encontrado: {talents_path}"
    
    try:
        patch_data = load_json(patch_path)
        talents_data = load_json(talents_path)
    except Exception as e:
        return hero, f"Erro ao carregar JSON: {e}"
    
    changes = extract_talent_changes(patch_data)
    modified_count = 0
    
    # Processar abilities
    if 'abilities' in talents_data:
        for ability_type in ['basic', 'heroic']:
            if ability_type in talents_data['abilities']:
                for ability in talents_data['abilities'][ability_type]:
                    if ability.get('abilityChanged'):
                        ability_name = ability.get('name', '')
                        match = find_matching_change(ability_name, ability.get('description', ''), changes)
                        if match and match.get('developerCommentary'):
                            ability['developerCommentary'] = match['developerCommentary']
                            if match.get('subtexts'):
                                ability['subtexts'] = match['subtexts']
                            modified_count += 1
        
        # Processar trait
        if 'trait' in talents_data['abilities']:
            trait = talents_data['abilities']['trait']
            if trait.get('abilityChanged'):
                trait_name = trait.get('name', '')
                match = find_matching_change(trait_name, trait.get('description', ''), changes)
                if match and match.get('developerCommentary'):
                    trait['developerCommentary'] = match['developerCommentary']
                    if match.get('subtexts'):
                        trait['subtexts'] = match['subtexts']
                    modified_count += 1
    
    # Processar talentos (níveis 1, 4, 7, 10, 13, 16, 20)
    for level in ['1', '4', '7', '10', '13', '16', '20']:
        if level in talents_data:
            for talent in talents_data[level]:
                if talent.get('talentChanged'):
                    talent_name = talent.get('name', '')
                    match = find_matching_change(talent_name, talent.get('description', ''), changes)
                    if match and match.get('developerCommentary'):
                        talent['developerCommentary'] = match['developerCommentary']
                        if match.get('subtexts'):
                            talent['subtexts'] = match['subtexts']
                        modified_count += 1
    
    save_json(talents_path, talents_data)
    return hero, f"OK - {modified_count} itens modificados"

# Processar todos os heróis
results = []
for hero in heroes:
    result = process_hero(hero)
    results.append(result)
    print(f"{result[0]}: {result[1]}")

print("\n" + "="*50)
print("RESUMO:")
print("="*50)
for hero, status in results:
    print(f"{hero}: {status}")
