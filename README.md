# YT-DLP-GG 🐍🎬

Uma interface gráfica moderna e amigável para o poderoso **yt-dlp**, desenvolvida em Python com **PySide6**.  
Baixe vídeos do YouTube, Vimeo e **mais de 1000 sites** com facilidade, sem precisar usar a linha de comando.

---

## ✨ Funcionalidades

- **🚀 Modos de Download**  
  Vídeo (MP4/MKV), Áudio (MP3/M4A/WAV) e Playlists completas.

- **🎛️ Controle de Qualidade**  
  Selecione resolução (1080p, 720p, 4K) e bitrate de áudio (320kbps).

- **🍪 Suporte a Cookies (Anti-restrições)**  
  Contorne bloqueios de assinatura e restrições de idade usando arquivos `cookies.txt`.

- **📝 Nomes de Arquivos Inteligentes**  
  - Mantenha acentos e espaços originais (Padrão).
  - Ou use o **"Modo Seguro"** para substituir caracteres por `_`.

- **📑 Metadados**  
  Insira automaticamente título, capa (thumbnail) e informações no arquivo.

- **💻 Interface Nativa**  
  Desenvolvido com PySide6 (Qt), garantindo visual moderno e responsivo.

---

## 🛠️ Instalação

### Pré-requisitos

- **Python 3.8 ou superior** instalado.
- **FFmpeg** instalado e adicionado ao PATH do sistema (obrigatório para mesclar vídeo/áudio e converter formatos).

### Passo 1: Clone ou Baixe o Projeto

```bash
git clone https://github.com/atanycost-png/YT-DLP-GG.git
cd YT-DLP-GG
```

### Passo 2: Instale as Dependências

É recomendado usar um ambiente virtual (venv), mas não é obrigatório.

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Usar

1. Execute o arquivo principal:
   ```bash
   python YT-DLP-GG.py
   ```

2. Cole a URL do vídeo no campo de texto.

3. Selecione a Pasta de destino onde o arquivo será salvo.

4. (Opcional) **Cookies** – Se estiver baixando vídeos restritos (ex: YouTube Premium), clique em "Carregar Cookies" e selecione seu arquivo cookies.txt.
   - **Dica**: Use a extensão "Get cookies.txt LOCALLY" no seu navegador para exportar os cookies.

5. Escolha o Modo (Vídeo, Áudio ou Playlist) e configure as opções.

6. Clique em **INICIAR DOWNLOAD** e acompanhe o progresso no log.

---

## 📝 Resolvendo Problemas Comuns

### ❌ Erro: "FFmpeg not found"

O programa precisa do FFmpeg para funcionar corretamente (especialmente para converter para MP3 ou juntar vídeo e áudio).

**Solução:**
1. Baixe o FFmpeg do site oficial.
2. Extraia os arquivos.
3. Adicione a pasta bin do FFmpeg às variáveis de ambiente do Windows (PATH).

### ❌ Erro: "HTTP Error 403: Forbidden" ou "Sign in to confirm you're not a bot"

O YouTube está bloqueando o download anônimo.

**Solução:**
1. Faça login no YouTube no seu navegador.
2. Instale a extensão "Get cookies.txt LOCALLY" (Chrome ou Firefox).
3. Exporte o arquivo cookies.txt.
4. No programa, clique em "Carregar Cookies" e selecione esse arquivo.
5. Tente baixar novamente.

### ❌ Erro: "Nomes de Arquivo com Underline (_)"

Por padrão, o programa mantém acentos e espaços.  
Se você estiver vendo underlines, verifique se a opção "Modo Seguro" está desmarcada nas Opções Globais.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir Issues ou Pull Requests.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT – veja o arquivo LICENSE para detalhes.

---

## 🙏 Créditos

- **yt-dlp** – O motor de download backend.
- **PySide6** – O framework de interface gráfica.
- ✨ Projeto mantido com ❤️ para facilitar downloads de mídia de forma acessível e poderosa.
