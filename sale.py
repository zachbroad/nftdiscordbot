class Sale:
    def __init__(self,
                 id, item, price, date, image,
                 token, fromAddress, toAddress,
                 attributes,
                 marketplace,
                 lastSold=None):
        self.id = id
        self.item = item
        self.price = price
        self.date = date
        self.image = image

        self.token = token
        self.fromAddress = fromAddress
        self.toAddress = toAddress

        self.attributes = attributes
        self.marketplace = marketplace
        self.lastSold = lastSold

    def __str__(self):
        return f'{self.item} sold for {self.price} SOL'

    def get_tx_info(self):
        return f''

    @property
    def pretty(self):
        return (
            f'Just sold for: **{self.price} SOL**\n'
            # f'Seller: **{self.fromAddress}**\n',
            # f'Buyer: **{self.toAddress}**',
            # f'**{self.item}** sold for **{self.price} SOL** on **{self.marketplace}**\n'
        )
        # f'**Explorer:** {self.explorer}\n'
        # f'**Image:** {self.image}'

    @property
    def explorer(self):
        return f'https://explorer.solana.com/address/{self.token}'

