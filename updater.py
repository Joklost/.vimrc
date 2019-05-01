"""
Keeps lightweight .vimrc up-to-date.
"""
#!/usr/bin/env python3
import json
import os
import urllib.request
import urllib.error
import socket
import vim
import re


GITHUB_VERSION = "https://raw.githubusercontent.com/Joklost/.vimrc/master/version.json"
HOME = os.path.expanduser("~")
VERSION_FILE = "".join([HOME, "/.vimrc.json"])
CONFIG_FILE = "".join([HOME, "/.vim/config.json"])


def request(url: str):
    """Download file from GitHub"""
    try:
        with urllib.request.urlopen(url) as doc:
            return doc.read().decode()
    except (socket.gaierror, urllib.error.URLError) as e:
        return None


def versionfile_exists() -> bool:
    """Check if .vimrc.json exists"""
    return os.path.isfile(VERSION_FILE)


def config_exists() -> bool:
    """Check if .vim/config.json exists"""
    return os.path.isfile(CONFIG_FILE)


def github_version() -> list:
    """Return the version currently on the master branch"""
    res = request(GITHUB_VERSION)
    if res is None:
        return [0, 0, 0]
    return json.loads(res)["version"]


def local_version() -> list:
    """Return the local version"""
    if not versionfile_exists():
        return [0, 0, 0]  # force update

    with open(VERSION_FILE, "r") as conf:
        return json.load(conf)["version"]


def check_updates():
    """Check for updates, called from vim"""
    github = github_version()
    if github == [0, 0, 0]:
        print("Unable to connect to GitHub.")
        return
    if github > local_version():
        print("An update is available. Write :Update to update.")
    else:
        print("Already on latest version.")


def check_config():
    if not config_exists():
        return None

    with open(CONFIG_FILE, "r") as conf:
        return json.load(conf)


def add_plugins():
    config = check_config()
    if config is None or "plugins" not in config:
        return

    for plug in config["plugins"]:
        vim.command("Plug '{}'".format(plug))


def source_vimfiles():
    config = check_config()
    if config is None or "vimfiles" not in config:
        return

    for fi in config["vimfiles"]:
        vim.command("source {}".format(fi))


def load_cmds():
    config = check_config()
    if config is None or "cmds" not in config:
        return

    for cmd in config["cmds"]:
        vim.command(cmd)

