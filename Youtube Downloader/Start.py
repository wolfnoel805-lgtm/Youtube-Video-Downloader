import os
import threading
import customtkinter as ctk
from customtkinter import filedialog
import yt_dlp

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ModernDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader by elyxnoel")
        self.geometry("580x440")
        self.resizable(False, False)
        self.configure(fg_color="#1a1c23")

        self.title_label = ctk.CTkLabel(self, text="elyxnoel", font=ctk.CTkFont(size=28, weight="bold"), text_color="#e2e8f0")
        self.title_label.pack(padx=20, pady=(20, 2))

        self.made_by_label = ctk.CTkLabel(self, text="made by elyxnoel", font=ctk.CTkFont(size=12, slant="italic"), text_color="#64748b")
        self.made_by_label.pack(padx=20, pady=(0, 10))

        self.sub_label = ctk.CTkLabel(self, text="Füge deinen Videolink hier unten ein", font=ctk.CTkFont(size=13), text_color="#94a3b8")
        self.sub_label.pack(padx=20, pady=(0, 15))

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(padx=30, pady=10, fill="x")

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="https://www.youtube.com/watch?v=...", height=40, font=ctk.CTkFont(size=13), fg_color="#2d313f", border_color="#475569", text_color="white")
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.paste_btn = ctk.CTkButton(self.input_frame, text="Einfügen", width=80, height=40, command=self.paste_link, font=ctk.CTkFont(weight="bold"), fg_color="#2563eb", hover_color="#1d4ed8")
        self.paste_btn.pack(side="right")

        self.download_button = ctk.CTkButton(self, text="DOWNLOAD", height=45, command=self.start_download_thread, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#10b981", hover_color="#059669")
        self.download_button.pack(padx=30, pady=15, fill="x")

        self.stats_frame = ctk.CTkFrame(self, fg_color="#212530", corner_radius=12)
        self.stats_frame.pack(padx=30, pady=15, fill="both", expand=True)

        self.title_info_label = ctk.CTkLabel(self.stats_frame, text="Bereit für Download...", font=ctk.CTkFont(size=13, weight="bold"), text_color="#cbd5e1", wraplength=500)
        self.title_info_label.pack(padx=20, pady=(15, 5), anchor="w")

        self.progress_bar = ctk.CTkProgressBar(self.stats_frame, height=10, progress_color="#3b82f6", fg_color="#475569")
        self.progress_bar.pack(padx=20, pady=10, fill="x")
        self.progress_bar.set(0)

        self.speed_time_label = ctk.CTkLabel(self.stats_frame, text="Geschwindigkeit: -- MB/s | Verbleibend: --s", font=ctk.CTkFont(size=12), text_color="#94a3b8")
        self.speed_time_label.pack(padx=20, pady=(0, 10), anchor="w")

        self.footer_label = ctk.CTkLabel(self, text="Status: Made by elyxnoel", font=ctk.CTkFont(size=11, slant="italic"), text_color="#64748b")
        self.footer_label.pack(side="bottom", pady=12)

    def paste_link(self):
        try:
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, self.clipboard_get())
        except:
            pass

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            
            if total > 0:
                percent = downloaded / total
                self.progress_bar.set(percent)
                percent_str = f"{int(percent * 100)}%"
            else:
                percent_str = "0%"

            filename = os.path.basename(d.get('filename', 'Video'))
            filename_clean = os.path.splitext(filename)[0]

            self.title_info_label.configure(text=f"Lädt herunter: \"{filename_clean}\" - {percent_str}")

            speed = d.get('_speed_str', '0B/s').strip()
            eta = d.get('_eta_str', '00:00').strip()
            self.speed_time_label.configure(text=f"Geschwindigkeit: {speed} | Verbleibend (ETA): {eta}")
            
        elif d['status'] == 'finished':
            self.progress_bar.set(1)
            self.title_info_label.configure(text="🎉 Download erfolgreich beendet!", text_color="#10b981")
            self.speed_time_label.configure(text="Datei wurde erfolgreich gespeichert.")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.title_info_label.configure(text="❌ Bitte zuerst einen Link eingeben!", text_color="#ef4444")
            return
            
        ordner_pfad = filedialog.askdirectory(title="Speicherort auswählen")
        if not ordner_pfad:
            return

        self.download_button.configure(state="disabled")
        self.title_info_label.configure(text="Analysiere Link und starte Download...", text_color="#cbd5e1")
        
        threading.Thread(target=self.download_process, args=(url, ordner_pfad), daemon=True).start()

    def download_process(self, url, ordner_pfad):
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(ordner_pfad, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.progress_bar.set(0)
            fehler_text = str(e).split('\n')[0]
            self.title_info_label.configure(text=f"❌ Fehler: {fehler_text}", text_color="#ef4444")
        finally:
            self.download_button.configure(state="normal")

if __name__ == "__main__":
    app = ModernDownloader()
    app.mainloop()