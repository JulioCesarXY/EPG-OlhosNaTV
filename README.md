# 📺 EPG-OlhosNaTV

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/JulioCesarXY/EPG-OlhosNaTV/atualizar_lista.yml?branch=main&style=flat-square&label=Atualiza%C3%A7%C3%A3o%20Autom%C3%A1tica&color=success)
![GitHub last commit](https://img.shields.io/github/last-commit/JulioCesarXY/EPG-OlhosNaTV?style=flat-square&label=%C3%9Altimos%20Canais&color=blue)

Automação inteligente desenvolvida em Python e executada via GitHub Actions para realizar engenharia reversa, extração profunda de streams dinâmicas e sincronização de logos do feed indexador do Blogger.

---

### 🚀 Como usar no seu Player (VLC, IPTV Smarters, etc.)

Para carregar os canais sempre atualizados diretamente no seu aplicativo de IPTV ou player de vídeo, utilize o link direto (**Raw**) abaixo:

```text
https://raw.githubusercontent.com/JulioCesarXY/EPG-OlhosNaTV/main/lista_canais_com_logos.m3u

````
### 🛠️ Como Funciona a Tecnologia do Repositório
O ecossistema é dividido em três camadas principais operando de forma 100% autônoma:

1. Raspagem Avançada (Python)
Parser de Feed: Varre de forma otimizada o feed Atom/RSS do Blogger coletando os metadados e títulos das postagens.

Varredura Recursiva Profunda: O script simula um navegador mobile real e navega de forma automatizada por até 3 níveis de iframes internos das páginas de destino.

Descoberta Dinâmica: Captura endpoints .m3u8 escondidos em blocos complexos de JavaScript e reconstrói de forma cirúrgica os tokens de rota da JMV Stream e NuvemPlay.

Mapeamento de Identidade: Vincula a logo oficial (tvg-logo) hospedada nos servidores do Google diretamente à tag correspondente do canal na lista M3U.

2. Automação Agendada (GitHub Actions)
O arquivo de configuração em .github/workflows/atualizar_lista.yml acorda um servidor virtual Ubuntu de 12 em 12 horas.

O ambiente monta o interpretador Python, resolve as dependências do script, atualiza a lista e faz um commit automático de volta ao repositório apenas se houver novos canais ou links alterados.

### ⚙️ Estrutura do Projeto

```text
EPG-OlhosNaTV/
├── .github/
│   └── workflows/
│       └── atualizar_lista.yml   # Motor da automação (GitHub Actions)
├── script.py                     # Script Python de engenharia reversa 
└── lista_canais_com_logos.m3u    # Arquivo M3U gerado final (Link Raw)
```


### 📝 Requisitos para Rodar Localmente
Se quiser clonar e testar o script em sua máquina ou celular (via Pydroid 3), instale as seguintes dependências:

Bash
pip install feedparser beautifulsoup4 requests
Para rodar o coletor manual:

Bash
python script.py
⭐ Se este projeto te ajudou a manter suas streams atualizadas, considere deixar uma estrela neste repositório!


---

### 💡 Dicas de Ajuste antes de Salvar:
1. Pressione `Ctrl + F` (ou use a busca) no seu editor e substitua todas as ocorrências de **`SEU_USUARIO`** pelo seu nome de perfil do GitHub para que os links e os badges de status funcionem perfeitamente.
2. Caso o nome do seu arquivo workflow não seja exatamente `atualizar_lista.yml`, ajuste a linha 3 do código para o nome correto do seu arquivo.
