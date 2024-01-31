import csv
import json
import datetime
from rich.console import Console
from rich.table import Table
from rich.traceback import install
from modules import loadNsave

install()

# Function to sell a product
def sell_product(args):
    """
    Sell a product and update the inventory and sales records.
    """
    try:
        if args.product_name is None:
            return "Product name is required for the sell command.: use: ./superpy.py -h for full useage"

        # Load product data from JSON file
        with open('data/products.json', 'r') as json_file:
            products = json.load(json_file)

        # Determine the quantity to sell (default to 1 if not specified)
        sold_quantity = args.quantity if args.quantity else 1

        # Check if the product is available and there is sufficient quantity
        if products[args.product_name]['quantity'] == 0:
            loadNsave.check_product_quantity()

        if args.product_name not in products or products[args.product_name]['quantity'] < sold_quantity:
            return f"Insufficient quantity. Only {products[args.product_name]['quantity']} {args.product_name}(s) available.please send mail or buy"

        # Update the product quantity after a successful sale
        products[args.product_name]['quantity'] -= sold_quantity

        # Save the updated product data to the JSON file
        with open('data/products.json', 'w') as json_file:
            json.dump(products, json_file, indent=2)

        # Log the sale in a CSV file
        with open('data/sales.csv', 'a', newline='') as csvfile:
            fieldnames = ['product name', 'date', 'price', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the sale information to the CSV file
            writer.writerow({'product name': args.product_name, 'date': datetime.date.today(),
                             'price': args.price, 'quantity': sold_quantity})

        # Return success message
        return f"{sold_quantity} {args.product_name}(s) sold successfully."

    except Exception as e:
        # Handle exceptions, indicating that the product is not available for sale
        return f"Sorry you don't have {str(e)} in store, buy {str(e)} first"
