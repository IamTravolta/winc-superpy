import csv
import json
import datetime
from modules import loadNsave

def buy_product(args):
    """
    Buy a product and update the inventory and purchase records.
    :param args: Command-line arguments containing product information.
    :return: Success or error message.
    """
    try:
        # Set default quantity to 1 if not specified
        if not args.quantity:
            args.quantity = 1

        # Initialize the JSON file if it doesn't exist
        loadNsave.initialize_json_file('data/products.json')

        # Load product data from JSON file
        with open('data/products.json', 'r') as json_file:
            products = json.load(json_file)

        # Update product data and save to the JSON file
        with open('data/products.json', 'w') as json_file:
            if args.product_name in products:
                # If the product already exists, update its quantity
                products[args.product_name]['quantity'] += args.quantity
            else:
                # If the product is new, add it to the inventory
                products[args.product_name] = {
                    'price': args.price,
                    'expiration_date': args.expiration_date,
                    'quantity': args.quantity
                }

            # Save the updated product data to the JSON file
            json.dump(products, json_file, indent=2)

        # Log the purchase in a CSV file
        with open('data/products.csv', 'a', newline='') as csvfile:
            fieldnames = ['product name', 'date', 'price', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the purchase information to the CSV file
            writer.writerow({'product name': args.product_name, 'date': datetime.date.today(),
                             'price': args.price, 'quantity': args.quantity})

        # Return success message
        return f"{args.quantity} {args.product_name}(s) bought successfully."

    except Exception as e:
        # Handle exceptions and return an error message
        return f"Error during product purchase: {str(e)}"
