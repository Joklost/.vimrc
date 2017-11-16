"""
Keeps lightweight .vimrc up-to-date.
"""
#!/usr/bin/env python3
import json
import os
import urllib.request
import urllib.error
import socket

GITHUB_VERSION = "https://raw.githubusercontent.com/Joklost/.vimrc/master/version.json"
HOME = os.path.expanduser("~")
CONF = "".join([HOME, "/.vimrc.json"])


def request(url: str):
    """Download file from GitHub"""
    try:
        with urllib.request.urlopen(url) as doc:
            return doc.read().decode()
    except (socket.gaierror, urllib.error.URLError) as e:
        return None


def config_exists() -> bool:
    """Check if .vimrc.json exists"""
    return os.path.isfile(CONF)


def github_version() -> list:
    """Return the version currently on the master branch"""
    res = request(GITHUB_VERSION)
    if res is None:
        return [0, 0, 0]
    return json.loads(res)["version"]


def local_version() -> list:
    """Return the local version"""
    if not config_exists():
        return [0, 0, 0]  # force update

    with open(CONF, "r") as conf:
        return json.load(conf)["version"]


def check_updates():
    """Check for updates, called from vim"""
    github = github_version()
    if github == [0, 0, 0]:
        print("Unable to connect to GitHub.")
        return
    if github > local_version():
        print("An update is available. Write :Update to update.")

