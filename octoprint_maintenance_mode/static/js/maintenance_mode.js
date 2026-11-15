$(function () {
    function MaintenanceModeViewModel(parameters) {
        var self = this;
        self.loginState = parameters[0];

        // locked === true  -> psucontrol.powerOffWhenIdle is ON  -> normal, green padlock
        // locked === false -> psucontrol.powerOffWhenIdle is OFF -> held on, red open padlock
        self.locked = ko.observable(true);

        self.iconClass = ko.pureComputed(function () {
            return self.locked() ? "fa-lock" : "fa-unlock";
        });
        self.iconColor = ko.pureComputed(function () {
            return self.locked() ? "#5cb85c" : "#d9534f"; // green : red
        });
        self.tooltip = ko.pureComputed(function () {
            return self.locked()
                ? "Normal mode: PSU auto power-off is ON — click to hold the PSU on for maintenance"
                : "Maintenance mode: PSU held ON, auto power-off is OFF — click to resume normal auto-off";
        });

        self.apply = function (response) {
            self.locked(!!response.powerOffWhenIdle);
        };

        // PSU Control's setting can also be changed from its own settings dialog
        // or by another OctoFarm client, so the icon is re-read rather than
        // assumed to still match what this tab last set.
        self.refreshStatus = function () {
            $.ajax({
                url: API_BASEURL + "plugin/maintenance_mode",
                type: "GET",
                dataType: "json",
            }).done(self.apply);
        };

        self.toggle = function () {
            $.ajax({
                url: API_BASEURL + "plugin/maintenance_mode",
                type: "POST",
                dataType: "json",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify({ command: "toggle" }),
            }).done(self.apply);
        };

        self.onStartupComplete = function () {
            self.refreshStatus();
            setInterval(self.refreshStatus, 10000);
        };
    }

    ADDITIONAL_VIEWMODELS.push([
        MaintenanceModeViewModel,
        ["loginStateViewModel"],
        ["#navbar_plugin_maintenance_mode"],
    ]);
});
