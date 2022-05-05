import logging
import os
import requests

try:
    from alerta.plugins import app  # alerta >= 5.0
except ImportError:
    from alerta.app import app  # alerta < 5.0
from alerta.plugins import PluginBase

LOG = logging.getLogger("alerta.plugins.discord")

ALERTA_SEVERITIES = [
    "unknown",
    "ok",
    "normal",
    "cleared",
    "indeterminate",
    "trace",
    "debug",
    "informational",
    "warning",
    "minor",
    "major"
    "critical",
    "security"
] #List: less severe --> more severe errors
DISCORD_COLOR_GREY = 8421504
DISCORD_COLOR_GREEN = 32768
DISCORD_COLOR_SILVER = 12632256
DISCORD_COLOR_PURPLE = 6950317
DISCORD_COLOR_BLUE = 255
DISCORD_COLOR_YELLOW = 16776960
DISCORD_COLOR_ORANGE = 16753920
DISCORD_COLOR_RED = 16711680
DISCORD_COLOR_BLACK = 0
SEVERITY_TO_DISCORD_COLOR = {
    "unknown": DISCORD_COLOR_GREY,
    "ok" : DISCORD_COLOR_GREEN,
    "normal": DISCORD_COLOR_GREEN,
    "cleared": DISCORD_COLOR_GREEN,
    "indeterminate": DISCORD_COLOR_SILVER,
    "trace": DISCORD_COLOR_GREY,
    "debug": DISCORD_COLOR_PURPLE,
    "informational": DISCORD_COLOR_GREEN,
    "warning": DISCORD_COLOR_BLUE,
    "minor": DISCORD_COLOR_YELLOW,
    "major": DISCORD_COLOR_ORANGE,
    "critical": DISCORD_COLOR_RED,
    "security": DISCORD_COLOR_BLACK
} #Maps severity names to embed colors

DISCORD_WEBHOOKS_URL = os.environ.get("DISCORD_WEBHOOKS_URL") or app.config["DISCORD_WEBHOOKS_URL"]
DISCORD_MINIMUM_ALERT_SEVERITY = os.environ.get("DISCORD_MINIMUM_ALERT_SEVERITY") or app.config.get("DISCORD_MINIMUM_ALERT_SEVERITY", "warning")
#Get the severities on which the webhook should be sent.
SEVERITIES_TO_USE = ALERTA_SEVERITIES[ALERTA_SEVERITIES.index(DISCORD_MINIMUM_ALERT_SEVERITY)]
LOG.debug("The Discord Webhooks plugin will send messages if the severity is one of the following: %s."%(SEVERITIES_TO_USE))

class DiscordWebhooks(PluginBase):

    def pre_receive(self, alert):
        return alert

    def post_receive(self, alert):
        if alert.repeat: #Ignore repeated alerts
            return
        if alert.severity.lower() not in SEVERITIES_TO_USE: #Ignore alert
            LOG.debug("Ignoring alert with severity %s since it is too low."%(alert.severity.lower()))
            return
        #Generate Alert details
        LOG.debug("Generating Discord message...")
        alert_dict = alert.__dict__
        message = "`{}` - **[{}]** - {} ({}) reported {} \n{}".format(
            alert.create_time.strftime('%Y-%m-%d %M:%H:%S'),
            alert.severity.upper(),
            alert.resource,
            alert.environment,
            alert.event,
            alert_dict['text']
        )
        discord_body = {
            "embeds": [{
                "title": "New message posted to Alerta",
                "description": message,
                "inline": False,
                "color": SEVERITY_TO_DISCORD_COLOR[alert.severity.lower()]
            }]
        }

        try:
            LOG.debug(f"Sending request to {DISCORD_WEBHOOKS_URL}...")
            r = requests.post(DISCORD_WEBHOOKS_URL, data=discord_body)
            if r.status_code not in [200, 204]:
                LOG.critical("Unknown status code received from Discord: {} (text {})".format(r.status_code, r.text))
                raise RuntimeError("Unknown status code received from Discord: %s"%(r.status_code))
        except Exception as e:
            LOG.critical("Failed to send Discord Webhooks message: %s."%(e), exc_info=True)
            raise RuntimeError("Error encountered when sending Discord webhooks: %s"%(e))
    def status_change(self, alert, status, text):
        return

