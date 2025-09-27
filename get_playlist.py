#!/usr/bin/env python3
"""
Script para extrair vídeos de uma playlist do YouTube
Instale as dependências: pip install yt-dlp requests
"""

import yt_dlp
import json
import re
from urllib.parse import urlparse, parse_qs

def extract_playlist_id(url):
    """Extrai o ID da playlist de uma URL do YouTube"""
    parsed_url = urlparse(url)
    if 'list' in parse_qs(parsed_url.query):
        return parse_qs(parsed_url.query)['list'][0]
    return None

def get_playlist_videos(playlist_url):
    """Extrai informações dos vídeos de uma playlist"""
    
    # Configurações do yt-dlp
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Não baixa, apenas extrai metadados
        'playlistend': 50,     # Limita a 50 vídeos (ajuste conforme necessário)
    }
    
    videos = []
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extrai informações da playlist
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            print(f"Playlist: {playlist_info.get('title', 'Sem título')}")
            print(f"Total de vídeos: {len(playlist_info.get('entries', []))}")
            print("-" * 50)
            
            # Processa cada vídeo
            for entry in playlist_info.get('entries', []):
                if entry:
                    video_id = entry.get('id')
                    title = entry.get('title', 'Sem título')
                    
                    # Remove caracteres especiais do título para uso em HTML
                    clean_title = re.sub(r'[<>"&]', '', title)
                    
                    video_info = {
                        'id': video_id,
                        'title': clean_title,
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'thumbnail': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                    }
                    
                    videos.append(video_info)
                    print(f"✓ {clean_title}")
            
    except Exception as e:
        print(f"Erro ao extrair playlist: {e}")
        return []
    
    return videos

def generate_html_thumbnails(videos):
    """Gera o HTML dos thumbnails para inserir no index.html"""
    
    html_parts = []
    
    for i, video in enumerate(videos):
        html_parts.append(f'''                    <div class="thumbnail-item" data-video-id="{video['id']}">
                        <img src="{video['thumbnail']}" alt="{video['title']}">
                        <span class="video-title">{video['title']}</span>
                    </div>''')
    
    return '\n'.join(html_parts)

def save_to_files(videos, playlist_url):
    """Salva os resultados em arquivos"""
    
    # Salva JSON com todos os dados
    with open('playlist_videos.json', 'w', encoding='utf-8') as f:
        json.dump({
            'playlist_url': playlist_url,
            'total_videos': len(videos),
            'videos': videos
        }, f, indent=2, ensure_ascii=False)
    
    # Gera HTML dos thumbnails
    html_thumbnails = generate_html_thumbnails(videos)
    
    # Salva HTML para copiar e colar
    with open('thumbnails.html', 'w', encoding='utf-8') as f:
        f.write("<!-- Cole este código dentro da div 'thumbnails-grid' no seu index.html -->\n")
        f.write(html_thumbnails)
    
    print(f"\n✅ Arquivos salvos:")
    print("📄 playlist_videos.json - Dados completos em JSON")
    print("📄 thumbnails.html - HTML pronto para usar")

def main():
    """Função principal"""
    
    # URL da sua playlist
    playlist_url = "https://www.youtube.com/playlist?list=PLF1g1khsB5hgXQL_nbjK4deFEZ2JAD08F"
    
    print("🎬 Extraindo vídeos da playlist do YouTube...")
    print(f"URL: {playlist_url}")
    print("=" * 60)
    
    # Extrai os vídeos
    videos = get_playlist_videos(playlist_url)
    
    if videos:
        # Salva os resultados
        save_to_files(videos, playlist_url)
        
        print(f"\n🎉 Sucesso! {len(videos)} vídeos extraídos.")
        print("\n📋 Próximos passos:")
        print("1. Copie o conteúdo de 'thumbnails.html'")
        print("2. Cole dentro da div 'thumbnails-grid' no seu index.html")
        print("3. Substitua os comentários de exemplo")
        
    else:
        print("❌ Nenhum vídeo foi extraído. Verifique a URL da playlist.")

if __name__ == "__main__":
    main()