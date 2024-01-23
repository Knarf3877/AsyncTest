import asyncio
#import nest_asyncio # needed to avoid conflict with jupyter notebook event loop
#nest_asyncio.apply() # patch, uses nested event loop

import time

class GroceryStore:
    def __init__(self, name):
        """A class for each grocery store within a chain of stores"""
        self.inventory = {}
        self.name = name

    def add_product(self, name, product_num):
        """Adds a product to the inventory given the name and product number"""
        if not name or not product_num:
            return "Please fill out all categories"
        self.inventory[product_num] = name

    def add_multiple(self, names = [], product_nums = []):
        """Simple extension of add_product method to add multiple at a time"""

        if len(names) != len(product_nums):
            return "Please make sure you've filled out the categories correctly"
        for idx, num in enumerate(product_nums):
            self.add_product(names[idx], num)

    async def binary_search(self, product_num):
        """Checks if product is available"""
        keys = list(self.inventory.keys())
        left, right = 0, len(keys) - 1

        while left <= right:
            mid = (left + right) // 2
            mid_key = keys[mid]
            if mid_key == product_num:
                return True
            elif mid_key < product_num:
                left = mid + 1
            else:
                right = mid - 1
        return False

    def delete_product(self, identifier):
        """Removes product from inventory. User can provide either the product number or name."""
        if identifier.isdigit(): # product number is provided
            return "Couldn't find product" if not self.inventory.pop(int(identifier), None) else "Deleted"
        else: # product name is provided
            for key in self.inventory:
                if self.inventory[key] == identifier:
                    self.inventory.pop(key, None)
                    return "Deleted"
            return "Couldn't find product"

    def __str__(self) -> str:
        return f"{self.name} store contains the following products:\n" + "\n".join([f'{key}: {value}' for key, value in self.inventory.items()])
    
async def async_search(totalInv, productNum):
    tasks = [gstore.binary_search(productNum) for gstore in totalInv]
    results = await asyncio.gather(*tasks)
    names = [gstore.name for gstore in totalInv]
    return [name for name, boolean in zip(names, results) if boolean]
def initialize_test_items():
    nueces = GroceryStore("Nueces St")
    nueces.add_multiple(names=["Apple", "Banana", "Tangerines", "Grape", "Mango"], product_nums=[1, 2, 4, 7, 10])

    riogrande = GroceryStore("Rio Grande")
    riogrande.add_multiple(names=["Apple", "Orange", "Tangerines", "Pear", "Grape", "Pineapple", "Jackfruit"], product_nums=[1,3,4,6,7,8,9])

    deankeaton = GroceryStore("Dean Keaton")
    deankeaton.add_multiple(names=["Canteloupe", "Pear", "Grape", "Pineapple", "Jackfruit", "Mango"], product_nums=[5,6,7,8,9,10])

    return [nueces, riogrande, deankeaton]
print("""Welcome to the RishiRong grocery chain command line interface!
We built this to allow you to find fruit products you're looking for as fast as possible across all our stores.
To do so, we use a binary search algorithm and asynchronous functions to search all our stores at once.
All you need is a product number, and we'll parse through our inventory in the backend to return which stores have that item!

Here's a list of commands you can use to interact with this interface:
'l': List all the products and their product numbers
'q': Quit the interface
[product number]: Returns a lists of stores with that item\n""")
totalInv = initialize_test_items()
while True:
    inp = input("\nEnter your input here: ")
    if inp.isdigit() and int(inp) in range(1,11):
        start_time = time.time()
        storeNames = asyncio.run(async_search(totalInv, int(inp)))
        elapsed_time = time.time() - start_time
        print(f"The {', '.join(map(str, storeNames))} stores have the item. It took {round(elapsed_time, 4)} seconds to find it.")
    elif inp == 'q':
        print("\nThanks for visiting!")
        break
    elif inp == 'l':
        print(f"\nApple: 1\nBanana: 2\nOrange: 3\nTangerines: 4\nCanteloupe:"\
        f"5\nPear: 6\nGrape: 7\nPineapple: 8\nJackfruit: 9\nMango: 10")
    else:
        print("\nPlease enter a valid input.")

