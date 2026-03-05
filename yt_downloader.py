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

'''
if __name__ == "__main__":
    video_url = input("Enter YouTube video URL / Введите URL YouTube видео: ")
    file_path = download_1080p_with_audio(video_url)
    
    if not file_path:
        print("\nDownload failed. | Не удалось загрузить видео.")

'''

url = 'https://www.youtube.com/watch?v=SKMQmvFkJe4'

import yt_dlp

ydl_opts = {
    'ffmpeg_location': 'ffmpeg/',
    'quiet': False, 
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    
    formats = info.get('formats', [])

    print(formats)

    print(f"{'ID':<10} {'Расширение':<12} {'Разрешение':<15} {'Заметки'}")
    print("-" * 50)


    for i, f in enumerate(formats):
        acodec = f.get('acodec')
        vcodec = f.get('vcodec')
        f_id = f.get('format_id')
        ext = f.get('ext')
        resolution = f.get('resolution')
        note = f.get('format_note', '')
        print(f"{f_id:<10} {ext:<12} {resolution:<15} {note:<15} {acodec:<10} {vcodec:<10}")
    
    print(len(f))

print("\n--- ИНСТРУКЦИЯ ---")
#print("Введите один ID (например: 22) или комбинацию видео+аудио (например: 137+140)")
video_id = input("Ваш выбор: ").strip()

# 3. Настраиваем опции для самой загрузки
ydl_opts_download = {
    'ffmpeg_location': 'ffmpeg/',
    'merge_output_format': 'mp4',
    'outtmpl': '%(title)s_%(resolution)s.%(ext)s',
    
    # Расширенная логика выбора:
    'format': f"{video_id}+bestaudio[ext=m4a]/bestaudio/best",
    
    # ВАЖНО: Настройка клиентов, чтобы обойти SABR и ошибки форматов
    'extractor_args': {
        'youtube': {
            'player_client': ['web', 'mweb', 'ios'], # Убираем проблемный android
            'skip': ['dash', 'hls'] # Иногда помогает, если ссылки битые
        }
    },
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
}

# 4. Запускаем скачивание
print(f"\nНачинаю загрузку формата: {ydl_opts_download['format']}...")
with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
    ydl.download([url])

print("\nГотово!")

