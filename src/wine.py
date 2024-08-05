class Wine:
    def __init__(self, name, wine_type, year, region, price, quantity):
        if not isinstance(year, int) or year < 0:
            raise ValueError("Year must be a positive integer.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a positive integer.")
        
        self.name = name
        self.wine_type = wine_type
        self.year = year
        self.region = region
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return (f"Wine(name='{self.name}', type='{self.wine_type}', "
                f"year={self.year}, region='{self.region}', price={self.price}, "
                f"quantity={self.quantity})")
