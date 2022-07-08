# Cloudflare

{% hint style="info" %}
**OS Compatibility:**

This module currently only supports the following platforms:

* Windows

It could work on other platforms, but it isn't tested.
{% endhint %}

This module's name is `cloudflare`

## Tunnel (create-tunnel)

You can create tunnels using Cloudflare Tunnels and their program `cloudflared`. This module can be used to provide access to locally running applications and servers during the development process. **HTTPS** is enabled automatically on these tunnels. This can be very useful.

{% hint style="info" %}
If **cloudflared** can be found is an accessible command, this module will use it as **coudflared** command. If not, **cloudflared** will automatically be downloaded. Note that it **doesn't install** cloudflared on your system. It just downloads the executable, and stores it in a cache.
{% endhint %}

To create a tunnel, use the subcommand `create-tunnel` like so:

```
<CLIUtils command> cloudflare create-tunnel <URL_TO_REDIRECT> [--should-update-cloudflared]
```

`URL_TO_REDIRECT` (required): The url to the locally running app, or the url you want to redirect.

`--should-update-cloudflared` (optional): If included, tells the module to update cloudflared. Note that it will only update cloudflared if the module downloaded it: it cannot update the cloudflared installed on your system.

For example, I launched a React app on port 3000, and I want to show my friend my progress. I can setup a tunnel to that like so:

```
><CLIUtils command> cloudflare create-tunnel http://localhost:3000
2022-07-08T16:13:33Z INF Thank you for trying Cloudflare Tunnel. Doing so, without a Cloudflare account, is a quick way to experiment and try it out. However, be aware that these account-less Tunnels have no uptime guarantee. If you intend to use Tunnels in production you should use a pre-created named tunnel by following: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps
2022-07-08T16:13:33Z INF Requesting new quick Tunnel on trycloudflare.com...
2022-07-08T16:13:35Z INF +--------------------------------------------------------------------------------------------+
2022-07-08T16:13:35Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2022-07-08T16:13:35Z INF |  https://encouraged-slope-jul-leader.trycloudflare.com                                     |
2022-07-08T16:13:35Z INF +--------------------------------------------------------------------------------------------+
.....
```

My friend can now access `https://encouraged-slope-jul-leader.trycloudflare.com` to see my React project !

Note that this subcommand doesn't login you into Cloudflare, thus this is just a "try it" tunnel: no uptime guarantee. If you aim to create a long during tunnel, a subcommand will be created for that, but for now, it is not possible. You can use cloudflared directly to create this kind of tunnel. Follow the steps detailed [here](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/).
