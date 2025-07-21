import yt_dlp
import os

def download_1080p_with_audio(url):
    FFMPEG_PATH = r"ffmpeg\ffmpeg.exe"
    
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'merge_output_format': 'mkv',
        'outtmpl': '%(title)s_1080p.%(ext)s',
        'ffmpeg_location': FFMPEG_PATH,
        'progress_hooks': [lambda d: print(f"\rProgress: {d['_percent_str']} | Прогресс: {d['_percent_str']}", end='')],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},
        'retries': 5
    }

    try:
        print("Starting download... | Начинаем загрузку...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            filename = ydl.prepare_filename(info)
            full_path = os.path.abspath(filename)
            
            print(f"\nDownload complete | Видео успешно загружено: {info['title']}.mkv")
            print(f"\nFile saved to | Файл сохранён по пути: {full_path}")
            
            return full_path
            
    except Exception as e:
        return None

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL / Введите URL YouTube видео: ")
    file_path = download_1080p_with_audio(video_url)
    
    if not file_path:
        print("\nDownload failed. | Не удалось загрузить видео.")
