Discord Plugin
======
The Alerta Discord plugin allows you to send alerts to Discord servers using Discord webhooks.

Installation
------------

Clone the GitHub repo and run:

    $ python setup.py install

Or, to install remotely from GitHub run:

    $ pip install git+https://github.com/alerta/alerta-contrib.git#subdirectory=plugins/discord

Configuration
-------------

Add `discord` to the list of enabled `PLUGINS` in `alertad.conf` server
configuration file and set plugin-specific variables either in the
server configuration file or as environment variables.  

**Example**

```
DISCORD_WEBHOOKS_URL="https://discord.com/api/webhooks/<details>"
DISCORD_MINIMUM_ALERT_SEVERITY="warning"
```

Note that `DISCORD_WEBHOOKS_URL` is required and `DISCORD_MINIMUM_ALERT_SEVERITY` is optional (the default value is `"warning"`). 
