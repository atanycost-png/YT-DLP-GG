import sys
import os
import threading
import yt_dlp
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                 QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                                 QComboBox, QCheckBox, QTabWidget, QProgressBar, 
                                 QTextEdit, QFileDialog, QGroupBox, QSpinBox, QMessageBox)
from PySide6.QtCore import Qt, Signal, QObject

# --- SINAIS PARA THREAD (COMUNICAÇÃO ENTRE THREADS E GUI) ---
class WorkerSignals(QObject):
    progress = Signal(str, float) # mensagem, porcentagem
    log = Signal(str, str)         # mensagem, tipo (info, warning, error)
    finished = Signal()

# --- LÓGICA DE DOWNLOAD (DEFINITIVAMENTE CORRIGIDA) ---
class DownloadWorker(threading.Thread):
    def __init__(self, url, opts, signals):
        super().__init__()
        self.url = url
        self.opts = opts
        self.signals = signals

    def run(self):
        try:
            # Classe de Logger agora recebe 'signals' no init
            class YtLogger:
                def __init__(self, signals_ref):
                    self.signals = signals_ref

                def debug(self, msg): 
                    # Log silencioso para debug
                    pass 
                
                def warning(self, msg): 
                    self.signals.log.emit(f"AVISO: {msg}", "warning")
                
                def error(self, msg): 
                    self.signals.log.emit(f"ERRO: {msg}", "error")

            # Hook de progresso do yt-dlp
            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        pct = d.get('_percent_str', '0%').replace('%', '')
                        speed = d.get('_speed_str', 'N/A')
                        eta = d.get('_eta_str', 'N/A')
                        msg = f"{pct}% | {speed} | ETA: {eta}"
                        self.signals.progress.emit(msg, float(pct)/100)
                    except:
                        pass
                elif d['status'] == 'finished':
                    self.signals.log.emit("Download concluído. Processando conversão...", "info")

            # Instancia o logger passando self.signals
            logger_instance = YtLogger(self.signals)

            # Configurar opções finais
            self.opts['logger'] = logger_instance
            self.opts['progress_hooks'] = [progress_hook]

            # Executar download
            with yt_dlp.YoutubeDL(self.opts) as ydl:
                ydl.download([self.url])
            
            self.signals.log.emit("Processo finalizado com sucesso!", "success")
            self.signals.progress.emit("Concluído.", 1.0)

        except Exception as e:
            self.signals.log.emit(f"Falha no download: {str(e)}", "error")
        finally:
            self.signals.finished.emit()

# --- JANELA PRINCIPAL ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YT-DLP-GG Desktop v1.0 (PySide6)")
        self.resize(850, 700)
        
        # Estado
        self.cookies_path = ""
        self.output_folder = ""
        self.worker = None
        self.is_downloading = False

        # Setup Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.setup_ui()
        self.apply_dark_theme()

    def setup_ui(self):
        # 1. Header
        header_layout = QHBoxLayout()
        title_label = QLabel("YT-DLP-GG")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ef4444;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        version_label = QLabel("v1.0 Stable")
        version_label.setStyleSheet("color: #a1a1aa;")
        header_layout.addWidget(version_label)
        self.main_layout.addLayout(header_layout)

        # 2. URL Input
        url_group = QGroupBox("Fonte (URL)")
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole o link do YouTube aqui...")
        url_layout.addWidget(self.url_input)
        url_group.setLayout(url_layout)
        self.main_layout.addWidget(url_group)

        # 3. Paths (Output & Cookies)
        paths_layout = QHBoxLayout()
        
        # Output Folder
        out_group = QGroupBox("Pasta de Destino")
        out_layout = QHBoxLayout()
        self.output_display = QLineEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setPlaceholderText("Selecione onde salvar...")
        btn_out = QPushButton("Selecionar")
        btn_out.clicked.connect(self.select_output_folder)
        out_layout.addWidget(self.output_display)
        out_layout.addWidget(btn_out)
        out_group.setLayout(out_layout)
        paths_layout.addWidget(out_group)

        # Cookies
        cook_group = QGroupBox("Autenticação (Cookies)")
        cook_layout = QHBoxLayout()
        self.cookies_display = QLineEdit()
        self.cookies_display.setReadOnly(True)
        self.cookies_display.setPlaceholderText("Arquivo cookies.txt (Opcional)")
        btn_cook = QPushButton("Carregar")
        btn_cook.clicked.connect(self.select_cookies)
        cook_layout.addWidget(self.cookies_display)
        cook_layout.addWidget(btn_cook)
        cook_group.setLayout(cook_layout)
        paths_layout.addWidget(cook_group)
        
        self.main_layout.addLayout(paths_layout)

        # 4. Tabs (Video / Audio / Playlist)
        self.tabs = QTabWidget()
        self.tab_video = QWidget()
        self.tab_audio = QWidget()
        self.tab_playlist = QWidget()
        
        self.setup_video_tab()
        self.setup_audio_tab()
        self.setup_playlist_tab()
        
        self.tabs.addTab(self.tab_video, "Vídeo")
        self.tabs.addTab(self.tab_audio, "Áudio")
        self.tabs.addTab(self.tab_playlist, "Playlist")
        
        self.main_layout.addWidget(self.tabs)

        # 5. Opções Globais
        global_opts = QHBoxLayout()
        self.check_meta = QCheckBox("Inserir Metadados")
        self.check_meta.setChecked(True)
        self.check_restrict = QCheckBox("Modo Seguro (Underline _)")
        self.check_restrict.setToolTip("Marque para substituir espaços por underline.\nDesmarque para manter acentuação original.")
        global_opts.addWidget(self.check_meta)
        global_opts.addWidget(self.check_restrict)
        global_opts.addStretch()
        self.main_layout.addLayout(global_opts)

        # 6. Progresso e Botão
        progress_layout = QVBoxLayout()
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        self.status_label = QLabel("Aguardando...")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        progress_layout.addLayout(status_layout)

        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)

        self.btn_download = QPushButton("INICIAR DOWNLOAD")
        self.btn_download.setFixedHeight(40)
        self.btn_download.setStyleSheet("background-color: #3b82f6; color: white; font-weight: bold; font-size: 14px;")
        self.btn_download.clicked.connect(self.start_download)
        progress_layout.addWidget(self.btn_download)

        self.main_layout.addLayout(progress_layout)

        # 7. Log
        log_group = QGroupBox("Log de Execução")
        log_layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("font-family: Consolas, monospace; background-color: #000; color: #22c55e;")
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        self.main_layout.addWidget(log_group)

    def setup_video_tab(self):
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        
        row1.addWidget(QLabel("Qualidade:"))
        self.combo_video_quality = QComboBox()
        self.combo_video_quality.addItems(["Melhor (4K/1080)", "1080p", "720p", "Pior"])
        row1.addWidget(self.combo_video_quality)
        
        row1.addWidget(QLabel("Formato:"))
        self.combo_video_format = QComboBox()
        self.combo_video_format.addItems(["MP4", "MKV"])
        row1.addWidget(self.combo_video_format)
        
        layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        self.check_subs = QCheckBox("Baixar Legendas (.srt)")
        self.check_thumb = QCheckBox("Inserir Thumbnail")
        row2.addWidget(self.check_subs)
        row2.addWidget(self.check_thumb)
        row2.addStretch()
        layout.addLayout(row2)
        
        self.tab_video.setLayout(layout)

    def setup_audio_tab(self):
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        
        row1.addWidget(QLabel("Formato:"))
        self.combo_audio_format = QComboBox()
        self.combo_audio_format.addItems(["mp3", "m4a", "wav", "flac"])
        row1.addWidget(self.combo_audio_format)
        
        row1.addWidget(QLabel("Bitrate:"))
        self.combo_audio_bitrate = QComboBox()
        self.combo_audio_bitrate.addItems(["320", "192", "128"])
        row1.addWidget(self.combo_audio_bitrate)
        
        layout.addLayout(row1)
        layout.addStretch()
        self.tab_audio.setLayout(layout)

    def setup_playlist_tab(self):
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        
        row1.addWidget(QLabel("Início:"))
        self.spin_playlist_start = QSpinBox()
        self.spin_playlist_start.setMinimum(1)
        self.spin_playlist_start.setValue(1)
        row1.addWidget(self.spin_playlist_start)
        
        row1.addWidget(QLabel("Fim (0=Tudo):"))
        self.spin_playlist_end = QSpinBox()
        self.spin_playlist_end.setMinimum(0)
        self.spin_playlist_end.setValue(0)
        row1.addWidget(self.spin_playlist_end)
        
        layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Formato Saída:"))
        self.combo_playlist_format = QComboBox()
        self.combo_playlist_format.addItems(["MP4", "MP3"])
        row2.addWidget(self.combo_playlist_format)
        layout.addLayout(row2)
        
        layout.addStretch()
        self.tab_playlist.setLayout(layout)

    # --- LÓGICA ---
    def apply_dark_theme(self):
        # Estilo básico Dark Mode
        self.setStyleSheet("""
            QMainWindow { background-color: #0f0f0f; }
            QWidget { color: #ffffff; font-size: 14px; }
            QLineEdit, QComboBox, QSpinBox, QTextEdit { 
                background-color: #2d2d2d; 
                border: 1px solid #3f3f46; 
                padding: 5px; 
                border-radius: 4px;
            }
            QGroupBox { 
                border: 1px solid #3f3f46; 
                margin-top: 10px; 
                padding-top: 10px; 
                font-weight: bold;
            }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; }
            QPushButton { 
                background-color: #2d2d2d; 
                border: 1px solid #3f3f46; 
                padding: 8px; 
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #3f3f46; }
            QProgressBar { 
                border: 1px solid #3f3f46; 
                border-radius: 4px; 
                text-align: center; 
                background-color: #2d2d2d;
            }
            QProgressBar::chunk { background-color: #3b82f6; }
            QTabWidget::pane { border: 1px solid #3f3f46; }
            QTabBar::tab { 
                background: #1e1e1e; 
                color: #a1a1aa; 
                padding: 8px 16px; 
                margin-right: 2px; 
                border-top-left-radius: 4px; 
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected { 
                background: #2d2d2d; 
                color: #ffffff; 
                border-bottom: 2px solid #3b82f6;
            }
            QCheckBox { spacing: 5px; }
        """)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Destino")
        if folder:
            self.output_folder = folder
            self.output_display.setText(folder)

    def select_cookies(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo Cookies", "", "Arquivo de Texto (*.txt)")
        if file:
            self.cookies_path = file
            self.cookies_display.setText(file)
            self.log_output.append(f"<span style='color:#3b82f6'>Cookies carregados: {file}</span>")

    def start_download(self):
        if self.is_downloading:
            QMessageBox.warning(self, "Aviso", "Já existe um download em andamento.")
            return

        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Erro", "Por favor, insira uma URL.")
            return
        
        if not self.output_folder:
            QMessageBox.warning(self, "Erro", "Selecione uma pasta de destino.")
            return

        # Montar opções do yt-dlp
        opts = {
            'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
        }

        # Cookies
        if self.cookies_path:
            opts['cookiefile'] = self.cookies_path

        # Lógica de Nomes (Espaços vs Underline)
        if not self.check_restrict.isChecked():
            opts['no_clean_info'] = True # Mantém espaços/acentos
        else:
            opts['restrictfilenames'] = True # Modo seguro (underline)

        # Lógica por Aba
        tab_name = self.tabs.tabText(self.tabs.currentIndex())

        if tab_name == "Vídeo":
            qual = self.combo_video_quality.currentText()
            fmt = self.combo_video_format.currentText()

            fmt_str = 'bestvideo+bestaudio/best'
            if qual == "1080p": fmt_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            elif qual == "720p": fmt_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif qual == "Pior": fmt_str = 'worst'
            
            opts['format'] = fmt_str
            
            if fmt == "MP4": opts['merge_output_format'] = 'mp4'
            if fmt == "MKV": opts['merge_output_format'] = 'mkv'

            if self.check_subs.isChecked():
                opts['writesubtitles'] = True
                opts['writeautomaticsub'] = True
                opts['subtitleslangs'] = ['all']

        elif tab_name == "Áudio":
            ext = self.combo_audio_format.currentText()
            qual = self.combo_audio_bitrate.currentText()
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': ext.lower(),
                'preferredquality': qual,
            }]

        elif tab_name == "Playlist":
            start = self.spin_playlist_start.value()
            end = self.spin_playlist_end.value()
            if start > 0: opts['playliststart'] = start
            if end > 0: opts['playlistend'] = end
            
            opts['outtmpl'] = os.path.join(self.output_folder, '%(playlist_index)s - %(title)s.%(ext)s')
            
            if self.combo_playlist_format.currentText() == "MP3":
                opts['format'] = 'bestaudio/best'
                opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
            else:
                opts['format'] = 'bestvideo+bestaudio/best'

        # Opções Globais
        if self.check_meta.isChecked():
            opts['addmetadata'] = True
        if self.check_thumb.isChecked():
            opts['writethumbnail'] = True
            opts['embedthumbnail'] = True

        # Iniciar Thread
        self.is_downloading = True
        self.btn_download.setEnabled(False)
        self.btn_download.setText("Baixando...")
        self.log_output.append(f"<span style='color:#3b82f6'>Iniciando download de: {url}</span>")

        self.signals = WorkerSignals()
        self.signals.progress.connect(self.update_progress)
        self.signals.log.connect(self.update_log)
        self.signals.finished.connect(self.download_finished)

        self.worker = DownloadWorker(url, opts, self.signals)
        self.worker.start()

    def update_progress(self, msg, value):
        self.status_label.setText(msg)
        self.progress_bar.setValue(int(value * 100))

    def update_log(self, msg, type_str):
        color = "#ffffff"
        if type_str == "error": color = "#ef4444"
        elif type_str == "warning": color = "#facc15"
        elif type_str == "success": color = "#22c55e"
        elif type_str == "info": color = "#3b82f6"
        
        self.log_output.append(f"<span style='color:{color}'>{msg}</span>")
        # Auto scroll
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    def download_finished(self):
        self.is_downloading = False
        self.btn_download.setEnabled(True)
        self.btn_download.setText("INICIAR DOWNLOAD")
        self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())