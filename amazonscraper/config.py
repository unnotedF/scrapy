def get_search_term():
    search_term = input("Product: ").strip().lower()
    while search_term == "":
        search_term = input("Product: ").strip().lower()
    return search_term

def get_specific_brand():
    option = input("Search for a specific brand? (y/n): ").lower().strip()
    while option not in ["y", "n"]:
        print("Please enter 'y' or 'n'.")
        option = input("Search for a specific brand? (y/n): ").lower().strip()
    if option == "y":
        brand = input("Brand: ").lower().strip()
        while brand == "":
            print("Brand cannot be empty.")
            brand = input("Brand: ").lower().strip()
        return brand
    return None

def get_price_range():
    min_price = None
    max_price = None
    option = input("Set a price range? (y/n): ").lower().strip()
    while option not in ["y", "n"]:
        print("Please enter 'y' or 'n'.")
        option = input("Set a price range? (y/n): ").lower().strip()
    if option == "y":
        while True:
            try:
                min_price = input("Min price: ").strip()
                if min_price == "":
                    min_price = None
                    break
                min_price = float(min_price)
                break
            except ValueError:
                print("Please enter a valid number.")
        while True:
            try:
                max_price = input("Max price: ").strip()
                if max_price == "":
                    max_price = None
                    break
                max_price = float(max_price)
                break
            except ValueError:
                print("Please enter a valid number.")
    return min_price, max_price