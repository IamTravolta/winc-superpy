#!/usr/bin/python3

import cmd
import argparse
from superpy_modules.buy import buy_product
from superpy_modules.sell import sell_product
from superpy_modules.report import generate_inventory_report, generate_revenue_report
from superpy_modules.date_management import advance_time, set_current_date, get_current_date


class SuperpyConsole(cmd.Cmd):
    intro = "Welcome to Superpy Console. Type 'help' for a list of commands."
    prompt = "superpy> "

    def do_buy(self, arg):
        """Buy a product: buy <product_name> --price <price> --expiration-date <expiration_date> --quantity <quantity>"""
        args = self._parse_args(arg.split())
        result = buy_product(args)
        print(result)

    def do_sell(self, arg):
        """Sell a product: sell <product_name> --price <price> --quantity <quantity>"""
        args = self._parse_args(arg.split())
        result = sell_product(args)
        print(result)

    def do_report(self, arg):
        """Generate an inventory report"""
        args = self._parse_args(arg.split())
        report = generate_inventory_report(args)
        print(report)

    def do_report_revenue(self, arg):
        """Generate a revenue report: report-revenue --yesterday/--today/--date <date>"""
        args = self._parse_args(arg.split())
        result = generate_revenue_report(args)
        print(result)

    def do_advance_time(self, arg):
        """Advance time: advance-time <days>"""
        args = self._parse_args(arg.split())
        advance_time(args.days)
        print("OK")

    def do_set_date(self, arg):
        """Set the current date: set-date <date>"""
        args = self._parse_args(arg.split())
        set_current_date(args)
        print(f"Current date set to: {args.set_date}")

    def do_quit(self, arg):
        """Exit the console"""
        print("Exiting Superpy Console.")
        return True

    def _parse_args(self, args):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')

        for command_func in [buy_product, sell_product, generate_inventory_report, generate_revenue_report,
                             advance_time, set_current_date]:
            command_func(parser, subparsers)

        return parser.parse_args(args)

if __name__ == "__main__":
    SuperpyConsole().cmdloop()
