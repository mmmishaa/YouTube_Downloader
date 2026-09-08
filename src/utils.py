import msvcrt

def make_format_selector(video_id, audio_id):

    def format_selector(ctx):

        formats = ctx.get('formats')

        selected_video = next(f for f in formats if f['format_id'] == video_id)
        selected_audio = next(f for f in formats if f['format_id'] == audio_id)

        yield {
            'format_id': f'{video_id}+{audio_id}',
            'ext': 'mkv',
            'requested_formats': [selected_video, selected_audio],
            'protocol': f'{selected_video["protocol"]}+{selected_audio["protocol"]}'
        }

    return format_selector

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

def ask_restart() -> bool:
    print('Download another video? (y - Yes, n - Exit): ', end='', flush=True)

    while True:
        char = msvcrt.getch()

        try:
            key = char.decode('utf-8').lower()
        except UnicodeDecodeError:
            continue

        if key in ("y", "д"):
            print(key)
            return True
        
        elif key in ("n", "н"):
            print(key)
            return False
        
        elif key == "\x03":
            raise KeyboardInterrupt