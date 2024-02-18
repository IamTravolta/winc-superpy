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
        table.add_column("Quantity", style="bold")
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
    with open('data/products.json', 'r') as json_file:
        products = json.load(json_file)
    count += products[product_name]['quantity']
    #with open('data/sales.csv', 'r') as csvfile:
    #    fieldnames = ['product name', 'date', 'price', 'quantity']
    #    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    #    for row in reader:
    #        if row['product name'] == product_name and row['date'] == str(current_date):
    #            count = int(row['quantity'])
    #            break
    return count

def generate_revenue_report():
    try:
        # Initialize a dictionary to store total revenue and profit for each product
        revenue_report = {}

        # Read sales data from the CSV file and calculate total revenue and profit
        with open('data/sales.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product_name = row['product name']
                price = float(row['price'])
                quantity = int(row['quantity'])
                buy_price = get_buy_price(product_name)
                profit = price - buy_price  # Calculate profit per unit
                total_profit = profit * quantity  # Calculate total profit for all units sold

                if product_name not in revenue_report:
                    revenue_report[product_name] = {'total_revenue': 0, 
                                                    'total_profit': 0, 
                                                    'buy price': buy_price,
                                                    'sold price': price,
                                                    'quantity': 0
                                                    }
                revenue_report[product_name]['total_revenue'] += price * quantity
                revenue_report[product_name]['total_profit'] += total_profit
                revenue_report[product_name]['quantity'] += quantity

        # Generate and display revenue report using rich.Table
        table = Table(title="Revenue Report")
        table.add_column("Product Name", style="bold")
        table.add_column("buy price", style="bold")
        table.add_column("sold price", style="bold")
        table.add_column("quantity", style="bold")
        table.add_column("Total Revenue", style="bold")
        table.add_column("Total Profit", style="bold")

        for product_name, data in revenue_report.items():
            table.add_row(product_name,
                          f"${data['buy price']:.2f}",
                          f"${data['sold price']:.2f}",
                          f"{data['quantity']}",
                          f"${data['total_revenue']:.2f}",
                          f"${data['total_profit']:.2f}"
                          )

        console = Console()
        console.print(table)

    except Exception as e:
        return f"Error generating revenue report: {str(e)}"

def get_buy_price(product_name):
    with open('data/products.csv', 'r') as csv_f:
        reader = csv.DictReader(csv_f)
        for row in reader:
            if row['product name'] == product_name:
                return float(row['price'])
