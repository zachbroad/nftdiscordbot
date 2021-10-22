import json
import os.path

import dateutil
from discord import Embed, Colour
from discord.ext import commands, tasks

from api import Solanart


# URL = 'https://discord.com/api/oauth2/authorize?client_id=900276529903317022&permissions=60496&scope=bot'

class FancyFrenchieDiscordClient(commands.Bot):
    # REAL
    SALES_CHANNEL = 899914291136831518

    # TEST
    # SALES_CHANNEL = 901043744772620298

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, command_prefix='$')

    def start_tasks(self):
        self.check_for_sales.start()

    @tasks.loop(seconds=20)
    async def check_for_sales(self):
        await Solanart.check_for_new_sales(client)

    async def on_ready(self):
        print(f'Logged in as {client}')
        try:
            self.start_tasks()
        except:
            print('tasks already started')

    async def on_message(self, message):
        if message.author == client.user:
            return

        await client.process_commands(message)


client = FancyFrenchieDiscordClient()


@client.command()
async def high(ctx):
    await Solanart.fetch_most_expensive(ctx)


@client.command()
async def low(ctx):
    await Solanart.fetch_cheapest(ctx)


@client.command()
async def recent(ctx):
    await Solanart.fetch_recent(ctx)


def start_bot():
    # print('Loading config...')
    if os.path.exists('data.json'):
        # print('JSON config found... loading it')

        with open('data.json', 'r') as file:
            data = json.load(file)
            Solanart.last_count = data['solanart']
            # print(f'Last count on Solanart: {Solanart.last_count}')

    else:
        # print('JSON config file does not exist... creating one')
        with open('data.json', 'w') as file:
            data = {
                'solanart': 0,
                'magiceden': 0,
            }

            json.dump(data, file)

    client.run('OTAxMDYyMzA0MTg2MTM4NjQ0.YXKZqg.MZK-38vS0gWuI9AWjR3AHLpGQqs')


if __name__ == '__main__':
    start_bot()
