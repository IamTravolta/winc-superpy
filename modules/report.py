import csv
import json
import datetime
from rich.console import Console
from rich.table import Table

def generate_inventory_report(products, current_date):
    """
    Generate an inventory report.

    Parameters:
    - products (dict): A dictionary containing product information.
    - current_date (datetime.date): The current date for the report.

    Returns:
    None
    """
    try:
        table = Table(title=f"Inventory Report - {current_date}")
        table.add_column("Product Name", style="bold")
        table.add_column("Count", style="bold")
        table.add_column("Buy Price", style="bold")
        table.add_column("Expiration Date", style="bold")

        for product_name, product_info in products.items():
            name = product_name
            buy_price = product_info['price']
            expiration_date = product_info.get('expiration_date', "")
            count = get_product_count(product_name, current_date)
            table.add_row(name, str(count), str(buy_price), expiration_date)

        console = Console()
        console.print(table)

    except Exception as e:
        return f"Error generating inventory report: {str(e)}"

def get_product_count(product_name, current_date):
    """
    Get the count of a product sold on a specific date.

    Parameters:
    - product_name (str): The name of the product.
    - current_date (datetime.date): The date for which to get the count.

    Returns:
    int: The quantity of the product sold on the specified date.
    """
    count = 0
    with open('data/sales.csv', 'r') as csvfile:
        fieldnames = ['product name', 'date', 'price', 'quantity']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            if row['product name'] == product_name and row['date'] == str(current_date):
                count = int(row['quantity'])
                break
    return count
