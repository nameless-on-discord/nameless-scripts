# This is a script of everything!
# Do anything you want, as long as you comply with the license!

import os
import re
from enum import Enum
from shutil import copyfile
from typing import List
from urllib import request
from zipfile import ZipFile

SOURCE_URL: str = (
    "https://github.com/nameless-on-discord/nameless/archive/refs/tags/{version}.zip"
)
VERSIONS: List[str] = ["1.2.2", "1.2.1", "1.2.0", "1.0.1", "1.0.0"]
FOLDER_NAME: str = "nameless-{version}-{instance_name}"
FOLDER_NAME_REGEX = re.compile(r"nameless-(\d+\.\d+\.\d+.*)-(.*)")
CHOICES = {
    "0": "Exit this",
    "1": "Install nameless instance",
    "2": "Open config wizard for an instance",
    "3": "Run instance",
}


class Selection(Enum):
    """Enum for user selection"""

    EXIT = 0
    INSTALL = 1
    CONFIG = 2
    RUN = 3


def get_folders(directory: str = ".") -> List[str]:
    """Get a folder in the specified directory, '.' by default."""
    return [*filter(os.path.isdir, os.listdir(directory))]


def get_nameless_folders() -> List[str]:
    """Get valid Nameless directories."""
    return [x for x in get_folders() if FOLDER_NAME_REGEX.fullmatch(x)]


def prepare_prompts() -> str:
    """Prepare user prompts based on current condition(s)."""
    prompts = ""

    prompts += f"0 - {CHOICES['0']}\n"
    prompts += f"1 - {CHOICES['1']}\n"

    if any(get_nameless_folders()):
        prompts += f"2 - {CHOICES['2']}\n"
        prompts += f"3 - {CHOICES['3']}\n"

    return prompts


def install_nameless() -> None:
    """Install nameless instance folder"""
    versions = " ; ".join(VERSIONS)

    while (
        version := input(
            f"Specify a version to install (default: {VERSIONS[0]}) - {versions} : "
        )
        or VERSIONS[0].lower().lstrip().rstrip().replace(" ", "")
    ) not in VERSIONS:
        print(f"Invalid version specified ({version})")

    instance_name = input("Specify the instance name: ")

    test_folder_name = FOLDER_NAME.replace("{version}", version).replace(
        "{instance_name}", instance_name
    )

    if test_folder_name in get_nameless_folders():
        print(f"{test_folder_name} already created! Exiting")
    else:
        target_folder_name = f"nameless-{version}"
        target_zipfile_name = f"{target_folder_name}.zip"

        # Create cache directory if not exists
        if not os.path.exists(f".{os.sep}cache"):
            print("Creating cache directory")
            os.mkdir("cache")

        # Cache validation
        # If the zip file is in cache, use it
        # Else, download and save to /cache
        if target_zipfile_name not in os.listdir(f".{os.sep}cache"):
            print(f"{target_zipfile_name} not in 'cache' folder, downloadng...")
            dl_url = SOURCE_URL.replace("{version}", version)

            with request.urlopen(dl_url) as dl_file:
                with open(target_zipfile_name, "wb") as target_file:
                    target_file.write(dl_file.read())

            print(f"Downloaded {target_zipfile_name}")

            os.rename(
                target_zipfile_name, f".{os.sep}cache{os.sep}{target_zipfile_name}"
            )
            print(f"Moved {target_zipfile_name} to cache folder")
        else:
            print(f"{target_zipfile_name} existed in cache folder")

        print(f"Retrieving {target_zipfile_name} from cache")
        copyfile(
            f".{os.sep}cache{os.sep}{target_zipfile_name}",
            f".{os.sep}{target_zipfile_name}",
        )

        print(f"Unzipping {target_zipfile_name}")

        with ZipFile(target_zipfile_name, "r") as zip_file:
            zip_file.extractall()

        print(f"Unzipped {target_zipfile_name}")

        print(f"Renaming {target_folder_name} to {test_folder_name}")
        os.rename(target_folder_name, test_folder_name)
        print("Rename done!")

        print("Removing the zip file...")
        os.remove(target_zipfile_name)


def open_config() -> None:
    print("op 2 called")


def run_instance() -> None:
    print("op 3 called")


def main():
    """Main process."""
    actions = {
        Selection.EXIT: exit,
        Selection.INSTALL: install_nameless,
        Selection.CONFIG: open_config,
        Selection.RUN: run_instance,
    }

    while (
        user_input := int(input(f"{prepare_prompts()}\nEnter your selection: "))
    ) != Selection.EXIT:
        actions[Selection(user_input)]()
        print("==============================")


if __name__ == "__main__":
    main()
