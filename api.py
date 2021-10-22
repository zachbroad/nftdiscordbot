import datetime
import dateutil.parser
import json

from discord import Embed, Colour
import requests

from sale import Sale


class Solanart:
    last_count = 0
    last_fetch = None

    @staticmethod
    def get_seen(id):
        with open('solanart.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def is_seen(id):
        with open('solanart.json', 'r') as file:
            data = json.load(file)

            if data['seen'] == None:
                return False

            if (id in data['seen']) == True:
                return True

        return False

    @staticmethod
    def add_to_seen(id):
        with open('solanart.json', 'r+') as file:
            data = json.load(file)

            if not Solanart.is_seen(id):
                data['seen'] = [*data['seen'], id]

                file.seek(0)
                json.dump(data, file)
                file.truncate()

    def update_last_count(count):
        with open('data.json', 'r+') as file:
            data = json.load(file)
            data['solanart'] = count
            file.seek(0)
            json.dump(data, file)
            file.truncate()

    @staticmethod
    def fetch():
        URL = 'https://qzlsklfacc.medianetwork.cloud/all_sold_per_collection_day?collection=fancyfrenchies'
        response = requests.get(URL)
        if response.status_code >= 300:
            print(f'ERROR: Status code {response.status_code}.')
            return

        data = response.json()
        return data

    async def check_for_new_sales(client):
        print(f'[{datetime.datetime.now()}] Checking for new sales...')
        data = Solanart.fetch()
        if data == None:
            print('data is None')
            return

        for frenchie in reversed(data):
            sale = Sale(
                id=frenchie['id'],
                item=frenchie['name'],
                price=frenchie['price'],
                token=frenchie['token_add'],
                fromAddress=frenchie['seller_address'],
                toAddress=frenchie['buyerAdd'],
                marketplace='Solanart',
                date=frenchie['date'],
                attributes=frenchie['attributes'],
                image=frenchie['link_img'],
            )
            if Solanart.is_seen(sale.id):
                pass
                # print(f'ignoring {sale.id}')
            else:
                Solanart.add_to_seen(sale.id)
                print(f'added {sale.id} to seen')

                embed = Embed(
                    title=sale.item,
                    # description=sale.pretty,
                    colour=Colour.from_rgb(0, 191, 255),
                    url=sale.explorer,
                    timestamp=dateutil.parser.parse(sale.date),
                )
                embed.set_image(url=sale.image)
                embed.add_field(name='Sale price', value=f'**{sale.price} SOL**', inline=False)
                embed.add_field(name='Buyer', value=sale.toAddress, inline=True)
                embed.add_field(name='Seller', value=f'{sale.fromAddress}', inline=True)
                embed.add_field(name='Token', value=sale.token, inline=False)

                channel = client.get_channel(client.SALES_CHANNEL)
                message = await channel.send(embed=embed)

                pog = client.get_emoji(886353956652056627)
                plus = client.get_emoji(886351382905491496)

                emojis = [plus, pog, '😍', '👀']

                for emoji in emojis:
                    await message.add_reaction(emoji)

    @staticmethod
    async def fetch_most_expensive(ctx):
        data = Solanart.fetch()
        data.sort(key=lambda x: x['price'], reverse=True)
        frenchie = data[0]

        sale = Sale(
            id=frenchie['id'],
            item=frenchie['name'],
            price=frenchie['price'],
            token=frenchie['token_add'],
            fromAddress=frenchie['seller_address'],
            toAddress=frenchie['buyerAdd'],
            marketplace='Solanart',
            date=frenchie['date'],
            attributes=frenchie['attributes'],
            image=frenchie['link_img'],
        )

        embed = Embed(
            title=sale.item,
            description="Today's most expensive Fancy Frenchie sale",
            colour=Colour.from_rgb(11, 218, 81),
            url=sale.explorer,
            timestamp=dateutil.parser.parse(sale.date),
        )
        embed.set_image(url=sale.image)
        embed.add_field(name='Sale price', value=f'**{sale.price} SOL**', inline=False)
        embed.add_field(name='Buyer', value=sale.toAddress, inline=True)
        embed.add_field(name='Seller', value=f'{sale.fromAddress}', inline=True)
        embed.add_field(name='Token', value=sale.token, inline=False)

        message = await ctx.send(embed=embed)
        return sale

    @staticmethod
    async def fetch_cheapest(ctx):
        data = Solanart.fetch()
        data.sort(key=lambda x: x['price'])
        frenchie = data[0]

        sale = Sale(
            id=frenchie['id'],
            item=frenchie['name'],
            price=frenchie['price'],
            token=frenchie['token_add'],
            fromAddress=frenchie['seller_address'],
            toAddress=frenchie['buyerAdd'],
            marketplace='Solanart',
            date=frenchie['date'],
            attributes=frenchie['attributes'],
            image=frenchie['link_img'],
        )

        embed = Embed(
            title=sale.item,
            description="Today's cheapest Fancy Frenchie sale",
            colour=Colour.from_rgb(11, 218, 81),
            url=sale.explorer,
            timestamp=dateutil.parser.parse(sale.date),
        )
        embed.set_image(url=sale.image)
        embed.add_field(name='Sale price', value=f'**{sale.price} SOL**', inline=False)
        embed.add_field(name='Buyer', value=sale.toAddress, inline=True)
        embed.add_field(name='Seller', value=f'{sale.fromAddress}', inline=True)
        embed.add_field(name='Token', value=sale.token, inline=False)

        message = await ctx.send(embed=embed)
        return sale

    @staticmethod
    async def fetch_recent(ctx, count=1):
        """Return <Sale> array of all Frenchies sold on Solanart"""
        data = Solanart.fetch()

        how_many = count  # default sales to show on recent command
        d = data[0:how_many]
        dr = reversed(d)

        for frenchie in dr:
            sale = Sale(
                id=frenchie['id'],
                item=frenchie['name'],
                price=frenchie['price'],
                token=frenchie['token_add'],
                fromAddress=frenchie['seller_address'],
                toAddress=frenchie['buyerAdd'],
                marketplace='Solanart',
                date=frenchie['date'],
                attributes=frenchie['attributes'],
                image=frenchie['link_img'],
            )

            embed = Embed(
                title=sale.item,
                # description=sale.pretty,
                colour=Colour.from_rgb(0, 191, 255),
                url=sale.explorer,
                timestamp=dateutil.parser.parse(sale.date),
            )
            embed.set_image(url=sale.image)
            embed.add_field(name='Sale price', value=f'**{sale.price} SOL**', inline=False)
            embed.add_field(name='Buyer', value=sale.toAddress, inline=True)
            embed.add_field(name='Seller', value=f'{sale.fromAddress}', inline=True)
            embed.add_field(name='Token', value=sale.token, inline=False)

            message = await ctx.send(embed=embed)

        return data
