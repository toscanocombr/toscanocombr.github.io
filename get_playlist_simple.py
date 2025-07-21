#!/usr/bin/env python3
"""
Script simples para extrair vídeos de uma playlist do YouTube
Usa apenas bibliotecas padrão do Python (sem dependências externas)
"""

import requests
import re
import json
from urllib.parse import urlparse, parse_qs

def extract_playlist_id(url):
    """Extrai o ID da playlist de uma URL do YouTube"""
    parsed_url = urlparse(url)
    if 'list' in parse_qs(parsed_url.query):
        return parse_qs(parsed_url.query)['list'][0]
    return None

def get_playlist_videos_simple(playlist_url):
    """Extrai vídeos usando scraping simples da página"""
    
    try:
        # Faz request para a página da playlist
        response = requests.get(playlist_url)
        response.raise_for_status()
        
        html_content = response.text
        
        # Regex para encontrar dados dos vídeos no JavaScript da página
        # Procura por padrões como "videoId":"ABC123" e "title":{"runs":[{"text":"Título"}]}
        video_pattern = r'"videoId":"([^"]+)"'
        title_pattern = r'"title":{"runs":\[{"text":"([^"]+)"}'
        
        video_ids = re.findall(video_pattern, html_content)
        titles = re.findall(title_pattern, html_content)
        
        # Remove duplicatas mantendo a ordem
        unique_videos = []
        seen_ids = set()
        
        for i, video_id in enumerate(video_ids):
            if video_id not in seen_ids and len(video_id) == 11:  # IDs do YouTube têm 11 caracteres
                seen_ids.add(video_id)
                title = titles[i] if i < len(titles) else f"Vídeo {len(unique_videos) + 1}"
                
                # Limpa o título de caracteres especiais
                clean_title = re.sub(r'[<>"&\\]', '', title)
                
                unique_videos.append({
                    'id': video_id,
                    'title': clean_title,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                })
        
        return unique_videos[:20]  # Limita a 20 vídeos
        
    except Exception as e:
        print(f"Erro ao extrair playlist: {e}")
        return []

def generate_html_thumbnails(videos):
    """Gera o HTML dos thumbnails"""
    html_parts = []
    
    for video in videos:
        html_parts.append(f'''                    <div class="thumbnail-item" data-video-id="{video['id']}">
                        <img src="{video['thumbnail']}" alt="{video['title']}">
                        <span class="video-title">{video['title']}</span>
                    </div>''')
    
    return '\n'.join(html_parts)

def main():
    """Função principal"""
    
    playlist_url = "https://www.youtube.com/playlist?list=PLF1g1khsB5hgXQL_nbjK4deFEZ2JAD08F"
    
    print("🎬 Extraindo vídeos da playlist...")
    print(f"URL: {playlist_url}")
    print("=" * 50)
    
    videos = get_playlist_videos_simple(playlist_url)
    
    if videos:
        print(f"✅ {len(videos)} vídeos encontrados:")
        
        for i, video in enumerate(videos, 1):
            print(f"{i:2d}. {video['title']}")
        
        # Gera HTML
        html_content = generate_html_thumbnails(videos)
        
        # Salva em arquivo
        with open('thumbnails.html', 'w', encoding='utf-8') as f:
            f.write("<!-- Cole este código dentro da div 'thumbnails-grid' no seu index.html -->\n")
            f.write(html_content)
        
        # Salva JSON
        with open('playlist_data.json', 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Arquivos gerados:")
        print("- thumbnails.html (HTML pronto para usar)")
        print("- playlist_data.json (dados em JSON)")
        
        print(f"\n📋 Copie o conteúdo de 'thumbnails.html' e cole no seu index.html")
        
    else:
        print("❌ Nenhum vídeo encontrado. Tente o script com yt-dlp.")

if __name__ == "__main__":
    main()