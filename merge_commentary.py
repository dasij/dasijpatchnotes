import json
import os

heroes = ["tyrael", "tyrande", "uther", "valeera", "valla", "varian", "whitemane", "xul", "yrel", "zagara", "zarya", "zeratul", "zuljin"]

results = []

for hero in heroes:
    try:
        patch_file = f"src/data/heroes/{hero}.json"
        talents_file = f"src/data/heroes/talents/{hero}_talents.json"
        
        # Verificar se arquivos existem
        if not os.path.exists(patch_file):
            results.append(f"[ERRO] {hero}: arquivo de patch notes nao encontrado")
            continue
        if not os.path.exists(talents_file):
            results.append(f"[ERRO] {hero}: arquivo de talentos nao encontrado")
            continue
        
        # Ler arquivos
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch_data = json.load(f)
        with open(talents_file, 'r', encoding='utf-8') as f:
            talents_data = json.load(f)
        
        # Criar dicionário de mudanças do patch notes por nome do talento
        patch_changes = {}
        
        for patch_note in patch_data.get('patchNotes', []):
            for section in patch_note.get('sections', []):
                level_name = section.get('name', '')  # "Level 1", "Level 4", etc.
                level_key = level_name.replace('Level ', '').strip()
                
                for change in section.get('changes', []):
                    talent_name = change.get('name', '').strip()
                    if not talent_name:
                        continue
                    
                    # Coletar texts
                    texts = []
                    subtexts = []
                    developer_commentary = change.get('developerCommentary', '').strip()
                    
                    for text_obj in change.get('texts', []):
                        if isinstance(text_obj, dict):
                            text_content = text_obj.get('text', '').strip()
                            if text_content:
                                texts.append(text_content)
                            
                            # Subtexts
                            for sub in text_obj.get('subtexts', []):
                                if isinstance(sub, str) and sub.strip():
                                    subtexts.append(sub.strip())
                    
                    patch_changes[talent_name] = {
                        'level': level_key,
                        'texts': texts,
                        'subtexts': [s for s in subtexts if s],
                        'developerCommentary': developer_commentary
                    }
        
        # Também verificar general changes
        for patch_note in patch_data.get('patchNotes', []):
            for change in patch_note.get('general', []):
                ability_name = change.get('change', '').strip()
                if not ability_name:
                    continue
                
                texts = []
                developer_commentary = change.get('developerCommentary', '').strip()
                
                for text_obj in change.get('texts', []):
                    if isinstance(text_obj, dict):
                        text_content = text_obj.get('text', '').strip()
                        if text_content:
                            texts.append(text_content)
                
                patch_changes[ability_name] = {
                    'level': 'general',
                    'texts': texts,
                    'subtexts': [],
                    'developerCommentary': developer_commentary
                }
        
        # Atualizar talentos
        updated = False
        talent_levels = ['1', '4', '7', '10', '13', '16', '20']
        
        for level in talent_levels:
            if level not in talents_data:
                continue
            
            for talent in talents_data[level]:
                if not isinstance(talent, dict):
                    continue
                
                talent_name = talent.get('name', '').strip()
                is_changed = talent.get('talentChanged', False) or talent.get('abilityChanged', False)
                
                # Procurar no patch_changes
                if talent_name in patch_changes:
                    patch_info = patch_changes[talent_name]
                    
                    # Adicionar developerCommentary se existir
                    if patch_info['developerCommentary']:
                        talent['developerCommentary'] = patch_info['developerCommentary']
                        updated = True
                    
                    # Adicionar subtexts se existirem
                    if patch_info['subtexts']:
                        talent['subtexts'] = patch_info['subtexts']
                        updated = True
                    
                    # Juntar texts na descrição se existirem
                    if patch_info['texts']:
                        original_desc = talent.get('description', '')
                        new_text = ' '.join(patch_info['texts'])
                        if new_text and new_text != original_desc:
                            talent['description'] = new_text
                            updated = True
        
        # Atualizar habilidades também
        abilities = talents_data.get('abilities', {})
        for ability_type in ['basic', 'heroic']:
            for ability in abilities.get(ability_type, []):
                if not isinstance(ability, dict):
                    continue
                
                ability_name = ability.get('name', '').strip()
                
                if ability_name in patch_changes:
                    patch_info = patch_changes[ability_name]
                    
                    if patch_info['developerCommentary']:
                        ability['developerCommentary'] = patch_info['developerCommentary']
                        updated = True
                    
                    if patch_info['subtexts']:
                        ability['subtexts'] = patch_info['subtexts']
                        updated = True
                    
                    if patch_info['texts']:
                        original_desc = ability.get('description', '')
                        new_text = ' '.join(patch_info['texts'])
                        if new_text and new_text != original_desc:
                            ability['description'] = new_text
                            updated = True
        
        # Trait
        trait = abilities.get('trait', {})
        if isinstance(trait, dict):
            trait_name = trait.get('name', '').strip()
            if trait_name in patch_changes:
                patch_info = patch_changes[trait_name]
                
                if patch_info['developerCommentary']:
                    trait['developerCommentary'] = patch_info['developerCommentary']
                    updated = True
                
                if patch_info['subtexts']:
                    trait['subtexts'] = patch_info['subtexts']
                    updated = True
                
                if patch_info['texts']:
                    original_desc = trait.get('description', '')
                    new_text = ' '.join(patch_info['texts'])
                    if new_text and new_text != original_desc:
                        trait['description'] = new_text
                        updated = True
        
        # Salvar arquivo atualizado
        if updated:
            with open(talents_file, 'w', encoding='utf-8') as f:
                json.dump(talents_data, f, indent=2, ensure_ascii=False)
            results.append(f"[OK] {hero}: atualizado com sucesso")
        else:
            results.append(f"[--] {hero}: nenhuma alteracao necessaria (sem dados para mesclar)")
        
    except Exception as e:
        results.append(f"[ERRO] {hero}: erro - {str(e)}")

print("\n".join(results))
