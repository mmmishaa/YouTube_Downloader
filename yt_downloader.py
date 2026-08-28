import yt_dlp
import os

URLS = [input("Enter video URL: ")]
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

import yt_dlp

def format_size(bytes_val):
    if not bytes_val:
        return "N/A"
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def get_size_str(f, duration):
    size_bytes = f.get('filesize') or f.get('filesize_approx')

    if not size_bytes and duration:
        bitrate = f.get('tbr') or f.get('vbr') or f.get('abr')
        if bitrate:
            size_bytes = (bitrate * 1000 / 8) * duration

    if not size_bytes:
        return "N/A"

    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

with yt_dlp.YoutubeDL(ydl_opts1) as ydl:
    info = ydl.extract_info(URLS[0], download=False)
    duration = info.get("duration")

    print("\n--- Available Video Formats ---")
    for f in info.get("formats", []):
        vcodec = f.get("vcodec")
        acodec = f.get("acodec")
        if vcodec != "none" and acodec == "none":
            fid = str(f.get("format_id") or "N/A")
            ext = str(f.get("ext") or "N/A")
            res = str(f.get("resolution") or "N/A")
            fps = f"{f.get('fps'):.0f}" if f.get("fps") is not None else "N/A"
            codec = (
                f.get("vcodec", "").split(".")[0]
                if f.get("vcodec")
                else "N/A"
            )
            tbr = f"{f.get('tbr'):.1f}" if f.get("tbr") is not None else "N/A"
            size = get_size_str(f, duration)

            print(
                f"ID: {fid:<5} | Ext: {ext:<4} | Res: {res:<10} | FPS: {fps:<4} | "
                f"Codec: {codec:<6} | Bitrate: {tbr:<8} | Size: ~{size:<9}"
            )

    print("\n--- Available Audio Formats ---")
    for f in info.get("formats", []):
        vcodec = f.get("vcodec")
        acodec = f.get("acodec")
        if vcodec == "none" and acodec != "none":
            fid = str(f.get("format_id") or "N/A")
            ext = str(f.get("ext") or "N/A")
            bitrate_val = f.get("abr") if f.get("abr") is not None else f.get("tbr")
            abr = f"{bitrate_val:.1f}" if bitrate_val is not None else "N/A"
            lang = str(f.get("language") or "und")
            size = get_size_str(f, duration)

            print(
                f"ID: {fid:<8} | Ext: {ext:<4} | ABR: {abr:<8} | "
                f"Lang: {lang:<5} | Size: ~{size:<9}"
            )

print()
video_id = input("Enter Video ID (e.g., 313): ")
audio_id = input("Enter Audio ID (e.g., 140-1): ")
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
    print(f"\nDone! The video is ready in the Downloads folder.")