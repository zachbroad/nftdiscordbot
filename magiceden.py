import json
import requests

from api import Sale


class MagicEden:
    URL = 'https://api-mainnet.magiceden.io/rpc/getActivitiesByQuery?q=%7B%22%24match%22%3A%7B%22collection_symbol%22%3A%22fancy_frenchies%22%7D%2C%22%24sort%22%3A%7B%22blockTime%22%3A-1%7D%2C%22%24skip%22%3A0%7D'
    last_results = []

    # going to have to fetch the image info from sol scanner

    @staticmethod
    def fetch():
        response = requests.get(MagicEden.URL)
        if (response.status_code >= 300):
            print(f'ERROR: Status code {response.status_code}. {response.content}')
            return

        data = response.json()
        results = data['results']
        MagicEden.last_results = results

        frenchie = results[0]

        sale = Sale(
            item=frenchie['_id'],
            price=frenchie['price'],
            token=frenchie['token_add'],
            fromAddress=frenchie['seller_address'],
            toAddress=frenchie['buyerAdd'],
            marketplace='Solanart',
            date=frenchie['date'],
            attributes=frenchie['attributes'],
            image=frenchie['link_img'],
        )

        return data


MagicEden.fetch()
