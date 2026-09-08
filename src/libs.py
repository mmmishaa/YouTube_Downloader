import urllib.request
from importlib.metadata import PackageNotFoundError, version
import subprocess
import sys
import os
import json
import logging
import platform
from pathlib import Path
import shutil
import ssl

logger = logging.getLogger("libs")

DENO_TARGETS: dict[tuple[str, str], str] = {
    ("windows", "x86_64"): "x86_64-pc-windows-msvc",
    ("windows", "arm64"): "aarch64-pc-windows-msvc",
    ("linux", "x86_64"): "x86_64-unknown-linux-gnu",
    ("linux", "arm64"): "aarch64-unknown-linux-gnu",
    ("darwin", "x86_64"): "x86_64-apple-darwin",
    ("darwin", "arm64"): "aarch64-apple-darwin",
}

FFMPEG_URLS: dict[tuple[str, str], str] = {
    ("windows", "x86_64"): (
        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
        "ffmpeg-master-latest-win64-gpl.zip"
    ),
    ("windows", "arm64"): (
        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
        "ffmpeg-master-latest-winarm64-gpl.zip"
    ),
    ("linux", "x86_64"): (
        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
        "ffmpeg-master-latest-linux64-gpl.tar.xz"
    ),
    ("linux", "arm64"): (
        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
        "ffmpeg-master-latest-linuxarm64-gpl.tar.xz"
    ),
    ("darwin", "x86_64"): (
        "https://ffmpeg.martin-riedl.de/redirect/latest/macos/amd64/release/ffmpeg.zip"
    ),
    ("darwin", "arm64"): (
        "https://ffmpeg.martin-riedl.de/redirect/latest/macos/arm64/release/ffmpeg.zip"
    ),
}

def check_dependencies(base_path: Path) -> tuple[Path, Path]:

    def get_norm_arch(raw_arch):
        if raw_arch in ("x86_64", "amd64", "x64"):
            return "x86_64"
        if raw_arch in ("arm64", "aarch64"):
            return "arm64"

        raise RuntimeError(f"Unsupported CPU architecture: {raw_arch}")

    def get_deno_url(system: str, arch: str) -> str:
        target: str = DENO_TARGETS[(system, arch)]
        return f"https://github.com/denoland/deno/releases/latest/download/deno-{target}.zip"


    def get_ffmpeg_url(system: str, arch: str) -> str:
        return FFMPEG_URLS[(system, arch)]

    system = platform.system().lower()
    raw_arch = platform.machine().lower()   
    arch = get_norm_arch(raw_arch)

    is_windows: bool = system == "windows"

    binary_name_deno: str = "deno.exe" if is_windows else "deno"
    binary_name_ffmpeg: str = "ffmpeg.exe" if is_windows else "ffmpeg"

    bin_path = base_path / "bin"

    bin_path.mkdir(parents=True, exist_ok=True)

    deno_bin_path = next(bin_path.rglob(binary_name_deno), None)
    ffmpeg_bin_path = next(bin_path.rglob(binary_name_ffmpeg), None)

    if deno_bin_path is not None and ffmpeg_bin_path is not None:
        logger.info('FFmpeg and Deno found') 
    else:
        logger.info('FFmpeg and Deno not found. Starting the download')
        deno_url = get_deno_url(system=system, arch=arch)
        ffmpeg_url = get_ffmpeg_url(system=system, arch=arch)

        temp_path = base_path / 'temp'
        temp_path.mkdir(parents=True, exist_ok=True)

        temp_path_deno = temp_path / deno_url.split("/")[-1]
        temp_path_ffmpeg = temp_path / ffmpeg_url.split("/")[-1]

        extract_deno = temp_path / "deno_extracted"
        extract_ffmpeg = temp_path / "ffmpeg_extracted"

        try:
            ctx = ssl.create_default_context()
            ctx.set_ciphers("DEFAULT@SECLEVEL=1")

            req_deno = urllib.request.Request(
                url=deno_url,
                headers={"User-Agent": "Mozilla/5.0"},
            )

            with (
                urllib.request.urlopen(req_deno, context=ctx, timeout=60) as response_deno,
                open(temp_path_deno, "wb") as file_out,
            ):
                shutil.copyfileobj(response_deno, file_out, length=64 * 1024)

            req_ffmpeg = urllib.request.Request(
                url=ffmpeg_url,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            with (
                urllib.request.urlopen(req_ffmpeg, context=ctx, timeout=60) as response_ffmpeg,
                open(temp_path_ffmpeg, "wb") as file_out,
            ):
                shutil.copyfileobj(response_ffmpeg, file_out, length=64 * 1024)

            shutil.unpack_archive(temp_path_deno, extract_deno)
            shutil.unpack_archive(temp_path_ffmpeg, extract_ffmpeg)

            found_deno = next(extract_deno.rglob(binary_name_deno), None)
            found_ffmpeg = next(extract_ffmpeg.rglob(binary_name_ffmpeg), None)

            if found_deno is None:
                raise FileNotFoundError(
                    f"Binary {binary_name_deno} not found in archive"
                )
            if found_ffmpeg is None:
                raise FileNotFoundError(
                    f"Binary {binary_name_ffmpeg} not found in archive"
                )

            deno_bin_path = bin_path / binary_name_deno
            ffmpeg_bin_path = bin_path / binary_name_ffmpeg

            shutil.move(str(found_deno), str(deno_bin_path))
            shutil.move(str(found_ffmpeg), str(ffmpeg_bin_path))

            if not is_windows:
                deno_bin_path.chmod(0o755)
                ffmpeg_bin_path.chmod(0o755)

        finally:
            shutil.rmtree(temp_path, ignore_errors=True)

        logger.info("FFmpeg and Deno have been successfully installed")

    return deno_bin_path, ffmpeg_bin_path      

def check_libs():

    logger.info("Checking libraries, dependencies, and their versions")

    need_install = False

    try:
        pkg_version = version("yt-dlp")
    except PackageNotFoundError:
        pkg_version = None
        need_install = True

    if not need_install:
        try:
            req = urllib.request.Request(
                "https://pypi.org/pypi/yt-dlp/json",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode("utf-8"))
                latest_version = data["info"]["version"]

                if pkg_version != latest_version:
                    logger.info(
                        "New version found: %s. Current: %s",
                        latest_version,
                        pkg_version,
                    )
                    need_install = True
                else:
                    logger.info("The latest versions of the libraries have already been installed")
        except Exception as err:
            logger.debug("Failed to check updates: %s", err)

    if need_install:
        logger.info("Installing/updating yt-dlp...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default]"]
        )
        os.execv(sys.executable, [sys.executable] + sys.argv)