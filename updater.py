"""
Keeps lightweight .vimrc up-to-date.
"""
#!/usr/bin/env python3
import json
import os
import urllib.request
import time
import subprocess
import multiprocessing as mp


GITHUB_VERSION = "https://raw.githubusercontent.com/Joklost/.vimrc/master/version.json"
GITHUB_VIMRC = "https://raw.githubusercontent.com/Joklost/.vimrc/master/.vimrc"
HOME = os.path.expanduser("~")
CONF = "".join([HOME, "/.vimrc.json"])
VIMRC = "".join([HOME, "/.vimrc"])


def request(url: str) -> list:
    """Download file from GitHub"""
    with urllib.request.urlopen(url) as doc:
        return doc.read().decode()


def vimrc_exists() -> bool:
    """Check if .vimrc exists"""
    return os.path.isfile(VIMRC)


def config_exists() -> bool:
    """Check if .vimrc.json exists"""
    return os.path.isfile(CONF)


def github_version() -> list:
    """Return the version currently on the master branch"""
    return json.loads(request(GITHUB_VERSION))["version"]


def update_files():
    """Update the files from GitHub"""
    version = request(GITHUB_VERSION)
    vimrc = request(GITHUB_VIMRC)
    write_config(json.loads(version))
    write_vimrc(vimrc)

    print("Finished updating files")


def local_version() -> list:
    """Return the local version"""
    if not config_exists():
        return [0, 0, 0]  # force update

    with open(CONF, "r") as conf:
        return json.load(conf)["version"]


def read_config() -> dict:
    """Read .vimrc.json"""
    if config_exists():
        with open(CONF, "r") as conf:
            return json.load(conf)
    else:
        return


def write_config(config: dict):
    """Write .vimrc.json"""
    if not config_exists():
        update_files()
        return

    with open(CONF, "w") as conf:
        json.dump(config, conf)


def write_vimrc(content: str):
    """Write .vimrc"""
    with open(VIMRC, "w") as vimrc:
        vimrc.write(content)


def vim_running():
    """Check if the vim process is running."""
    try:
        return subprocess.check_output(["pgrep", "vim"]) is not None
    except subprocess.CalledProcessError:
        pass

    return False


def __update():
    """Target function for Update process."""
    counter = 0
    while counter < 10:
        time.sleep(1)
        counter += 1

        if not vim_running:
            update_files()
            return


def update():
    """Update files, called from vim"""
    if github_version() > local_version():
        print("Please exit vim within 10 seconds to update...")
        proc = mp.Process(target=__update)
        proc.daemon = False
        proc.start()


def check_updates():
    """Check for updates, called from vim"""
    if github_version() > local_version():
        print("An update is available. Write :Update to update.")


# def main():
#     """Update if GitHub version is newer"""
#     if github_version() > local_version():
#         update_files()


# if __name__ == "__main__":
#     main()
