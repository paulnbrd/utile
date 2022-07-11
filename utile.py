import utile
import fire
import termcolor
import yt_dlp

command_line = utile.CommandLine()
try:
    fire.Fire(command_line.interface)
except KeyboardInterrupt:
    print(termcolor.colored("[User aborted]", "red"))
