import json
import os

heroes = [
    "probius", "qhira", "ragnaros", "raynor", "rehgar", "rexxar", 
    "samuro", "sgt-hammer", "sonya", "stitches", "stukov", "sylvanas", 
    "tassadar", "the-butcher", "the-lost-vikings", "thrall", "tracer", "tychus"
]

results = []

for hero in heroes:
    patch_file = f"src/data/heroes/{hero}.json"
    talents_file = f"src/data/heroes/talents/{hero}_talents.json"
    
    try:
        # Ler arquivos
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch_data = json.load(f)
        with open(talents_file, 'r', encoding='utf-8') as f:
            talents_data = json.load(f)
        
        # Criar mapeamento de mudancas do patch notes por nivel e nome
        patch_changes = {}  # {(level, name): {developerCommentary, texts, subtexts}}
        
        for patch in patch_data.get('patchNotes', []):
            for section in patch.get('sections', []):
                level = section.get('name', '').replace('Level ', '')
                for change in section.get('changes', []):
                    name = change.get('name', '')
                    dev_commentary = change.get('developerCommentary', '')
                    texts = change.get('texts', [])
                    
                    # Extrair subtexts e textos principais
                    all_subtexts = []
                    main_texts = []
                    
                    for text_obj in texts:
                        if isinstance(text_obj, dict):
                            # Texto principal
                            if 'text' in text_obj and text_obj['text']:
                                main_texts.append(text_obj['text'])
                            # Subtexts
                            if 'subtexts' in text_obj:
                                for st in text_obj['subtexts']:
                                    if st and st.strip():
                                        all_subtexts.append(st)
                    
                    # Só adicionar se houver dados relevantes
                    if name and (dev_commentary.strip() or main_texts or all_subtexts):
                        patch_changes[(level, name)] = {
                            'developerCommentary': dev_commentary,
                            'texts': main_texts,
                            'subtexts': all_subtexts
                        }
        
        # Atualizar talentos
        updated = False
        
        # Processar talentos em niveis numericos (1, 4, 7, 10, 13, 16, 20)
        for level_key in ['1', '4', '7', '10', '13', '16', '20']:
            if level_key not in talents_data:
                continue
            for talent in talents_data[level_key]:
                talent_name = talent.get('name', '')
                key = (level_key, talent_name)
                
                # Verificar se talento tem alteracao no patch notes
                if key not in patch_changes:
                    continue
                
                change_data = patch_changes[key]
                
                # Adicionar developerCommentary se existir e nao estiver vazio
                dev_comm = change_data.get('developerCommentary', '')
                if dev_comm and dev_comm.strip():
                    talent['developerCommentary'] = dev_comm
                    updated = True
                
                # Adicionar subtexts se existirem
                subtexts = change_data.get('subtexts', [])
                if subtexts:
                    talent['subtexts'] = subtexts
                    updated = True
                
                # Atualizar descricao com textos principais se existirem
                texts = change_data.get('texts', [])
                if texts:
                    new_desc = '\n\n'.join(texts)
                    if new_desc.strip():
                        talent['description'] = new_desc
                        updated = True
                
                # Marcar como alterado se foi atualizado
                if dev_comm.strip() or subtexts or texts:
                    talent['talentChanged'] = True
        
        # Processar abilities (basic, heroic, trait)
        abilities = talents_data.get('abilities', {})
        
        # Basic abilities
        for ability in abilities.get('basic', []):
            ability_name = ability.get('name', '')
            # Procurar em general changes
            for patch in patch_data.get('patchNotes', []):
                for change in patch.get('general', []):
                    change_name = change.get('change', '')
                    if change_name and ability_name and change_name in ability_name:
                        dev_comm = change.get('developerCommentary', '')
                        if dev_comm and dev_comm.strip():
                            ability['developerCommentary'] = dev_comm
                            ability['abilityChanged'] = True
                            updated = True
                        texts = change.get('texts', [])
                        if texts:
                            main_texts = []
                            for t in texts:
                                if isinstance(t, dict) and t.get('text'):
                                    main_texts.append(t['text'])
                            if main_texts:
                                ability['description'] = '\n\n'.join(main_texts)
                                updated = True
        
        # Heroic abilities
        for ability in abilities.get('heroic', []):
            ability_name = ability.get('name', '')
            for patch in patch_data.get('patchNotes', []):
                for change in patch.get('general', []):
                    change_name = change.get('change', '')
                    if change_name and ability_name and change_name in ability_name:
                        dev_comm = change.get('developerCommentary', '')
                        if dev_comm and dev_comm.strip():
                            ability['developerCommentary'] = dev_comm
                            ability['abilityChanged'] = True
                            updated = True
        
        # Trait
        trait = abilities.get('trait', {})
        if trait:
            trait_name = trait.get('name', '')
            for patch in patch_data.get('patchNotes', []):
                for change in patch.get('general', []):
                    change_name = change.get('change', '')
                    if change_name and trait_name and change_name in trait_name:
                        dev_comm = change.get('developerCommentary', '')
                        if dev_comm and dev_comm.strip():
                            trait['developerCommentary'] = dev_comm
                            trait['abilityChanged'] = True
                            updated = True
        
        # Salvar arquivo atualizado
        if updated:
            with open(talents_file, 'w', encoding='utf-8') as f:
                json.dump(talents_data, f, indent=2, ensure_ascii=False)
            results.append(f"[OK] {hero}: Atualizado com sucesso")
        else:
            results.append(f"[--] {hero}: Nenhuma alteracao necessaria")
            
    except Exception as e:
        results.append(f"[ERRO] {hero}: Erro - {str(e)}")

# Imprimir resultados
for r in results:
    print(r)
