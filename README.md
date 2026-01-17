# YT-DLP-GG 🐍🎬

Uma solução completa, moderna e amigável para o poderoso **yt-dlp**. Este projeto oferece duas formas de facilitar o download de vídeos, áudios e playlists de mais de 1000 sites.

---

## 🛠️ Duas Formas de Usar

O projeto YT-DLP-GG agora oferece duas interfaces distintas para atender a diferentes necessidades:

### 1. 🖥️ Interface Desktop (Nativa)
Uma aplicação completa desenvolvida em **Python** com **PySide6 (Qt)**. Ideal para quem deseja gerenciar downloads diretamente pelo computador sem lidar com o terminal.
- **Arquivo:** `YT-DLP-GG.py`
- **Requisitos:** Python instalado + FFmpeg.

### 2. 🌐 Interface Web (Gerador de Comandos)
Uma interface web moderna, minimalista e "dark mode" para gerar comandos complexos do yt-dlp visualmente. Perfeita para quem prefere usar o terminal mas não quer decorar todas as flags.
- **Arquivo:** `index.html` (Basta abrir no navegador)
- **Destaque:** Design premium atualizado com ícones Lucide e tipografia moderna.

---

## ✨ Funcionalidades Principais

- **🚀 Múltiplos Modos**
  Vídeo (MP4/MKV), Áudio (MP3/M4A/WAV) e Playlists completas.

- **🎛️ Controle de Qualidade**
  Selecione resoluções (1080p, 720p, 4K) e bitrates de áudio de alta qualidade.

- **🍪 Suporte a Cookies (Anti-SARS)**
  Contorne bloqueios de login e restrições de idade usando arquivos `cookies.txt`.

- **📝 Nomes de Arquivos Flexíveis**
  Suporte total a caracteres especiais, acentos e espaços, com opção de modo seguro (ASCII).

- **📑 Metadados e Thumbnails**
  Incrustação automática de capas, títulos e tags diretamente nos arquivos baixados.

---

## 🚀 Como Começar

### Pré-requisitos
- **Python 3.8+** (Para a versão Desktop).
- **FFmpeg** instalado e no PATH do sistema (Necessário para ambas as versões processarem mídia).

### Instalação (Versão Desktop)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/atanycost-png/YT-DLP-GG.git
   cd YT-DLP-GG
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute:**
   ```bash
   python YT-DLP-GG.py
   ```

### Uso da Versão Web

Basta abrir o arquivo `index.html` em qualquer navegador moderno. Configure as opções visualmente, copie o comando gerado e cole no seu terminal com o `yt-dlp` instalado.

---

## 📝 Solução de Problemas

### ❌ "FFmpeg not found"
O motor de download precisa do FFmpeg para converter formatos ou unir áudio e vídeo.
- **Windows:** Baixe o binário e adicione a pasta `bin` ao seu PATH.
- **Linux:** `sudo apt install ffmpeg`

### ❌ Vídeos Bloqueados (403 Forbidden)
O YouTube exige autenticação para certos vídeos.
1. Use a extensão **"Get cookies.txt LOCALLY"** no seu navegador.
2. Exporte os cookies do YouTube logado.
3. Carregue o `cookies.txt` na interface do YT-DLP-GG.

---

## 🤝 Contribuições

Sinta-se à vontade para abrir Issues ou enviar Pull Requests. Toda ajuda para melhorar a interface ou as funcionalidades é bem-vinda!

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.

---

## 🙏 Créditos

- **yt-dlp** – O motor de download fenomenal.
- **PySide6** – Framework para a interface desktop.
- **Lucide Icons** – Ícones modernos para a interface web.

---
✨ Mantido com ❤️ para tornar o download de mídias acessível a todos.
