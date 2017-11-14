"""
Keeps lightweight .vimrc up-to-date.
"""
#!/usr/bin/env python3
import json
import os
import urllib.request


GITHUB_VERSION = "https://raw.githubusercontent.com/Joklost/.vimrc/master/version.json"
HOME = os.path.expanduser("~")
CONF = "".join([HOME, "/.vimrc.json"])


def request(url: str) -> list:
    """Download file from GitHub"""
    with urllib.request.urlopen(url) as doc:
        return doc.read().decode()


def config_exists() -> bool:
    """Check if .vimrc.json exists"""
    return os.path.isfile(CONF)


def github_version() -> list:
    """Return the version currently on the master branch"""
    return json.loads(request(GITHUB_VERSION))["version"]


def local_version() -> list:
    """Return the local version"""
    if not config_exists():
        return [0, 0, 0]  # force update

    with open(CONF, "r") as conf:
        return json.load(conf)["version"]


def check_updates():
    """Check for updates, called from vim"""
    if github_version() > local_version():
        print("An update is available. Write :Update to update.")
