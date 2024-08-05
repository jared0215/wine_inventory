class Wine:
    def __init__(self, name, wine_type, year, region, price, quantity):
        self.name = name
        self.wine_type = wine_type
        self.year = year
        self.region = region
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Wine(name='{self.name}', type='{self.wine_type}', year={self.year}, region='{self.region}', price={self.price}, quantity={self.quantity})"