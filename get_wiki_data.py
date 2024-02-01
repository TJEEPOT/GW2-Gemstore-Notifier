#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Script for gathering gemstore information from the GW2 wiki.

Project : GW2-Gemstore-Notifier
File    : get-data.py
Date    : Friday 25 August 2023
History : 2023/08/25 - v1.0 - Create project file
"""

__author__     = "Martin Siddons"
__email__      = "tjeepot@gmail.com"
__status__     = "Production"  # "Development" "Prototype" "Production"

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

import requests

""" Make a request to the GW2 wiki API for the data of a given page in json format, then returns the content field (the page data) and timestamp as a set for further processing. Can take an existing session as parameter if doing multiple calls, else will generate a session for just this call. """
def get_current_gemstore(page_name:str, s = requests.session()) -> set[str]:
    url = f"https://wiki.guildwars2.com/api.php?action=query&prop=revisions&titles={page_name}&rvslots=%2A&rvprop=timestamp|content&formatversion=2&format=json"
    headers = {"User-Agent": "GW2-Gemstore-Notifier", # good practice to remain contactable with web admins
                     "From": "https://github.com/TJEEPOT/GW2-Gemstore-Notifier"}  
    response = s.get(url, headers=headers, timeout=10)
    json_response = response.json()

    content = json_response["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
    timestamp = json_response["query"]["pages"][0]["revisions"][0]["timestamp"]
    return (content, timestamp)

"""" Takes a page of wiki data and isolates each row of a table, adding it to a list which is returned once the data has been fully checked. Returned list has each element in the format of [Item, Availability, Cost, Qty, Discounted[y/n], Section, Subsection] """
def process_page_data(data:str) -> list[list[str]]:
    # First, split the data so that each new row begins with {{
    split = data.split("{{")
    gemstore_list = []

    for line in split:
        if not line.startswith("Gem store entry"):
            continue
        
        split_line = line.split("\n| ")
        split_line = split_line[1:] # remove the first line since it contains no useful info
        

        gemstore_list_line = ["UNKNOWN", "UNKNOWN", "0", "1", "n", "UNKNOWN", "UNKNOWN"]
        for item in split_line:
            split_item = item.split(" = ", 1)
            key = split_item[0]
            value = split_item[1]

            if key == "item":
                gemstore_list_line[0] = value
            elif key == "availability":
                gemstore_list_line[1] = value
            elif key == "cost":
                gemstore_list_line[2] = value
            elif key == "qty":
                gemstore_list_line[3] = value
            elif key == "discounted":
                gemstore_list_line[4] = value
            elif key == "section":
                gemstore_list_line[5] = value
            elif key == "subsection":
                value = value.replace("[[", "")
                value = value.replace("]]", "")
                value = value.replace("\n", "")
                value = value.replace("}}", "")
                gemstore_list_line[6] = value

        gemstore_list.append(gemstore_list_line)
                
    return gemstore_list

""" Returns a list of items that are designated as being discounted. """
def find_sale_items(item_list: list[list[str]]) -> list[list[str]]:
    sale_items = []
    for item in item_list:
        if item[4] == "y": # is this item discounted?
            sale_items.append(item)

    return sale_items

""" Wrapper for the above functions. Returns a set: list of items that are currently on sale and the timestamp when the page was last edited. Each item has the format: [Item, Availability, Cost, Qty, Discounted[y/n], Section, Subsection]. """
def get_sales_from_wiki() -> set:
    page_name = "Gem_Store/data"
    data, timestamp = get_current_gemstore(page_name)
    gemstore_list = process_page_data(data)
    sale_items = find_sale_items(gemstore_list)
    return (sale_items, timestamp)


if __name__ == "__main__":
    session = requests.session()
    page_name = "Gem_Store/data"
    data, timestamp = get_current_gemstore(page_name, session)

    gemstore_list = process_page_data(data)

    sale_items = find_sale_items(gemstore_list)
    print(f"{len(sale_items)} items found")
    [print(x) for x in sale_items]
    print(f"API last updated: {timestamp}")