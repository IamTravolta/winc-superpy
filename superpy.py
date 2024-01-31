import datetime
import argparse
from modules import sell, buy, send_mail, loadNsave, report, date_manage

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.


def create_parser():
    uss = """
./superpy.py buy --product-name Apple --price 1.5 --expiration-date 2023-12-31 --quantity 10

./superpy.py sell --product-name Apple --price 2.0 --quantity 5

./superpy.py report inventory --now

./superpy.py --advance-time 7 
"""
    parser = argparse.ArgumentParser(prog=uss, description='Supermarket Inventory Management')
    parser.add_argument('--advance-time', type=int, help='Advance time by specified number of days')
    subparsers = parser.add_subparsers(dest='command', title='Commands')

    parser_buy = subparsers.add_parser('buy', help='Buy a product')
    parser_buy.add_argument('--product-name', help='Product name')
    parser_buy.add_argument('--price', type=float, help='Purchase price')
    parser_buy.add_argument('--expiration-date', help='Expiry date (YYYY-MM-DD)')
    parser_buy.add_argument('--quantity', type=int, default=1, help='Quantity of the product to buy')

    parser_sell = subparsers.add_parser('sell', help='Sell a product')
    parser_sell.add_argument('--product-name', help='Product name')
    parser_sell.add_argument('--price', type=float, help='Selling price')
    parser_sell.add_argument('--quantity', type=int, default=1, help='Quantity of the product to sell')

    parser_report = subparsers.add_parser('report', help='Generate inventory report')
    parser_report.add_argument('type', choices=['inventory'], help='Type of report')
    parser_report.add_argument('--now', action='store_true', help='Report for the current date')
    parser_report.add_argument('--yesterday', action='store_true', help='Report for the previous date')

    parser_report_revenue = subparsers.add_parser('report-revenue', help='Generate revenue report')
    parser_report_revenue.add_argument('--yesterday', action='store_true', help='Report revenue for yesterday')
    parser_report_revenue.add_argument('--today', action='store_true', help='Report revenue for today')
    parser_report_revenue.add_argument('--date', help='Report revenue for a specific date (YYYY-MM-DD)')

    parser.add_argument('--set-date', help='Set the current date (YYYY-MM-DD)')

    return parser

import json

def load_products():
    """
    Load products from a JSON file.

    Returns:
    dict: A dictionary containing product information.
    """
    try:
        with open('data/products.json', 'r') as json_file:
            products = json.load(json_file)
        return products
    except Exception as e:
        print(f"Error loading products: {str(e)}")
        return {}


def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.advance_time:
            date_manage.advance_time(args.advance_time)
            print("OK")
        elif args.set_date:
            date_manage.set_current_date(args)
        elif args.command == 'buy':
            result = buy.buy_product(args)
            print(result)
        elif args.command == 'sell':
            result = sell.sell_product(args)
            print(result)
        elif args.command == 'report':
            # Load products from JSON or any other source
            products = load_products()

            # Obtain the current date
            current_date = datetime.date.today()

            # Use the functions from the report module
            report.generate_inventory_report(products, current_date)
        elif args.command == 'report-revenue':
            result = report.generate_revenue_report(args)
            print(result)
        else:
            parser.print_help()

        # Check and notify if products have run out of stock
        #loadNsave.check_product_quantity()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
