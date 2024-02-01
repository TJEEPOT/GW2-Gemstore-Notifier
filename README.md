# What It Does #
Small project to check if there's any desired items on sale on the Guild Wars 2 Gemstore at the moment and if so, send a discord webhook to a given channel. Leverages the information provided by the community on the GW2 Wiki.

# Usage Notes #
In order to work correctly, you will need to add your desired items to desired_items.txt (instructions included within). 
You will also need to provide your Discord webhook, either as a command line option or as the environment variable. To modify the environment variable, open the ```.env``` file in the main project folder and replace "REPLACE_ME" with your webhook.


This script is written in Python 3, therefore I recommend installing the latest version of
 [Python](https://www.python.org/downloads/) to run it. Once installed, do the following:
 - Open a Terminal / Command Line / Powershell prompt in the folder the script is in and type ```python3 -m venv .venv``` to build a virtual environment for the scripts to run in. 
 - Activate the virtual environment with ```.\.venv\Scripts\activate.bat``` in Windows Command Line, ```.\.venv\Scripts\activate.ps1``` in Windows Powershell or ```source \.venv\Scripts\activate``` on Linux or Mac.
 - Load the required libraries with ```pip install -r requirements.txt```.
 - type ```python3 notifier.py [discord webhook]``` to run the program, obviously replacing ```[discord webhook]``` with your actual webhook (unless provided in the .env file).

I'd recommend setting up a task / cron to run ```notifier.py``` every day or two to ensure you don't miss out on a deal.