class Entity:

    def __init__(
        self,
        href,
        user_id=None,
        name=None,
        photo=None,
        price=None,
        description=None
    ) -> None:
        self.href = href
        self.user_id = user_id
        self.name = name
        self.photo = photo
        self.price = price
        self.description = description

    def format():
        pass