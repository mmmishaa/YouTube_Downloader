import yt_dlp
from pathlib import Path
from src.utils import format_size, get_size_str, ask_restart
from src.libs import check_libs, check_dependencies
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("Downloader")

BASE_PATH = Path(__file__).resolve().parent

DOWNLOAD_PATH = BASE_PATH / 'Downloads'

ydl_opts = {
    'outtmpl': f'{DOWNLOAD_PATH}/%(title)s [%(format_id)s].%(ext)s',
    "retries": 10,
    "retry_sleep": 2,
    "fragment_retries": 10,
    'ffmpeg_location': None,
    'merge_output_format': 'mkv',
    'javascript_runtime': 'deno',
    'ext_utils': {'deno': None},
    'writetitle': True,
    'quiet': True,
    'no_warnings': True,
}

def run_task():
    URL = input("\nEnter video URL: ")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
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

    ydl.params['format'] = f'{video_id}+{audio_id}'

    logger.info("Start downloading")

    result = ydl.download([URL])

    if result == 0:
        print(f"\nDone! The video is ready in the Downloads folder.")

def main():

    while True:
        run_task()

        if not ask_restart():
            break

if __name__ == '__main__':
    check_libs()
    deno_bin_path, ffmpeg_bin_path = check_dependencies(BASE_PATH)
    ydl_opts['ext_utils']['deno'] = str(deno_bin_path)
    ydl_opts['ffmpeg_location'] = str(ffmpeg_bin_path)
    main()