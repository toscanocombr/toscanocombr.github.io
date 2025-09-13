#!/usr/bin/env python3
"""
Script para extrair vídeos de uma playlist do YouTube
Usa apenas bibliotecas padrão do Python (urllib, re, json)
"""

import urllib.request
import urllib.parse
import re
import json

def get_playlist_videos(playlist_url):
    """Extrai vídeos da playlist usando apenas bibliotecas padrão"""
    
    try:
        # Headers para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Cria request com headers
        req = urllib.request.Request(playlist_url, headers=headers)
        
        # Faz o request
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        # Regex para encontrar dados dos vídeos
        video_pattern = r'"videoId":"([A-Za-z0-9_-]{11})"'
        title_pattern = r'"title":{"runs":\[{"text":"([^"]+)"}'
        # Padrões mais específicos para capturar títulos completos
        title_pattern2 = r'"title":"([^"]+)"'
        views_pattern = r'"viewCountText":{"simpleText":"([^"]+)"}'
        
        video_ids = re.findall(video_pattern, html_content)
        titles = re.findall(title_pattern, html_content)
        
        # Remove duplicatas e cria lista de vídeos
        videos = []
        seen_ids = set()
        
        for i, video_id in enumerate(video_ids):
            if video_id not in seen_ids:
                seen_ids.add(video_id)
                
                # Pega o título correspondente ou usa um padrão
                if i < len(titles):
                    title = titles[i]
                else:
                    title = f"Vídeo {len(videos) + 1}"
                
                # Limpa caracteres especiais do título
                clean_title = re.sub(r'[<>"&\\]', '', title)
                clean_title = clean_title.replace('\\u0026', '&')  # Decodifica &
                
                video_info = {
                    'id': video_id,
                    'title': clean_title,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                }
                
                videos.append(video_info)
        
        return videos[:25]  # Limita a 25 vídeos
        
    except Exception as e:
        print(f"Erro ao extrair playlist: {e}")
        return []

def generate_html_thumbnails(videos):
    """Gera HTML dos thumbnails"""
    html_parts = []
    
    for video in videos:
        html_parts.append(f'''                    <div class="thumbnail-item" data-video-id="{video['id']}">
                        <img src="{video['thumbnail']}" alt="{video['title']}">
                        <span class="video-title">{video['title']}</span>
                    </div>''')
    
    return '\n'.join(html_parts)

def save_files(videos):
    """Salva os arquivos de saída"""
    
    # HTML dos thumbnails
    html_content = generate_html_thumbnails(videos)
    with open('thumbnails.html', 'w', encoding='utf-8') as f:
        f.write("<!-- Cole este código dentro da div 'thumbnails-grid' no seu index.html -->\n")
        f.write(html_content)
    
    # JSON com os dados
    with open('playlist_data.json', 'w', encoding='utf-8') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    
    # Instrucões
    with open('INSTRUCOES.txt', 'w', encoding='utf-8') as f:
        f.write("COMO USAR OS ARQUIVOS GERADOS:\n")
        f.write("=" * 40 + "\n\n")
        f.write("1. Abra o arquivo 'thumbnails.html'\n")
        f.write("2. Copie todo o conteúdo\n")
        f.write("3. No seu index.html, encontre a linha com:\n")
        f.write("   <!-- Adicione seus vídeos aqui seguindo este formato: -->\n")
        f.write("4. Substitua os comentários de exemplo pelo conteúdo copiado\n")
        f.write("5. Salve e teste o site\n\n")
        f.write("ARQUIVOS GERADOS:\n")
        f.write("- thumbnails.html: HTML pronto para usar\n")
        f.write("- playlist_data.json: Dados em formato JSON\n")
        f.write(f"- Total de {len(videos)} vídeos extraídos\n")

def main():
    """Função principal"""
    
    playlist_url = "https://www.youtube.com/playlist?list=PLF1g1khsB5hgXQL_nbjK4deFEZ2JAD08F"
    
    print("🎬 Extraindo vídeos da playlist do YouTube...")
    print(f"URL: {playlist_url}")
    print("=" * 60)
    
    videos = get_playlist_videos(playlist_url)
    
    if videos:
        print(f"✅ {len(videos)} vídeos encontrados:\n")
        
        for i, video in enumerate(videos, 1):
            print(f"{i:2d}. {video['title'][:50]}{'...' if len(video['title']) > 50 else ''}")
        
        save_files(videos)
        
        print(f"\n📄 Arquivos gerados:")
        print("✓ thumbnails.html")
        print("✓ playlist_data.json") 
        print("✓ INSTRUCOES.txt")
        
        print(f"\n🎉 Sucesso! Agora você pode:")
        print("1. Abrir thumbnails.html e copiar o conteúdo")
        print("2. Colar no seu index.html dentro da 'thumbnails-grid'")
        
    else:
        print("❌ Nenhum vídeo foi extraído.")
        print("💡 Dicas:")
        print("- Verifique se a playlist é pública")
        print("- Tente executar novamente")
        print("- Use o script com yt-dlp para melhor compatibilidade")

if __name__ == "__main__":
    main()