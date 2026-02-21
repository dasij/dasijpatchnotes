"""
Mockup da tela de Dragon Shire em 1920x1600px
"""
from PIL import Image, ImageDraw, ImageFont

def create_mockup():
    # Dimensões da tela
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1600
    SIDEBAR_WIDTH = 280
    
    # Criar imagem base (fundo escuro)
    img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), '#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Criar um gradiente de fundo similar ao do jogo
    for y in range(SCREEN_HEIGHT):
        # Gradiente de azul escuro para roxo escuro
        r = int(26 + (y / SCREEN_HEIGHT) * 20)
        g = int(26 + (y / SCREEN_HEIGHT) * 10)
        b = int(46 + (y / SCREEN_HEIGHT) * 20)
        draw.line([(0, y), (SCREEN_WIDTH, y)], fill=(r, g, b))
    
    # ========== SIDEBAR (lado esquerdo) ==========
    # Fundo da sidebar (preto semi-transparente)
    sidebar_overlay = Image.new('RGBA', (SIDEBAR_WIDTH, SCREEN_HEIGHT), (0, 0, 0, 217))
    img.paste(Image.blend(Image.new('RGBA', (SIDEBAR_WIDTH, SCREEN_HEIGHT), (0, 0, 0, 0)), 
                          sidebar_overlay, 0.85).convert('RGB'), (0, 0))
    
    # Recriar draw após o paste
    draw = ImageDraw.Draw(img)
    
    # Tabs na parte superior da sidebar
    tabs = ['Heroes', 'Maps', 'General', 'Modes']
    tab_width = SIDEBAR_WIDTH // 4
    tab_height = 70
    
    for i, tab in enumerate(tabs):
        x1 = i * tab_width
        x2 = (i + 1) * tab_width
        
        # Tab ativa (Maps) tem destaque
        if tab == 'Maps':
            draw.rectangle([x1, 0, x2, tab_height], fill=(116, 42, 255, 77))
            draw.line([x1, tab_height-2, x2, tab_height-2], fill='#742aff', width=3)
        else:
            draw.rectangle([x1, 0, x2, tab_height], fill=(0, 0, 0, 127))
        
        # Separador entre tabs
        if i > 0:
            draw.line([x1, 5, x1, tab_height-5], fill='#333', width=1)
    
    # Área de conteúdo da sidebar (lista de mapas)
    sidebar_content_y = tab_height + 10
    
    # Título da seção
    draw.text((20, sidebar_content_y), 'MAPS', fill='#888888')
    sidebar_content_y += 40
    
    # Lista de mapas (simplificada - alguns exemplos)
    maps_list = [
        ('ALTERAC PASS', False),
        ('BLACKHEART\'S BAY', False),
        ('BATTLEFIELD OF ETERNITY', False),
        ('BRAXIS HOLDOUT', False),
        ('CURSED HOLLOW', False),
        ('DRAGON SHIRE', True),  # Este está selecionado!
        ('GARDEN OF TERROR', False),
        ('HANAMURA TEMPLE', False),
        ('INFERNAL SHRINES', False),
        ('SKY TEMPLE', False),
    ]
    
    map_item_height = 60
    for map_name, is_selected in maps_list:
        y_pos = sidebar_content_y
        
        if is_selected:
            # Fundo destacado para o mapa selecionado
            draw.rectangle([10, y_pos, SIDEBAR_WIDTH-10, y_pos + map_item_height], 
                          fill=(116, 42, 255, 51), outline='#742aff', width=2)
            text_color = '#ffffff'
        else:
            draw.rectangle([10, y_pos, SIDEBAR_WIDTH-10, y_pos + map_item_height], 
                          fill=(255, 255, 255, 8))
            text_color = '#aaaaaa'
        
        # Nome do mapa
        draw.text((20, y_pos + 20), map_name, fill=text_color)
        
        sidebar_content_y += map_item_height + 8
    
    # Botão Hide na parte inferior da sidebar
    hide_btn_y = SCREEN_HEIGHT - 50
    draw.rectangle([0, hide_btn_y, SIDEBAR_WIDTH, SCREEN_HEIGHT], 
                  fill=(20, 20, 20, 242))
    draw.line([0, hide_btn_y, SIDEBAR_WIDTH, hide_btn_y], fill='#333333', width=2)
    draw.text((SIDEBAR_WIDTH//2 - 30, hide_btn_y + 15), '◀  Hide', fill='#888888')
    
    # Borda direita da sidebar
    draw.line([SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT], fill='#333333', width=2)
    
    # ========== CONTEÚDO PRINCIPAL ==========
    content_x = SIDEBAR_WIDTH + 40
    content_width = SCREEN_WIDTH - SIDEBAR_WIDTH - 80
    
    # Container principal (card escuro semi-transparente)
    container_padding = 30
    container_x1 = content_x
    container_y1 = 40
    container_x2 = content_x + content_width
    container_y2 = SCREEN_HEIGHT - 40
    
    # Fundo do container com transparência
    container_overlay = Image.new('RGBA', (content_width, SCREEN_HEIGHT - 80), (0, 0, 0, 178))
    img.paste(Image.blend(Image.new('RGBA', (content_width, SCREEN_HEIGHT - 80), (0, 0, 0, 0)), 
                          container_overlay, 0.7).convert('RGB'), 
              (container_x1, container_y1))
    
    # Bordas arredondadas do container
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([container_x1, container_y1, container_x2, container_y2], 
                          radius=12, outline='#444444', width=1)
    
    # Título da página
    title_y = container_y1 + 30
    # Tentar usar fonte maior se disponível, senão usar default
    draw.text((container_x1 + container_padding, title_y), 
              'DRAGON SHIRE PATCH NOTES', fill='#ffffff')
    
    # Linha divisória abaixo do título
    draw.line([container_x1 + container_padding, title_y + 50, 
               container_x2 - container_padding, title_y + 50], fill='#333333', width=1)
    
    # ========== CONTEÚDO DO PATCH NOTE ==========
    patch_y = title_y + 80
    
    # Título do patch
    draw.text((container_x1 + container_padding, patch_y), 
              'Small map changes', fill='#ffffff')
    patch_y += 40
    
    # Data
    draw.text((container_x1 + container_padding, patch_y), 
              '2024-05-14', fill='#888888')
    patch_y += 50
    
    # Developer Commentary Box
    commentary_box_x1 = container_x1 + container_padding
    commentary_box_y1 = patch_y
    commentary_box_x2 = container_x2 - container_padding
    commentary_box_y2 = patch_y + 120
    
    draw.rectangle([commentary_box_x1, commentary_box_y1, commentary_box_x2, commentary_box_y2],
                  fill=(116, 42, 255, 25))
    draw.line([commentary_box_x1, commentary_box_y1, commentary_box_x1, commentary_box_y2], 
              fill='#742aff', width=4)
    
    draw.text((commentary_box_x1 + 15, commentary_box_y1 + 15), 
              'Developer Comment:', fill='#ffffff')
    draw.text((commentary_box_x1 + 15, commentary_box_y1 + 45), 
              'These changes are aimed at encouraging players to use this paths', fill='#cccccc')
    draw.text((commentary_box_x1 + 15, commentary_box_y1 + 70), 
              'more by remembering them that they exist, most of these corners', fill='#cccccc')
    draw.text((commentary_box_x1 + 15, commentary_box_y1 + 95), 
              'are almost never used so rewarding players for going there is my goal.', fill='#cccccc')
    
    patch_y = commentary_box_y2 + 30
    
    # General Changes Section
    draw.text((container_x1 + container_padding, patch_y), 
              'General Changes', fill='#9900ff')
    patch_y += 50
    
    # Change title
    draw.text((container_x1 + container_padding + 20, patch_y), 
              '• New globes spawner', fill='#0099ff')
    patch_y += 40
    
    # Lista de mudanças
    changes = [
        'Additional globes spawn have been added on corners of the map that will be mirrored.',
        'This globes will spawn between 30-55 seconds(random) on this positions and will have',
        'no warning that they spawned',
        '',
        'Globe 1 on the path between top and middle lane.'
    ]
    
    for change in changes:
        if change:
            draw.text((container_x1 + container_padding + 40, patch_y), 
                      f'• {change}', fill='#ccc8d3')
        patch_y += 30
    
    # Placeholder para a imagem do globe
    img_x = container_x1 + container_padding + 40
    img_y = patch_y + 20
    img_width = 400
    img_height = 225
    
    draw.rounded_rectangle([img_x, img_y, img_x + img_width, img_y + img_height], 
                          radius=20, fill=(0, 0, 0, 127), outline='#742aff', width=4)
    draw.text((img_x + img_width//2 - 80, img_y + img_height//2 - 10), 
              '[Imagem: globe_1.jpg]', fill='#888888')
    draw.text((img_x + img_width//2 - 60, img_y + img_height//2 + 20), 
              'Globe Location', fill='#666666')
    
    # Salvar imagem
    output_path = 'dragon_shire_mockup_1920x1600.png'
    img.save(output_path, 'PNG')
    print(f'Mockup criado: {output_path}')
    print(f'Dimensões: {SCREEN_WIDTH}x{SCREEN_HEIGHT}px')
    
    return output_path

if __name__ == '__main__':
    create_mockup()
