import json
import os.path

import dateutil
from discord import Embed, Colour
from discord.ext import commands, tasks

from api import Solanart

# URL = 'https://discord.com/api/oauth2/authorize?client_id=900276529903317022&permissions=60496&scope=bot'
TEST = True


class FrenchieClient(commands.Bot):
    # REAL CHANNEL
    FANCY_FRENCHIES_SALES_CHANNEL = 899914291136831518
    FANCY_FRENCHIES_LISTING_CHANNEL = 899913978199834675

    # TEST CHANNEL FF
    FANCY_FRENCHIE_TEST_SALES_CHANNEL = 901043744772620298
    FANCY_FRENCHIE_TEST_LISTING_CHANNEL = 901043744772620298

    # MY SERVER
    MY_TEST_SALES_CHANNEL = 900295287099252787
    MY_TEST_LISTING_CHANNEL = 901323205896183808

    SALES_CHANNEL = FANCY_FRENCHIES_SALES_CHANNEL if not TEST else MY_TEST_SALES_CHANNEL
    LISTING_CHANNEL = FANCY_FRENCHIES_LISTING_CHANNEL if not TEST else MY_TEST_LISTING_CHANNEL

    def __init__(self, *args, **kwargs):
        self.sales_channel = FrenchieClient.SALES_CHANNEL
        self.listing_channel = FrenchieClient.LISTING_CHANNEL
        super().__init__(*args, **kwargs, command_prefix='$')

    def start_tasks(self):
        self.check_for_sales.start()

    @tasks.loop(seconds=20)
    async def check_for_sales(self):
        await Solanart.check_for_sales(client)

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


client = FrenchieClient()


@client.command(brief='Who bought the most Frenchies today?', aliases=['buys', 'buyers', 'diamondhands', 'buy', 'sweep', 'whale', 'whales'])
async def sweeper(ctx):
    await Solanart.fetch_sweeper(ctx)


@client.command(brief='Who sold the most Frenchies today?', aliases=['seller', 'sellers', 'paperhand', 'sales'])
async def paperhands(ctx):
    await Solanart.fetch_paperhands(ctx)


@client.command(brief='The most expensive Frenchie sold today', aliases=['expensive', 'highest', 'hi', 'ceiling', 'ceil', 'moon'])
async def high(ctx):
    await Solanart.fetch_most_expensive(ctx)


@client.command(brief='The cheapest Frenchie sold today', aliases=['cheap', 'cheapest', 'lowest', 'floor'])
async def low(ctx):
    await Solanart.fetch_cheapest(ctx)


@client.command(brief='The most recent Frenchie sold today', aliases=['new', 'newest', 'now', 'recently', 'last'])
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

    if TEST:
        # TEST
        client.run('OTAwMjc2NTI5OTAzMzE3MDIy.YW-92w.zpOApvJe8LNfmcB21r7Eo72BYQI')
    else:
        # MAIN
        client.run('OTAxMDYyMzA0MTg2MTM4NjQ0.YXKZqg.MZK-38vS0gWuI9AWjR3AHLpGQqs')


if __name__ == '__main__':
    start_bot()
