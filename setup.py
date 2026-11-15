# Deliberately a plain setuptools setup rather than OctoPrint's
# `octoprint_setuptools` helper: pip builds in an isolated environment where
# OctoPrint is not importable, so the helper's import would fail for anyone
# installing straight from a GitHub zip - which is how OctoPrint's own Plugin
# Manager installs "from URL". The entry point below is the only thing the
# helper would have generated for us.
from setuptools import setup

plugin_identifier = "maintenance_mode"
plugin_package = "octoprint_maintenance_mode"
plugin_name = "OctoPrint-MaintenanceMode"
plugin_version = "1.0.0"

with open("README.md", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name=plugin_name,
    version=plugin_version,
    description=(
        "Navbar toggle that holds PSU Control's idle auto-off off, so a printer "
        "stays powered through calibration or maintenance that OctoPrint cannot see."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="KrisMakes",
    author_email="356573616+KrisMakes@users.noreply.github.com",
    url="https://github.com/KrisMakes/OctoPrint-MaintenanceMode",
    license="AGPLv3",
    python_requires=">=3.7,<4",
    packages=[plugin_package],
    package_data={plugin_package: ["templates/*.jinja2", "static/js/*.js", "static/css/*.css"]},
    include_package_data=True,
    zip_safe=False,
    entry_points={"octoprint.plugin": ["{} = {}".format(plugin_identifier, plugin_package)]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Topic :: Printing",
    ],
)
