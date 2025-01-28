# Post-it for Dummies
Post-it for Dummies is a The Binding of Isaac: Repentance and Repentance+ tool that automatically edits your save file **based on your Steam achievements** for the game, by using the Steam Web API. It will properly set your **post-it notes** for each character (normal and tainted), as well as your **challenges**, all acording to your Steam achievements.

This is an application based on the old editor from Afterbirth https://moddingofisaac.com/mod/3236/afterbirth-save-editor-v10
    
**Please read this to the end, as I will be going through every detail, doing a step by step guide and addressing known "issues".**

**As expected, make sure to backup your original save files before using this tool.**

<img src="https://github.com/agusaenz/isaac-save-auto-editor-steam/blob/main/assets/readme/basic-gui.png">

# Running

I'm providing both a basic Graphical User Interface, which you can download here: _https://github.com/agusaenz/isaac-save-auto-editor-steam/releases/tag/v1.0_ and then open _isaac-tool.exe_, as well as the code to run with Python (I will be going through this after the GUI tutorial).

# How to use

There is some stuff you need to gather and prepare before using this tool.

## First steps

### 1. Use a new save file * Optional *
You should be able to use the tool in your main file (making a backup first) so that you don't lose your Eden tokens, as well as your progress in donation and Greed machines. Just press Alt + F2 in the stats tab of your file (in game) to make sure everything is in sync with your achievements (characters and challenges unlocked, not crossed out).

-- Optional for new file:

Go into the game and delete one save that you don't currently use. After that, select it, go to stats and press Alt + F2. This will update the secrets of the file with your Steam achievements, so that you can have your corresponding characters and challenges unlocked (but not crossed out). After that, **close** the game.

### 2. Set your profile and game details to public.
In order for the Steam Web API to be able to gather your achievements, you will first need to set these settings to public if you don't already do.

Go to your Steam profile -> Edit profile - > Privacy Settings, and then set _My profile_ and _Game details_ to **public**, as shown in the image:

<img src="https://github.com/agusaenz/isaac-save-auto-editor-steam/blob/main/assets/readme/privacy-settings.png">

### 3. Get your Steam ID
You can easily find this by going to your Steam profile and looking at the url.
The url can be of two forms:

**1.** _https://steamcommunity.com/profiles/76561198070040216/_

**2.** _https://steamcommunity.com/id/cacatuas26/_

What you need is the latter part (76561198070040216 or cacatuas26), any one will work.

### 4. Obtain a Steam Web API Key
If you already have one, then you can use yours. If not, it is really simple to get one:

Go to this link (official Steam website): https://steamcommunity.com/dev/apikey and log in to your account if you are not already, or you can also drag the link to your Steam Client.
Once you are there, you will either see your key or you will be able to request one by filling a "Domain Name" where you can write whatever and click "Register":

<img src="https://github.com/agusaenz/isaac-save-auto-editor-steam/blob/main/assets/readme/api-key.png">

<img src="https://github.com/agusaenz/isaac-save-auto-editor-steam/blob/main/assets/readme/api-key-2.png">

**WARNING!** Do NOT share this with anybody you do not know, as this key is private and any wrongdoing (like surpassing the limit of requests) in the Steam Web API can get you banned from using it. Needless to say, **I do not store any key a user inputs in this tool**. The program runs 100% locally and the source code is there for you to see.

## Usage

Once you have done all the previous steps, you are ready to use the tool.

You want to go ahead and paste both your Steam ID and API key into their respective fields. Then you can select the save file you previously prepared.

The file location is: {Steam installation disk}/Steam/userdata/{user}/250900/remote

And the file name is either **rep_persistentgamedata{1|2|3}.dat** for Repentance, or **rep+persistentgamedata{1|2|3}.dat** for Repentace+ (online beta). The {1|2|3} refers to which of the 3 saves you want to select. Make sure it is the same one you prepared (optional step). Once again, please make sure to **make a backup** of your files before proceeding.

<img src="https://github.com/agusaenz/isaac-save-auto-editor-steam/blob/main/assets/readme/run-script.png">

When it is all set, simply click the button "Run Script" and it will automatically edit your save. Just run the game and check it out!

<img src="https://github.com/agusaenz/isaac-save-auto-editor-steam/blob/main/assets/readme/success.png">

# Known issues

Tainted achievements behave differently than regular characters. For the latter, one post-it note is one Steam achievement for each character. For tainted ones this changes. It goes like this:

Mom's Heart -> No achievement

Ultra Greed (normal difficulty) -> No achievement

Isaac, ???, Satan and The Lamb -> 1 achievement once all 4 have been defeated

Boss Rush and Hush -> 1 achievement if both have been killed

Because of this, tainted post-its will not be 100% accurate until you get those achievemens out of the way. For example, if you killed Mom's Heart, Satan, The Lamb and Mega Satan with Tainted Keeper, only Mega Satan note will appear in your post-it. Same thing would happen if you did Boss Rush but not Hush. Unfortunately this can't be traced through this system.

**Note**: you will get Mom's Heart mark for tainted characters only if you have the achievement for killing Isaac, ???, Satan and The Lamb, and the same will happen with the other example. But don't worry, once you have the proper achievements it will correctly show it.
