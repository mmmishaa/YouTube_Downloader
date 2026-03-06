import yt_dlp
import os

URLS = [input("Введите ссылку на видео: ")]
download_path = 'Downloads/'

def format_selector(ctx):
    formats = ctx.get('formats')

    best_video = next(f for f in formats if f['format_id'] == video_id)
    best_audio = next(f for f in formats if f['format_id'] == audio_id)

    yield {
        'format_id': f'{video_id}+{audio_id}',
        'ext': 'mkv',
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

ydl_opts1 = {
    'ffmpeg_location': 'ffmpeg/',
    'merge_output_format': 'mkv',
    'javascript_runtime': 'deno',
    'ext_utils': {'deno': 'deno/deno.exe'},
    'writetitle': True,
    'quiet': True,
    'no_warnings': True,
}

with yt_dlp.YoutubeDL(ydl_opts1) as ydl:
    info = ydl.extract_info(URLS[0], download=False)
    print("\n--- Доступные форматы видео ---")
    for f in info['formats']:
        vcodec = f.get('vcodec')
        acodec = f.get('acodec')
        if vcodec != 'none' and acodec == 'none':
            print(f"ID: {f['format_id']:<4} | Ext: {f['ext']:<6} | Res: {f.get('resolution'):<10} | Bitrate: {f.get('tbr'):<10}")
    
    print("\n--- Доступные форматы аудио ---")
    for f in info['formats']:
        vcodec = f.get('vcodec')
        acodec = f.get('acodec')
        if vcodec == 'none' and acodec != 'none':
            print(f"ID: {f['format_id']:<4} | Ext: {f['ext']:<6} | Res: {f.get('resolution'):<10} | Bitrate: {f.get('tbr'):<10}")

print()
video_id = input("Введите ID видео (например, 313): ")
audio_id = input("Введите ID аудио (например, 140): ")
print()

ydl_opts2 = {
    'outtmpl': f'{download_path}/%(title)s [%(format_id)s].%(ext)s',
    'format': format_selector,
    'ffmpeg_location': 'ffmpeg/',
    'merge_output_format': 'mkv',
    'javascript_runtime': 'deno',
    'ext_utils': {'deno': 'deno/deno.exe'},
    'writetitle': True,
    'quiet': False,
    'no_warnings': True,
}

with yt_dlp.YoutubeDL(ydl_opts2) as ydl:
    result = ydl.download(URLS)

if result == 0:
    print(f"\nDONE! The video is ready in the Downloads folder.")