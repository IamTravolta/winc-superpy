import argparse
import csv
import datetime

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.


def create_parser():
    parser = argparse.ArgumentParser(prog='superpy', description='Supermarket Inventory Management')

    parser.add_argument('--advance-time', type=int, help='Advance time by specified number of days')

    subparsers = parser.add_subparsers(dest='command', title='Commands')

    parser_buy = subparsers.add_parser('buy', help='Buy a product')
    parser_buy.add_argument('--product-name', help='Product name')
    parser_buy.add_argument('--price', type=float, help='Purchase price')
    parser_buy.add_argument('--expiration-date', help='Expiry date (YYYY-MM-DD)')

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
    parser_buy.add_argument('--quantity', type=int, default=1, help='Quantity of the product to buy')

    parser.add_argument('--set-date', help='Set the current date (YYYY-MM-DD)')

    return parser


import csv

def buy_product(args):
    if not args.quantity:
        args.quantity = 1  # Default quantity is 1 if not provided

    with open('data/products.csv', 'a', newline='') as csvfile:
        fieldnames = ['product name', 'price', 'expiration date', 'quantity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the file is empty and write the headers if needed
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the new product record
        writer.writerow({'product name': args.product_name, 'price': args.price, 'expiration date': args.expiration_date, 'quantity': args.quantity})

    with open('data/sales.csv', 'r', newline='') as csvfile:
        fieldnames = ['product name', 'date', 'price', 'quantity']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        products = list(reader)

    bought_quantity = args.quantity
    for row in products:
        if row['product name'] == args.product_name:
            bought_quantity += int(row['quantity'])
            break

    available_quantity = args.quantity  # Initialize available_quantity here
    print(available_quantity)

    if bought_quantity <= available_quantity:
        with open('data/sales.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([args.product_name, datetime.date.today(), args.price, args.quantity])

        return f"{args.quantity} {args.product_name}(s) bought successfully."
    else:
        return f"Insufficient quantity. Only {available_quantity} {args.product_name}(s) available."


def sell_product(args):
    with open('data/products.csv', 'r') as csvfile:
        products = list(csv.reader(csvfile))

    sold = False
    for row in products:
        if row[0] == args.product_name:
            sold_price = args.price
            if args.quantity:
                sold_quantity = args.quantity
            else:
                sold_quantity = 1
            
            available_quantity = int(row[3]) if len(row) > 3 else 0
            if available_quantity >= sold_quantity:
                row[3] = str(available_quantity - sold_quantity)
                sold = True
                break

    available_quantity = args.quantity  # Initialize available_quantity here

    if sold:
        with open('data/products.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(products)

        with open('data/sales.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([args.product_name, datetime.date.today(), sold_price, sold_quantity])

        return f"{sold_quantity} {args.product_name}(s) sold successfully."
    else:
        return f"Insufficient quantity. Only {available_quantity} {args.product_name}(s) available."


def calculate_revenue(date):
    revenue = 0
    with open('data/sales.csv', 'r') as csvfile:
        sales = csv.reader(csvfile)
        for sale in sales:
            sale_date = datetime.datetime.strptime(sale[1], '%Y-%m-%d').date()
            sale_price = float(sale[2])
            if sale_date == date:
                revenue += sale_price
    return revenue

def calculate_revenue_month(year_month):
    revenue = 0
    with open('data/sales.csv', 'r') as csvfile:
        sales = csv.reader(csvfile)
        for sale in sales:
            sale_date = datetime.datetime.strptime(sale[1], '%Y-%m-%d').date()
            sale_price = float(sale[2])
            if sale_date.year == year_month.year and sale_date.month == year_month.month:
                revenue += sale_price
    return revenue


def generate_revenue_report(args):
    try:
        if args.yesterday:
            date = datetime.date.today() - datetime.timedelta(days=1)
        elif args.today:
            date = datetime.date.today()
        elif args.date:
            date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date()
        else:
            return "Invalid revenue report command"
        
        daily_revenue = calculate_revenue(date)
        daily_report = f"Revenue on {date}: {daily_revenue}"

        try:
            year_month = datetime.datetime.strptime(args.date, '%Y-%m').date()
            if year_month.day != 1:
                raise ValueError("Please enter a valid month in the format YYYY-MM.")
            
            monthly_revenue = calculate_revenue_month(year_month)
            monthly_report = f"Revenue for {year_month.strftime('%B %Y')}: {monthly_revenue}"
        except ValueError:
            monthly_report = "Invalid month format. Please provide a valid month in the format YYYY-MM."

        return f"{daily_report}\n{monthly_report}"
    except ValueError:
        return "Invalid date format. Please provide the date in the format YYYY-MM-DD for a day or YYYY-MM for a month."

    
def generate_inventory_report(args):
    with open('data/products.csv', 'r') as csvfile:
        products = list(csv.reader(csvfile))

    if args.now:
        current_date = datetime.date.today()
    elif args.yesterday:
        current_date = datetime.date.today() - datetime.timedelta(days=1)
    else:
        current_date = get_current_date()

    report = f"Inventory Report - {current_date}:\n"
    report += "--------------------------------\n"
    report += "Product Name\tCount\tBuy Price\tExpiration Date\n"
    report += "--------------------------------\n"
    for product in products:
        name = product[0]
        buy_price = product[1]
        expiration_date = product[2] if len(product) > 2 else ""
        count = get_product_count(name, current_date)
        report += f"{name}\t\t{count}\t{buy_price}\t\t{expiration_date}\n"

    return report


def get_product_count(product_name, current_date):
    count = 0
    with open('data/sales.csv', 'r') as csvfile:
        fieldnames = ['product name', 'date', 'price', 'quantity']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            if row['product name'] == product_name and row['date'] == str(current_date):
                count = int(row['quantity'])
                break
    return count


def save_current_date(date):
    date_str = date.strftime('%Y-%m-%d')
    with open('data/current_date.txt', 'w') as file:
        file.write(date_str)

def set_current_date(args):
    if args.set_date:
        try:
            new_date = datetime.datetime.strptime(args.set_date, '%Y-%m-%d').date()
            save_current_date(new_date)
            print(f"Current date set to: {new_date}")
        except ValueError:
            print("Invalid date format. Please provide the date in the format YYYY-MM-DD.")


def advance_time(days):
    current_date = get_current_date()
    new_date = current_date + datetime.timedelta(days=days)
    save_current_date(new_date)

def get_current_date():
    with open('data/current_date.txt', 'r') as file:
        date_str = file.read()
        if not date_str:
            return datetime.date.today()  # Return the current date as the default
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def save_current_date(date):
    date_str = date.strftime('%Y-%m-%d')
    with open('data/current_date.txt', 'w') as file:
        file.write(date_str)


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.advance_time:
        advance_time(args.advance_time)
        print("OK")
    elif args.set_date:
        set_current_date(args)
    elif args.command == 'buy':
        result = buy_product(args)
        print(result)
    elif args.command == 'sell':
        result = sell_product(args)
        print(result)
    elif args.command == 'report':
        report = generate_inventory_report(args)
        print(report)
    elif args.command == 'report-revenue':
        result = generate_revenue_report(args)
        print(result)
    else:
        parser.print_help()

main()

