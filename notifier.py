#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Script which notifies the user of sales they might be interested in

Project : GW2-Gemstore-Notifier
File    : get-data.py
Date    : Friday 25 August 2023
History : 2023/08/25 - v1.0 - Create project file
"""

__author__     = "Martin Siddons"
__email__      = "tjeepot@gmail.com"
__status__     = "Development"  # "Development" "Prototype" "Production"

import sys
import os
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

from get_data import get_sales


def load_desired_items() -> list[str]:
    desired_items = []
    with open("desired_items.txt", "r") as f:
        for line in f:
            if not line.startswith("#"):
                desired_items.append(line.strip("\n"))
    return desired_items

""" Takes a list of item names the user desires and sales data and returns those items in sales_data that match the items in desired_items """
def find_desired_sales(desired_items:list[str], sales_data:list[list[str]]) -> list[list[str]]:
    found_items = []
    for item in sales_data:
        if item[0] in desired_items:
            found_items.append(item)
    return found_items

""" Send a message to Discord with the desired item information. """
def notify_discord(items:list[list[str]], discord_webhook:str, last_updated:str):
    plural_item = "items" if len(items) > 1 else "item"
    title = f"Gemstone Notifier has found {len(items)} {plural_item} from your desired items list on sale!"

    fields = []
    for item in items:
        field = {"name":item[0], "value":f"{item[2]} Gems", "inline": True} 
        fields.append(field)

    content = f"It's recommended that you revise your desired items list to ensure this message doesn't continue to repeat. API last upadated: {last_updated}."

    author = {
        "name": "Gemstore Notifier",
        "url": "https://github.com/TJEEPOT/GW2-Gemstore-Notifier/",
        "icon_url": r"https://wiki.guildwars2.com/images/8/88/Gem_%28highres%29.png"
    }
    
    url = "https://wiki.guildwars2.com/wiki/Gem_Store#List_of_currently_available_Gem_Store_items"
    
    webhook = DiscordWebhook(url=discord_webhook, content=content)
    embed = DiscordEmbed(author=author, color="3e68cb", fields=fields, title=title, url=url )
    webhook.add_embed(embed)
    response = webhook.execute()

    if response.status_code != 200:
        write_to_log(f"Unusual response from Discord: {response.text}")

""" Write the given line to the log. """
def write_to_log(line:str):
    now = datetime.datetime.now()
    time = now.strftime("%b %d %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"\n{time}: {line}")


if __name__ == "__main__":
    load_dotenv() # load the .env file
    discord_webhook = os.getenv("gemstore_webhook")
    if len(sys.argv) > 1:
        discord_webhook = sys.argv[1]

    if discord_webhook is None:
        print("ERROR: Discord Webhook not found. Have you included it as a command line argument and/or as a environment variable?", file=sys.stderr)
        write_to_log("Error: Discord Webhook not found.")
        exit()

    desired_items = load_desired_items()
    sales_data, api_last_updated = get_sales()
    desired_sales = find_desired_sales(desired_items, sales_data)

    if not desired_sales:
        print(f"No sales found for desired items. API last updated: {api_last_updated}")
        write_to_log(f"No desired sales found. API Last updated {api_last_updated}")
        exit()
    
    notify_discord(desired_sales, discord_webhook, api_last_updated)
    for item in desired_sales:
        print(f"Sale found for item {item[0]}! Sale price: {item[2]} Gems")
        write_to_log(f"Sale found for item {item[0]}! Sale price: {item[2]} Gems. API Last updated {api_last_updated}")