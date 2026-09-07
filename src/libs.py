import urllib.request
from importlib.metadata import PackageNotFoundError, version
import subprocess
import sys
import os
import json
import logging

logger = logging.getLogger("libs")

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
    except Exception as err:
        logger.debug("Failed to check updates: %s", err)

if need_install:
    logger.info("Installing/updating yt-dlp...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default]"]
    )
    os.execv(sys.executable, [sys.executable] + sys.argv)