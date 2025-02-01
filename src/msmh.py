""" 
    Minecraft Server Mods Helper
    Copyright (C) 2024 ALEX A https://repo.alexarias.dev/localh3r0/msm-helper/

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import platform
import shutil
import ast
import configparser
import requests
import argparse
import zipfile
import os
import sys

VERSION = "0.3"
USR_OS = "mac" if platform.system().lower() == "darwin" else platform.system().lower()
UPDATED_MODS_FOLDER = "msmh-updater/mods"
UPDATED_CONFIG_FOLDER = "msmh-updater/config"

print("""
##     ##  ######  ##     ##         ##     ## ######## ##       ########  ######## ######## 
###   ### ##    ## ###   ###         ##     ## ##       ##       ##     ## ##       ##     ##
#### #### ##       #### ####         ##     ## ##       ##       ##     ## ##       ##     ##
## ### ##  ######  ## ### ## ####### ######### ######   ##       ########  ######   ######## 
##     ##       ## ##     ##         ##     ## ##       ##       ##        ##       ##   ##  
##     ## ##    ## ##     ##         ##     ## ##       ##       ##        ##       ##    ## 
##     ##  ######  ##     ##         ##     ## ######## ######## ##        ######## ##     ##
""")
print(f"Minecraft Server Mods Helper {VERSION} by localh3r0")
print(f"Detected OS: {USR_OS}")

class MSMHelper:
    def __init__(self):
        self.modpack_url = ""
        self.manifest_url = ""
        self.start_command = ""
        self.is_pack_already_downloaded = False

    def create_instance(self):
        if not os.path.isfile("msmh-instance.ini"):
            config = configparser.ConfigParser()
            config["Instance"] = {
            "modpack_url": "https://github.com/localh3r0/msm-helper/raw/main/src/modpack.zip?download=",
            "manifest_url": "https://github.com/localh3r0/msm-helper/raw/main/src/manifest.txt",
            "start_command": "",
        }
            with open("msmh-instance.ini", "w") as f:
                config.write(f)
            print("Created a new configuration file inside of the mods folder. Please edit before executing MSM-Helper again.")
            f.close()
            sys.exit(0)
        else:
            print("Found an existing configuration file!")
    
    def check_if_server_exist(self):
        if not os.path.exists("mods") or not os.path.exists("config"):
            print("Not inside of a minecraft directory! Ensure the script is executed inside of a valid minecraft directory!")
            return sys.exit(1)

        if not os.path.exists("msmh-instance.ini"):
            print("Did not find instance lock file! Creating one...")
            self.create_instance()
        
        self.read_config_file()

    def read_config_file(self):
        try:
            with open("msmh-instance.ini", "r") as f:
                config_file = f.readlines()

            config = configparser.ConfigParser()
            config.read_string("".join(config_file))
            section = config.sections()
            
            self.modpack_url = config.get(section[0], "modpack_url")
            self.manifest_url = config.get(section[0], "manifest_url")
            self.start_command = config.get(section[0], "start_command")

        except FileNotFoundError:
            print("Did not find instance config file!")
            sys.exit(1)

        self.get_mod_manifest(self.manifest_url)

    def get_mod_manifest(self, manifest_url: str):
        """
        fetches the manifest.txt file from the server 
        """
        print(f"Passed manifest URL: {manifest_url}")
        response = requests.get(manifest_url, stream=True)

        if response.status_code == 200:
            with open("manifest.txt", 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"File downloaded successfully: manifest.txt")
            self.read_and_validate_mods()
        else:
            print(f"Failed to download manifest file: {response.status_code}")
    
    @staticmethod
    def create_mod_manifest():
        """
        creates a manifest.txt file containing a list of
        all mods in mods folder
        """
        mods = os.listdir("mods")
        if "manifest.lock" in mods:
            mods.remove("manifest.lock")
        with open("manifest.txt", "w") as f:
            f.write(str(mods))
        print("Successfully created manifest.txt")

    def download_pack(self):
        """
        downloads the modpack from the provided url
        """
        response = requests.get(self.modpack_url, stream=True)

        if response.status_code == 200:
            print("Downloading modpack...")
            with open("modpack.zip", 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"File downloaded successfully: modpack.zip")
            self.unpack_modpack()
        else:
            print(f"Failed to download file: {response.status_code}")
    
    def unpack_modpack(self):
        """
        Unzip a ZIP file and extract its contents to the specified directory.

        :param zip_file_path: Path to the ZIP file
        :param extract_to_dir: Directory where the files will be extracted
        """
        with zipfile.ZipFile("modpack.zip", 'r') as zip_ref:
            zip_ref.extractall("msmh-updater")
        print(f"Successfully unpacked modpack archive...")
        self.is_pack_already_downloaded = True

    def install_mod(self, name):
        """
        updates the necessary mods
        :param name: the filename of the mod to install
        """
        if self.is_pack_already_downloaded == False:
            self.download_pack()

        for mod in os.listdir(UPDATED_MODS_FOLDER):
            if name in mod:
                try:
                    os.remove(f"mods/{mod}")
                except FileNotFoundError:
                    print(f"Did not find {mod}!")
                shutil.move(f"{UPDATED_MODS_FOLDER}/{name}", "mods")
                print(f"+ Updated mod: {mod}")

    def update_config_files(self):
        """
        updates the config folder with the one provided
        by the pack
        """
        try:
            shutil.rmtree("config")
        except FileNotFoundError:
            print("Did not find a configuration folder.. creating one")

        #os.mkdir("config")
        shutil.move(f"msmh-updater/config", ".")
        print("Successfully updated config folder!")
        print("Done! All mods have been updated to their latest version. You can close this window and launch Minecraft")
        sys.exit(0)

    def read_and_validate_mods(self):
        try:
            with open("manifest.txt", "r") as f:
                server_mods = ast.literal_eval(f.read())
                
        except FileNotFoundError:
            print("Did not find manifest.txt during mod comparison! Make sure it wasn't deleted or moved. Exiting.")
            sys.exit(0)
        
        local_mods = os.listdir("mods")

        print("Local MODS:", local_mods)
        if len(local_mods) == 0:
            print("Detected empty mods folder!")
            for s_mod in server_mods:
                self.install_mod(s_mod)
            self.update_config_files()

        for mod in local_mods:
            for s_mod in server_mods:
                if mod != s_mod:
                    self.install_mod(s_mod)
                else:
                    print(f"Skipping update of {mod}, as it's already up to date.")
        
        self.update_config_files()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minecraft Server Mod Helper")
    parser.add_argument(
        "-m",
        "-manifest",
        action="store_true",
        help="Create a text file containing a list of mods in the mods folder"
    )
    args = parser.parse_args()
    msm = MSMHelper()

    if args.m:
        msm.create_mod_manifest()
        sys.exit(0)

    msm.check_if_server_exist()
