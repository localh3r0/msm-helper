# Minecraft Server Mod Helper
(if u have a better name lmk :)

# How to use
1. Ensure that the script is inside of a valid minecraft directory, (where your mods and configs files live) if the folders don't exist you can simply create them.
2. You can run the mod directly using ```python3 msmh.py``` or running the exectuable if you dowloaded from releases, (make sure the executable has execute permission)
3. On first run the script will create an ini file inside of the mods folder called "msmh-instance.ini" and then exit. Open this ini file, by default it will contain my repos URL (modpacks and config), you can delete these and add your desired hosting/server URL(s), optionally you can also add a start command to auto run the client after mod check and updating has completed
4. Run the script or executable again to begin mod/config synchronization.

# How it works
The script simply makes a list of all mods in the mods directory, it then downloads and fetches the mod manifest from the provided manifest url and compares the two lists. If there is any mismatch or missing mod files the provided server url is used to download the modpack, then it is is extracted from the pack and installed directly onto the mods folder. On any mod changes, the configuration folder is also updated alongside; typically there are a lot of configuration files that move/change when deleting/adding/updating mods and would add complexity to keep track of, since these files are usually not too crucial (depending on the server), the configuration folder is downloaded entirely and replaced in the proccess.

# For server owners
If you are on the other end, the server hoster, you need to make sure that your server has the necessary mods and config files in correct folder hierarchy in order for the script to correctly identifiy the files needed. When connecting to a server, the script will initially look for one file: manifest.txt. This file should also have an updated list of all server mods for update mod comparison. The link to manifest.txt should be provided directly in the ini file, this is to prevent unecessary downloading if there are no mod updates.

```
(your_modpack.zip) contents:
mods <-- from your mc server
config <-- from your mc server
```
Whenever you update your server mods/config files, you need to ensure to also update the manifest.txt file, alongside the modpack.zip. You can use this repo's file architecture as a template. I do not encourage you to use Github as a hosting platform for minecraft mods as it is againt their TOS. The files uploaded here are just as an example in case you were to host in your own self hosted git.
```
somewhere in your server...
https://yourserver.com/msm-helper/manifest.txt
```

You can use the script to create a manifest.txt list, make sure you run it where your server mods list, it will create the text file in the current working directory.
To create a manifest.txt use:
```
python3 msmh.py -m
```
