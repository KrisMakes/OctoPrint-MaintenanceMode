# Maintenance Mode (PSU Control)

A one-icon navbar toggle for OctoPrint that suspends [PSU Control](https://github.com/kantlivelong/OctoPrint-PSUControl)'s
idle auto-off, so a printer stays powered for as long as you are working on it.

> Not affiliated with PSU Control or its author. This is a companion plugin that
> drives PSU Control's own setting; the name states the dependency, nothing more.

## Why

PSU Control powers a printer down once OctoPrint has seen it idle for long enough.
The trouble is that OctoPrint only sees what reaches it over the serial link, and a
lot of maintenance never does: levelling the bed, stepping through the printer's own
LCD menu, turning a leadscrew by hand, checking belt tension. All of it looks exactly
like an idle printer, so the PSU cuts out partway through the job - usually at the
least convenient moment.

The usual workaround is to open PSU Control's settings, untick *Power off when idle*,
do the work, then remember to tick it back. Forgetting leaves a printer powered up
overnight. This plugin makes that a single click, and makes the held state visible so
it is harder to forget.

## What it does

A padlock appears in the navbar, admin-only:

| Icon | Meaning |
| --- | --- |
| Green closed padlock | Normal. PSU Control's auto power-off is on. |
| Red open padlock | Maintenance mode. Auto power-off is held off; the printer will stay powered. |

Clicking it flips PSU Control's `powerOffWhenIdle` setting. The icon is re-read every
ten seconds, so it stays honest if the setting is changed from PSU Control's own
dialog or by another client rather than from this toggle.

The plugin keeps **no state of its own**. PSU Control's setting is the single source
of truth, so uninstalling leaves nothing behind and nothing to migrate.

## Requirements

- OctoPrint 1.4.0 or newer (uses the permissions system)
- [OctoPrint-PSUControl](https://github.com/kantlivelong/OctoPrint-PSUControl)

Without PSU Control installed the toggle has no setting to act on; install that first.

## Installation

In OctoPrint: **Settings → Plugin Manager → Get More… → ...from URL**, and paste:

```
https://github.com/KrisMakes/OctoPrint-MaintenanceMode/archive/master.zip
```

Or from a shell, using the Python environment OctoPrint itself runs under:

```
pip install https://github.com/KrisMakes/OctoPrint-MaintenanceMode/archive/master.zip
```

OctoPrint needs a restart afterwards.

## Using it from OctoFarm-Redux

[OctoFarm-Redux](https://github.com/KrisMakes/OctoFarm-Redux) drives this plugin over
its API, so maintenance mode can be toggled from a printer's command panel and a
farm-wide banner names every printer currently left powered. That is optional on both
sides: this plugin is a normal OctoPrint plugin and works on its own, and Redux keeps
the feature switched off until you enable it under *System → Server → Features*.

## Licence

AGPL-3.0, the same licence OctoPrint uses. See [LICENSE](LICENSE).
