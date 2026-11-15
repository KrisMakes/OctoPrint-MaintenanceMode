import flask
import octoprint.plugin
from octoprint.access.permissions import Permissions

PSU_CONTROL_IDLE_SETTING = ["plugins", "psucontrol", "powerOffWhenIdle"]


class MaintenanceModePlugin(
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.SettingsPlugin,
):
    """Suspend PSU Control's idle auto-off while a printer is worked on by hand.

    PSU Control powers a printer down once OctoPrint has seen it idle for long
    enough, and OctoPrint cannot see activity that never reaches it: levelling
    the bed, driving the LCD menu, or turning a leadscrew by hand all look like
    idleness. This plugin holds `powerOffWhenIdle` off from a navbar toggle so
    the printer stays powered for as long as the work takes, and makes the fact
    that it is being held visible rather than silent.

    There is no state of our own. The toggle reads and writes PSU Control's own
    global setting, so whatever PSU Control believes is the single truth, and
    nothing is left behind if this plugin is removed.
    """

    # OctoPrint 1.13 will enforce autoescaping globally; opt in now. The navbar
    # template carries no Jinja expressions at all, so nothing can break.
    def is_template_autoescaped(self):
        return True

    # OctoPrint 1.11.2 added this and will flip the default to True in a future
    # release. Declare it explicitly: reading and toggling a printer's power
    # behaviour is not something an anonymous caller should reach.
    def is_api_protected(self):
        return True

    def get_template_configs(self):
        return [dict(type="navbar", custom_bindings=True)]

    def get_assets(self):
        return dict(
            js=["js/maintenance_mode.js"],
            css=["css/maintenance_mode.css"],
        )

    def get_api_commands(self):
        return dict(toggle=[], status=[])

    def _power_off_when_idle(self):
        return bool(self._settings.global_get(PSU_CONTROL_IDLE_SETTING))

    def on_api_get(self, request):
        return flask.jsonify(powerOffWhenIdle=self._power_off_when_idle())

    def on_api_command(self, command, data):
        # A toggle here decides whether a printer can power itself down, so it
        # is held to the same bar as any other power action in OctoPrint.
        if not Permissions.ADMIN.can():
            return flask.make_response("Insufficient rights", 403)

        if command == "status":
            return flask.jsonify(powerOffWhenIdle=self._power_off_when_idle())

        if command == "toggle":
            new_value = not self._power_off_when_idle()
            self._settings.global_set(PSU_CONTROL_IDLE_SETTING, new_value)
            self._settings.save()
            return flask.jsonify(powerOffWhenIdle=new_value)

    def get_update_information(self):
        return dict(
            maintenance_mode=dict(
                displayName="Maintenance Mode (PSU Control)",
                displayVersion=self._plugin_version,
                type="github_release",
                user="KrisMakes",
                repo="OctoPrint-MaintenanceMode",
                current=self._plugin_version,
                pip="https://github.com/KrisMakes/OctoPrint-MaintenanceMode/archive/{target_version}.zip",
            )
        )


__plugin_name__ = "Maintenance Mode (PSU Control)"
__plugin_identifier__ = "maintenance_mode"
__plugin_version__ = "1.0.0"
__plugin_description__ = (
    "Navbar toggle that holds PSU Control's idle auto-off off, so a printer "
    "stays powered through calibration or maintenance that OctoPrint cannot see."
)
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = MaintenanceModePlugin()
__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
