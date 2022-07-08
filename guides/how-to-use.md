# ✏ How to use

Using CLIUtils is very simple. Every command is in this format

```
py cli.py <module_name> module_argument_1 module_argument_2 --flag=flag_value

// If you built cli.exe and the directory
// containing it is in the PATH, you can
// also use CLIUtils with the command:
cli <module_name> module_argument_1 module_argument_2 --flag=flag_value
```

Apart from `py` and `cli.py`, the command content differs for each module.

Under Modules on the sidebar, you can discover all the available modules and how to use them. For example, we have the YouTube downloader module, which allows to quickly download videos/audios from YouTube. An example command can be:

```
py cli.py youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

And if you want to download only the audio, there is a flag for that. Flags can be specified with two dashes, like so:

```
py cli.py youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ --onlyaudio
```
