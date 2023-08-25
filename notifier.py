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

# from discord-webhook import DiscordWebhook
from getdata import get_sales


def load_desired_items() -> list[str]:
    pass

""" Takes a list of item names the user desires and sales data and """
def find_desired_sales(desired_items:list[str], sales_data:list[list[str]]):
    pass


if __name__ == "__main__":
    desired_items = []
    sales_data = get_sales()
    find_desired_sales(desired_items)