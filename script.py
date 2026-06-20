import feedparser
from bs4 import BeautifulSoup
import requests
import re
import time
from urllib.parse import urljoin

url_feed = "https://www.blogger.com/feeds/6225118166347581914/posts/default"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Referer": "https://www.google.com/"
}

print("Buscando feed do Blogger...")
feed = feedparser.parse(url_feed)
streams_encontradas = []

print(f"Total de canais: {len(feed.entries)}\n")

def varrer_html_profundo(url_atual, html_conteudo, tentativa=1):
    """Varre o HTML recursivamente procurando por m3u8 ou sub-iframes"""
    if tentativa > 3:
        return None

    padrao_m3u8 = re.compile(r'(https?://[^\s<>"\']+\.m3u8[^\s<>"\']*)', re.IGNORECASE)
    matches = padrao_m3u8.findall(html_conteudo)
    
    if matches:
        for link in list(set(matches)):
            link_limpo = link.replace('\\/', '/')
            if not any(ext in link_limpo.lower() for ext in ['.js', '.css', '.png', '.jpg']):
                return link_limpo

    id_jmv = re.search(r'[\'"](LVW-\d+)[\'"]', html_conteudo)
    if id_jmv:
        id_canal = id_jmv.group(1)
        token_secundario = re.search(r'[\'"]([A-Za-vector7a-zA-Z0-9_]{10,25})[\'"]', html_conteudo)
        sufixo = token_secundario.group(1) if token_secundario else f"{id_canal.replace('-', '')}_513N26MDBL"
        return f"https://cdn.live.br1.jmvstream.com/w/{id_canal}/{sufixo}/playlist.m3u8"

    soup = BeautifulSoup(html_conteudo, 'html.parser')
    iframes = [ifrm.get('src') for ifrm in soup.find_all('iframe') if ifrm.get('src')]
    
    for ifr_url in iframes:
        ifr_url_completa = urljoin(url_atual, ifr_url)
        if "blogger.com" in ifr_url_completa or "disqus" in ifr_url_completa:
            continue
            
        try:
            sub_res = requests.get(ifr_url_completa, headers={**headers, "Referer": url_atual}, timeout=8)
            if sub_res.status_code == 200:
                resultado = varrer_html_profundo(ifr_url_completa, sub_res.text, tentativa + 1)
                if resultado:
                    return resultado
        except:
            pass
            
    return None

for entry in feed.entries:
    titulo = entry.title
    print(f"Analisando: {titulo}")
    
    conteudo_html = entry.content[0].value if 'content' in entry else entry.summary
    soup_feed = BeautifulSoup(conteudo_html, 'html.parser')
    
    # === EXTRAÇÃO DA LOGO DO CANAL ===
    logo_url = ""
    img_tag = soup_feed.find('img')
    if img_tag and img_tag.get('src'):
        logo_url = img_tag.get('src')
    
    link_alvo = None
    for tag in soup_feed.find_all('a'):
        href = tag.get('href')
        if href and "olhosnatv.com.br" in href:
            link_alvo = href
            break
            
    if not link_alvo and 'link' in entry:
        link_alvo = entry.link

    if link_alvo:
        try:
            res = requests.get(link_alvo, headers=headers, timeout=12)
            if res.status_code == 200:
                stream_link = varrer_html_profundo(link_alvo, res.text)
                
                if stream_link:
                    print(f"  [!] Encontrado Link + Logo: {logo_url[:50]}...")
                    # Salva uma tupla contendo (Título, URL da Stream, URL da Logo)
                    streams_encontradas.append((titulo, stream_link, logo_url))
                else:
                    print("  [?] Stream oculta por barreira de script complexa.")
        except Exception as e:
            print("  [Erro] Falha de conexão.")
            
        time.sleep(0.5)
    print("-" * 45)

# Exportação para arquivo M3U formatado com as logos
if streams_encontradas:
    nome_arquivo = "lista_canais_com_logos.m3u"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for t, s, logo in streams_encontradas:
            # Se encontrou a logo, adiciona a tag tvg-logo para o player renderizar
            if logo:
                f.write(f'#EXTINF:-1 tvg-logo="{logo}",{t}\n{s}\n')
            else:
                f.write(f'#EXTINF:-1,{t}\n{s}\n')
    print(f"\n[Fim] Lista gerada perfeitamente em '{nome_arquivo}' com as logos inclusas!")
else:
    print("\nNenhuma stream pôde ser extraída.")
