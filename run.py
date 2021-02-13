#!/usr/bin/env python3

import os
import argparse
import asyncio
import logging

from bot.client import BotClient
from cogs.jukebox import Jukebox


def get_args():
    parser = argparse.ArgumentParser('''The Jukebox Jeff YouTube Discord bot''')
    parser.add_argument('-discord_token', type=str, help='The discord token', required=True)
    args = parser.parse_args()
    print(f'Arguments processed: {args}')

    return args


def start(token):
    bot = BotClient()
    bot.add_cog(Jukebox(bot))
    bot.run(token)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = get_args()
    start(args.discord_token)