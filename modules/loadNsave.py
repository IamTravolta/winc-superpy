import csv
import json
import os
import datetime

def initialize_json_file(file_path):
    """Initialize JSON file with an empty dictionary if it doesn't exist."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump({}, json_file, indent=2)

def check_product_quantity():
    """Check the quantity of products and send an email if any is out of stock."""
    from modules.send_mail import send_email
    try:
        with open('data/products.json', 'r') as json_file:
            products = json.load(json_file)

        low_quantity_products = [name for name, info in products.items() if info['quantity'] == 0]

        if low_quantity_products:
            subject = "Low Quantity Alert"
            body = f"The following products have run out of stock: {', '.join(low_quantity_products)}"
            send_email(subject, body)

    except Exception as e:
        print(f"Error checking product quantity: {str(e)}")
