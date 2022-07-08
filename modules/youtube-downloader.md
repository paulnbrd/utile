# Youtube Downloader

{% hint style="info" %}
**OS Compatibility:**

This module has been tested on the following platforms:

* Windows

It probably works on other platforms but isn't tested.
{% endhint %}

This module uses a fork of youtube-dl to download videos. Thus you can provide any url youtube-dl supports, such as a direct video link ([https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://www.youtube.com/watch?v=dQw4w9WgXcQ)), a link to a playlist, another streaming service video link such as vimeo, ... (I havn't tested playlists to be honest)

By default (and for now you cannnot really change it, if you do not edit the module :) ), the files are saved in your Documents, under **Utile CLI**, and youtube.

Usage:

```
<utile command> youtube <URLS>... [--onlyaudio]
```

`<URLS>...` (required): The url to the locally running app, or the url you want to redirect.

`--onlyaudio` (optional): If included, tells the module to only download the video audio. This flags require ffmpeg to work. Under the hood, youtube-dl will download a black video (generally in the webm format) and postprocess it using ffmpeg to transform it into a mp3.



Example:

```
// The following will download the specified video
<utile command> youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ

// The following will download only the audio of the video
<utile command> youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ --onlyaudio
```
