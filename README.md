![Header logo](.assets/header.png)

# Utile CLI

To do multiple things, easily

[Docs](https://docs.utile.paulinux.fr)

## Installation

It has been developed under python 3.9.0. I don't know if it works well under other versions/os (For this project, I'm on Windows)/...

`pip install -r requirements.txt`

## Building

You can build `utile.exe` to use it as a standalone executable. You can then rename it, and add it to the path to use it in every terminal.

`py build.py build`

## GUI

The easiest way to use this util is to use the GUI, an interface to the CLI. Launch it with the following command: `py gui.py` at the root of the project

## Modules


### Youtube

With this CLI, you can easily download YouTube videos (restricted features for now) with the following command:

```shell
py utile.py youtube <url: str> [--onlyaudio]
```

`url` must be a valid YouTube link, or any valid link supported by youtube_dl

`--onlyaudio` allows you to download only a mp3 version of the video (so only the audio)


### Convert

You can also easily convert images (faster and even easier with gui) like so:

```shell
py utile.py convert <image_path: str> [--format=<format: str>] [--width=<width: int>] [--height=<height: int>]
```
