import tempfile
from yt_dlp import YoutubeDL, utils
import shutil
import cli.constants as constants
import os
import subprocess
import platform


def check_ffmpeg():
    ffmpeg_available = True
    try:
        if "windows" in platform.platform().lower():
            subprocess.check_output(['where', 'ffmpeg'])
        else:
            subprocess.check_output(['whereis', 'ffmpeg'])
    except:
        ffmpeg_available = False
    return ffmpeg_available


class yt_logger:
    def error(msg):
        pass

    def warning(msg):
        pass

    def debug(msg):
        pass


def execute(urls, audio_only: bool = False):
    print("Downloading {} url{}{}".format(
        len(urls),
        "s" if len(urls) > 1 else "",
        " (audio only)" if audio_only else ""
    ))
    if audio_only:
        if not check_ffmpeg():
            print("FFMPEG is not installed, but is required to download only audio.")
            return
    for url in urls:
        try:
            with tempfile.NamedTemporaryFile() as temp:
                temp.close()  # Because youtube_dl needs to access it
                file_destination = temp.name
                try:
                    with constants.create_spinner() as context:
                        def hook(data: dict):
                            if data.get("status") == "downloading":
                                context.text = "{} left, {} done".format(
                                    data["_eta_str"], data["_percent_str"])
                            elif data.get("status") == "finished":
                                context.text = "Finished{}".format(
                                    '. Converting to audio...' if audio_only else ''
                                )
                            else:
                                context.text = data.get("status")
                        opts = {
                            "quiet": True,
                            "logger": yt_logger,
                            "progress_hooks": [hook],
                            "outtmpl": file_destination,
                            'format': 'bestaudio/best' if audio_only else "bestvideo/best",
                        }
                        if audio_only:
                            opts["postprocessors"] = [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192'
                            }]
                        ydl = YoutubeDL(opts)
                        with ydl:
                            context.text = "Extracting video infos from url {}...".format(
                                url)
                            infos = ydl.extract_info(url, download=False)
                            context.text = "Downloading from video '{}'...".format(
                                infos["title"])
                            ydl.download([url])
                            context.text = "Resolving filepath..."
                            if audio_only:
                                file_destination = os.path.join(
                                    os.path.dirname(file_destination), ".mp3")
                                ext = "mp3"
                            else:
                                ext = infos["ext"]

                            new_path = constants.Directory.YOUTUBE_VIDEOS + os.sep + "".join([
                                c for c in infos["title"]
                                if c.isalpha() or c.isdigit() or c == ' ']).rstrip() + "." + ext
                            i = 1
                            while os.path.isfile(new_path):
                                context.text = "Duplicate filename, changing it..."
                                new_path = constants.Directory.YOUTUBE_VIDEOS + os.sep + "({}) ".format(i) + \
                                    "".join([
                                        c for c in infos["title"]
                                        if c.isalpha() or c.isdigit() or c == ' ']).rstrip() + "." + ext
                                i += 1
                            context.text = "Moving file..."
                            shutil.move(file_destination, new_path)
                            context.text = "Done"
                    print("\nDownloaded {}".format(infos["title"]))
                except utils.UnsupportedError:
                    print("Invalid link provided (url: {})".format(url))
                except utils.DownloadError as e:
                    print("Could not download video (url: {})".format(url))
        except PermissionError:
            print("The script is missing permissions to write temporary files")
