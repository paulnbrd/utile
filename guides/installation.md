# 🔽 Installation

## Install from a release

The release page is located on GitHub: [https://github.com/paulnbrd/utile/releases](https://github.com/paulnbrd/utile/releases), but since the project is still a beta, no release is available. For now, your only option is to follow the step to [install from source](installation.md#install-from-source-1)

## Install from source

You will now learn how to clone the repo and use the cli. The installation script is not yet available, you will have to put the script in your PATH by yourself if you want to access the script from everywhere.

**I/** First, you need to clone the repo using `git clone https://github.com/paulnbrd/utile`.

**II/** Go into the newly created directory, `utile`

**III/** Install the required dependencies with `pip install -r requirements.txt`

**IV/** Everything is ready, you can now use CLIUtils. See [How to use](how-to-use.md) page to begin !

## Build from source

{% hint style="warning" %}
Since this project is in beta, the build procedure **only** works on **Windows**
{% endhint %}

First, follow the steps detailed in [Install from source](installation.md#install-from-source)

Then, to build the project, you can use `build.py` like this: `py build.py build`. This script will build a standalone executable under build of Utile CLI. You will then be able to use it on any Windows system.
