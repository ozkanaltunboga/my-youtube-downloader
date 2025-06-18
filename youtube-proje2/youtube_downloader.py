import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading
import os
import re
from PIL import Image, ImageTk
import requests
from io import BytesIO
from moviepy.editor import VideoFileClip
import json

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class YouTubeDownloader:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        self.youtube_red = "#FF0000"
        self.youtube_dark = "#CC0000"
        self.white = "#FFFFFF"
        self.light_gray = "#F9F9F9"
        self.dark_gray = "#606060"
        
        self.video_info = None
        self.selected_format = None
        self.selected_subtitle = None
        self.download_path = os.path.expanduser("~/Downloads")
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root.configure(fg_color=self.white)
        
        header_frame = ctk.CTkFrame(self.root, fg_color=self.youtube_red, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="YouTube Downloader Pro", 
            font=("Arial Bold", 28),
            text_color=self.white
        )
        title_label.pack(pady=20)
        
        main_container = ctk.CTkFrame(self.root, fg_color=self.white)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        url_frame = ctk.CTkFrame(main_container, fg_color=self.light_gray)
        url_frame.pack(fill="x", pady=(0, 20))
        
        url_label = ctk.CTkLabel(url_frame, text="Video URL:", font=("Arial", 14))
        url_label.pack(side="left", padx=10, pady=10)
        
        self.url_entry = ctk.CTkEntry(
            url_frame, 
            width=500, 
            height=40,
            placeholder_text="Enter YouTube URL here..."
        )
        self.url_entry.pack(side="left", padx=10, pady=10)
        
        self.analyze_btn = ctk.CTkButton(
            url_frame,
            text="Analyze",
            width=100,
            height=40,
            fg_color=self.youtube_red,
            hover_color=self.youtube_dark,
            command=self.analyze_video
        )
        self.analyze_btn.pack(side="left", padx=10, pady=10)
        
        self.video_frame = ctk.CTkFrame(main_container, fg_color=self.light_gray)
        self.video_frame.pack(fill="x", pady=(0, 20))
        
        self.thumbnail_label = ctk.CTkLabel(self.video_frame, text="")
        self.thumbnail_label.pack(side="left", padx=20, pady=20)
        
        self.info_frame = ctk.CTkFrame(self.video_frame, fg_color=self.light_gray)
        self.info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        self.title_info = ctk.CTkLabel(self.info_frame, text="", font=("Arial Bold", 16), wraplength=400, justify="left")
        self.title_info.pack(anchor="w", pady=(0, 5))
        
        self.channel_info = ctk.CTkLabel(self.info_frame, text="", font=("Arial", 12), text_color=self.dark_gray)
        self.channel_info.pack(anchor="w", pady=(0, 5))
        
        self.duration_info = ctk.CTkLabel(self.info_frame, text="", font=("Arial", 12))
        self.duration_info.pack(anchor="w")
        
        self.video_frame.pack_forget()
        
        self.tabview = ctk.CTkTabview(main_container, fg_color=self.white)
        self.tabview.pack(fill="both", expand=True)
        
        self.quality_tab = self.tabview.add("Quality & Format")
        self.subtitle_tab = self.tabview.add("Subtitles")
        self.other_tab = self.tabview.add("Other Options")
        
        self.setup_quality_tab()
        self.setup_subtitle_tab()
        self.setup_other_tab()
        
        self.tabview.pack_forget()
        
        download_frame = ctk.CTkFrame(main_container, fg_color=self.light_gray)
        download_frame.pack(fill="x", pady=(20, 0))
        
        path_label = ctk.CTkLabel(download_frame, text="Save to:", font=("Arial", 12))
        path_label.pack(side="left", padx=10, pady=10)
        
        self.path_label = ctk.CTkLabel(download_frame, text=self.download_path, font=("Arial", 12), text_color=self.dark_gray)
        self.path_label.pack(side="left", padx=10, pady=10)
        
        browse_btn = ctk.CTkButton(
            download_frame,
            text="Browse",
            width=80,
            height=30,
            fg_color=self.dark_gray,
            command=self.browse_folder
        )
        browse_btn.pack(side="left", padx=10, pady=10)
        
        self.download_btn = ctk.CTkButton(
            download_frame,
            text="Download",
            width=150,
            height=40,
            fg_color=self.youtube_red,
            hover_color=self.youtube_dark,
            state="disabled",
            command=self.download_video
        )
        self.download_btn.pack(side="right", padx=10, pady=10)
        
        self.progress_frame = ctk.CTkFrame(self.root, fg_color=self.white, height=60)
        self.progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.progress_frame.pack_propagate(False)
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="", font=("Arial", 12))
        self.progress_label.pack(pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=860, height=20, progress_color=self.youtube_red)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)
        
        self.progress_frame.pack_forget()
        
        # Footer with developer credit
        footer_frame = ctk.CTkFrame(self.root, fg_color=self.light_gray, height=30)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        footer_label = ctk.CTkLabel(
            footer_frame,
            text="Powered by Ozkan Altunboga",
            font=("Arial", 10),
            text_color=self.dark_gray
        )
        footer_label.pack(pady=5)
        
    def setup_quality_tab(self):
        quality_container = ctk.CTkScrollableFrame(self.quality_tab, fg_color=self.white)
        quality_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.format_var = tk.StringVar()
        self.format_radios = []
        
        quality_label = ctk.CTkLabel(quality_container, text="Select video quality:", font=("Arial Bold", 14))
        quality_label.pack(anchor="w", pady=(0, 10))
        
        self.formats_frame = ctk.CTkFrame(quality_container, fg_color=self.white)
        self.formats_frame.pack(fill="both", expand=True)
        
    def setup_subtitle_tab(self):
        subtitle_container = ctk.CTkScrollableFrame(self.subtitle_tab, fg_color=self.white)
        subtitle_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        subtitle_label = ctk.CTkLabel(subtitle_container, text="Available subtitles:", font=("Arial Bold", 14))
        subtitle_label.pack(anchor="w", pady=(0, 10))
        
        self.subtitle_var = tk.StringVar(value="none")
        self.subtitle_radios = []
        
        self.subtitles_frame = ctk.CTkFrame(subtitle_container, fg_color=self.white)
        self.subtitles_frame.pack(fill="both", expand=True)
        
        no_sub_radio = ctk.CTkRadioButton(
            self.subtitles_frame,
            text="No subtitles",
            variable=self.subtitle_var,
            value="none",
            fg_color=self.youtube_red
        )
        no_sub_radio.pack(anchor="w", pady=5)
        
    def setup_other_tab(self):
        other_container = ctk.CTkScrollableFrame(self.other_tab, fg_color=self.white)
        other_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        options_label = ctk.CTkLabel(other_container, text="Additional Options:", font=("Arial Bold", 14))
        options_label.pack(anchor="w", pady=(0, 10))
        
        # Audio Only Option
        self.audio_only_var = tk.BooleanVar()
        audio_only_check = ctk.CTkCheckBox(
            other_container,
            text="Download audio only (MP3)",
            variable=self.audio_only_var,
            fg_color=self.youtube_red,
            font=("Arial", 12)
        )
        audio_only_check.pack(anchor="w", pady=5, padx=20)
        
        # Thumbnail Option
        self.thumbnail_var = tk.BooleanVar()
        thumbnail_check = ctk.CTkCheckBox(
            other_container,
            text="Download video thumbnail",
            variable=self.thumbnail_var,
            fg_color=self.youtube_red,
            font=("Arial", 12)
        )
        thumbnail_check.pack(anchor="w", pady=5, padx=20)
        
        # Description Option
        self.description_var = tk.BooleanVar()
        description_check = ctk.CTkCheckBox(
            other_container,
            text="Save video description",
            variable=self.description_var,
            fg_color=self.youtube_red,
            font=("Arial", 12)
        )
        description_check.pack(anchor="w", pady=5, padx=20)
        
        # Video Info Option
        self.info_var = tk.BooleanVar()
        info_check = ctk.CTkCheckBox(
            other_container,
            text="Save video info (JSON)",
            variable=self.info_var,
            fg_color=self.youtube_red,
            font=("Arial", 12)
        )
        info_check.pack(anchor="w", pady=5, padx=20)
        
    def analyze_video(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        self.analyze_btn.configure(state="disabled", text="Analyzing...")
        threading.Thread(target=self._analyze_video_thread, args=(url,), daemon=True).start()
        
    def _analyze_video_thread(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(url, download=False)
                
            self.root.after(0, self._display_video_info)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to analyze video: {str(e)}"))
            self.root.after(0, lambda: self.analyze_btn.configure(state="normal", text="Analyze"))
            
    def _display_video_info(self):
        self.video_frame.pack(fill="x", pady=(0, 20))
        self.tabview.pack(fill="both", expand=True)
        
        if self.video_info.get('thumbnail'):
            threading.Thread(target=self._load_thumbnail, args=(self.video_info['thumbnail'],), daemon=True).start()
            
        self.title_info.configure(text=self.video_info.get('title', 'Unknown Title'))
        self.channel_info.configure(text=f"Channel: {self.video_info.get('uploader', 'Unknown')}")
        self.duration_info.configure(text=f"Duration: {self._format_duration(self.video_info.get('duration', 0))}")
        
        for widget in self.formats_frame.winfo_children():
            widget.destroy()
            
        # Get all available formats
        video_formats = {}
        audio_formats = {}
        
        for f in self.video_info.get('formats', []):
            if f.get('vcodec') != 'none' and f.get('height'):
                height = f.get('height')
                if height not in video_formats or (f.get('filesize', 0) > video_formats[height].get('filesize', 0)):
                    video_formats[height] = f
            elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                audio_formats[f.get('format_id')] = f
        
        # Define preferred resolutions in order
        preferred_resolutions = [2160, 1440, 1080, 720, 480, 360, 240, 144]
        resolution_names = {
            2160: "4K (2160p)",
            1440: "2K (1440p)", 
            1080: "Full HD (1080p)",
            720: "HD (720p)",
            480: "SD (480p)",
            360: "360p",
            240: "240p",
            144: "144p"
        }
        
        # Create format options prioritizing common resolutions
        format_options = []
        used_heights = set()
        
        # First, add formats for preferred resolutions
        for preferred_height in preferred_resolutions:
            if preferred_height in video_formats:
                vf = video_formats[preferred_height]
                used_heights.add(preferred_height)
                
                # For high quality videos, we need to combine with best audio
                if preferred_height >= 720:
                    format_id = f"{vf['format_id']}+bestaudio"
                    filesize = vf.get('filesize', 0)
                    if filesize == 0 and vf.get('tbr'):
                        # Estimate file size if not available
                        duration = self.video_info.get('duration', 0)
                        filesize = int((vf.get('tbr', 1000) * 1000 * duration) / 8)
                else:
                    format_id = vf['format_id']
                    filesize = vf.get('filesize', 0)
                    
                format_options.append({
                    'format_id': format_id,
                    'height': preferred_height,
                    'ext': vf.get('ext', 'mp4'),
                    'filesize': filesize,
                    'fps': vf.get('fps', 30),
                    'vcodec': vf.get('vcodec', 'unknown'),
                    'display_name': resolution_names.get(preferred_height, f"{preferred_height}p")
                })
        
        # Then add any remaining formats not in preferred list
        for height in sorted(video_formats.keys(), reverse=True):
            if height not in used_heights:
                vf = video_formats[height]
                
                if height >= 720:
                    format_id = f"{vf['format_id']}+bestaudio"
                    filesize = vf.get('filesize', 0)
                    if filesize == 0 and vf.get('tbr'):
                        duration = self.video_info.get('duration', 0)
                        filesize = int((vf.get('tbr', 1000) * 1000 * duration) / 8)
                else:
                    format_id = vf['format_id']
                    filesize = vf.get('filesize', 0)
                    
                format_options.append({
                    'format_id': format_id,
                    'height': height,
                    'ext': vf.get('ext', 'mp4'),
                    'filesize': filesize,
                    'fps': vf.get('fps', 30),
                    'vcodec': vf.get('vcodec', 'unknown'),
                    'display_name': f"{height}p"
                })
        
        # Add format options to UI with improved layout
        for i, fmt in enumerate(format_options[:12]):  # Show up to 12 options for cleaner UI
            size_text = f" (~{fmt['filesize'] / 1024 / 1024:.1f} MB)" if fmt['filesize'] else ""
            codec_text = f" [{fmt['vcodec']}]" if fmt['vcodec'] != 'unknown' else ""
            fps_text = f" {fmt['fps']}fps" if fmt['fps'] != 30 else ""
            label_text = f"{fmt['display_name']}{fps_text} - {fmt['ext'].upper()}{codec_text}{size_text}"
            
            radio = ctk.CTkRadioButton(
                self.formats_frame,
                text=label_text,
                variable=self.format_var,
                value=fmt['format_id'],
                fg_color=self.youtube_red,
                font=("Arial", 12)
            )
            radio.pack(anchor="w", pady=8, padx=20)
            self.format_radios.append(radio)
            
            if i == 0:
                self.format_var.set(fmt['format_id'])
                
        for widget in self.subtitles_frame.winfo_children():
            if widget.winfo_class() != 'CTkRadioButton' or widget.cget("value") != "none":
                widget.destroy()
                
        subtitles = self.video_info.get('subtitles', {})
        auto_subs = self.video_info.get('automatic_captions', {})
        
        all_subs = {}
        for lang, sub_list in subtitles.items():
            all_subs[f"{lang} (Manual)"] = (lang, False)
        for lang, sub_list in auto_subs.items():
            if lang not in subtitles:
                all_subs[f"{lang} (Auto)"] = (lang, True)
                
        for display_name, (lang_code, is_auto) in sorted(all_subs.items()):
            radio = ctk.CTkRadioButton(
                self.subtitles_frame,
                text=display_name,
                variable=self.subtitle_var,
                value=f"{lang_code}|{is_auto}",
                fg_color=self.youtube_red,
                font=("Arial", 12)
            )
            radio.pack(anchor="w", pady=5, padx=20)
            self.subtitle_radios.append(radio)
            
        self.analyze_btn.configure(state="normal", text="Analyze")
        self.download_btn.configure(state="normal")
        
    def _load_thumbnail(self, url):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((160, 90), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.root.after(0, lambda: self.thumbnail_label.configure(image=photo))
            self.thumbnail_label.image = photo
        except:
            pass
            
    def _format_duration(self, seconds):
        if not seconds:
            return "Unknown"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.path_label.configure(text=folder)
            
    def download_video(self):
        if not self.video_info or not self.format_var.get():
            messagebox.showerror("Error", "Please select a video format")
            return
            
        self.download_btn.configure(state="disabled")
        self.progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        threading.Thread(target=self._download_thread, daemon=True).start()
        
    def _download_thread(self):
        try:
            format_id = self.format_var.get()
            
            safe_filename = re.sub(r'[<>:"/\\|?*]', '', self.video_info['title'])
            output_path = os.path.join(self.download_path, f"{safe_filename}.%(ext)s")
            
            # Handle audio-only download
            if hasattr(self, 'audio_only_var') and self.audio_only_var.get():
                format_id = 'bestaudio/best'
                output_path = os.path.join(self.download_path, f"{safe_filename}.%(ext)s")
            
            ydl_opts = {
                'format': format_id,
                'outtmpl': output_path,
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': True,
            }
            
            # Add subtitle options
            if self.subtitle_var.get() != "none":
                lang_code, is_auto = self.subtitle_var.get().split("|")
                ydl_opts['writesubtitles'] = True
                ydl_opts['writeautomaticsub'] = is_auto == "True"
                ydl_opts['subtitleslangs'] = [lang_code]
            
            # Add other options if they exist
            if hasattr(self, 'thumbnail_var') and self.thumbnail_var.get():
                ydl_opts['writethumbnail'] = True
                
            if hasattr(self, 'description_var') and self.description_var.get():
                ydl_opts['writedescription'] = True
                
            if hasattr(self, 'info_var') and self.info_var.get():
                ydl_opts['writeinfojson'] = True
                
            # Convert to MP3 if audio only is selected
            if hasattr(self, 'audio_only_var') and self.audio_only_var.get():
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                
            self.root.after(0, lambda: self.progress_label.configure(text="Downloading video..."))
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url_entry.get(), download=True)
                self.downloaded_file = ydl.prepare_filename(info)
                
            self.root.after(0, self._download_complete)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Download failed: {str(e)}"))
            self.root.after(0, self._reset_download_ui)
            
    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').replace('%', '')
            try:
                progress = float(percent) / 100
                self.root.after(0, lambda: self.progress_bar.set(progress))
                
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                self.root.after(0, lambda: self.progress_label.configure(
                    text=f"Downloading... {percent}% - Speed: {speed} - ETA: {eta}"
                ))
            except:
                pass
                
    def _download_complete(self):
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="Download complete!")
        
        result = messagebox.askyesno(
            "Download Complete", 
            "Video downloaded successfully!\n\nWould you like to convert it to another format?"
        )
        
        if result:
            self._show_conversion_dialog()
        else:
            self._reset_download_ui()
            
    def _show_conversion_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Convert Video")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text="Select output format:", font=("Arial", 14))
        label.pack(pady=20)
        
        format_var = tk.StringVar(value="mp4")
        formats = ["mp4", "avi", "mov", "mkv", "webm", "mp3", "wav", "flac"]
        
        for fmt in formats:
            radio = ctk.CTkRadioButton(
                dialog,
                text=fmt.upper(),
                variable=format_var,
                value=fmt,
                fg_color=self.youtube_red
            )
            radio.pack(anchor="w", padx=50, pady=5)
            
        def convert():
            dialog.destroy()
            self.progress_label.configure(text="Converting video...")
            self.progress_bar.set(0)
            threading.Thread(
                target=self._convert_video,
                args=(format_var.get(),),
                daemon=True
            ).start()
            
        convert_btn = ctk.CTkButton(
            dialog,
            text="Convert",
            fg_color=self.youtube_red,
            hover_color=self.youtube_dark,
            command=convert
        )
        convert_btn.pack(pady=20)
        
    def _convert_video(self, output_format):
        try:
            input_file = self.downloaded_file
            output_file = os.path.splitext(input_file)[0] + f".{output_format}"
            
            if output_format in ['mp3', 'wav', 'flac']:
                clip = VideoFileClip(input_file)
                clip.audio.write_audiofile(output_file, logger=None)
                clip.close()
            else:
                clip = VideoFileClip(input_file)
                clip.write_videofile(output_file, logger=None)
                clip.close()
                
            self.root.after(0, lambda: self.progress_bar.set(1.0))
            self.root.after(0, lambda: self.progress_label.configure(text="Conversion complete!"))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Video converted to {output_format.upper()}!"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Conversion failed: {str(e)}"))
            
        self.root.after(0, self._reset_download_ui)
        
    def _reset_download_ui(self):
        self.download_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="")
        self.progress_frame.pack_forget()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.run()