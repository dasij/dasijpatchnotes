import json

# Ler os dois arquivos
with open('src/data/heroes/diablo.json', 'r', encoding='utf-8') as f:
    diablo = json.load(f)

with open('src/data/heroes/talents/diablo_talents.json', 'r', encoding='utf-8') as f:
    talents = json.load(f)

# Mapear níveis para nomes de seções
level_map = {
    "1": "Level 1",
    "4": "Level 4", 
    "7": "Level 7",
    "10": "Level 10",
    "13": "Level 13",
    "16": "Level 16",
    "20": "Level 20"
}

# Extrair os developerCommentary das patch notes
patch_notes = diablo['patchNotes'][0]
sections = patch_notes['sections']

# Criar dicionário de developerCommentary por nível e posição
commentary_map = {}

for section in sections:
    level_name = section['name']
    changes = section['changes']
    
    for idx, change in enumerate(changes):
        dev_comment = change.get('developerCommentary', '')
        if dev_comment:
            if level_name not in commentary_map:
                commentary_map[level_name] = {}
            commentary_map[level_name][idx] = dev_comment

print("Developer Commentary encontrados:")
for level, comments in commentary_map.items():
    print(f"  {level}: {len(comments)} comentários")

# Adicionar os developerCommentary aos talentos
for level_key, section_name in level_map.items():
    if level_key in talents and section_name in commentary_map:
        level_talents = talents[level_key]
        level_comments = commentary_map[section_name]
        
        for idx, talent in enumerate(level_talents):
            if idx in level_comments:
                dev_text = level_comments[idx]
                # Determinar onde colocar o texto
                if dev_text.startswith('Developer Comment:'):
                    # Verificar se o talento tem subtexts ou passives
                    if 'subtexts' in talent:
                        if 'developerCommentary' not in talent:
                            talent['developerCommentary'] = {}
                        talent['developerCommentary']['subtexts'] = dev_text
                    elif 'passives' in talent:
                        if 'developerCommentary' not in talent:
                            talent['developerCommentary'] = {}
                        talent['developerCommentary']['passives'] = dev_text
                    else:
                        # Adicionar como campo developerCommentary direto
                        talent['developerCommentary'] = dev_text
                else:
                    talent['developerCommentary'] = dev_text
                
                print(f"Adicionado ao nível {level_key}, talento {idx}: {dev_text[:50]}...")

# Salvar o arquivo atualizado
with open('src/data/heroes/talents/diablo_talents.json', 'w', encoding='utf-8') as f:
    json.dump(talents, f, indent=2, ensure_ascii=False)

print("\nArquivo salvo com sucesso!")
