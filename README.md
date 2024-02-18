# Supermarket Inventory Management

This Python script facilitates managing inventory for a supermarket. It allows buying and selling products, generating reports, and managing dates.

## Usage

The script `superpy.py` supports the following commands:

### Buying a Product

```
./superpy.py buy --product-name Apple --price 1.5 --expiration-date 2023-12-31 --quantity 10
```

- `--product-name`: Name of the product.
- `--price`: Purchase price of the product.
- `--expiration-date`: Expiry date of the product in YYYY-MM-DD format.
- `--quantity`: Quantity of the product to buy. (Default is 1)

### Selling a Product

```
./superpy.py sell --product-name Apple --price 2.0 --quantity 5
```

- `--product-name`: Name of the product.
- `--price`: Selling price of the product.
- `--quantity`: Quantity of the product to sell. (Default is 1)

### Generating Reports

#### Inventory Report

```
./superpy.py report inventory [--now | --yesterday]
```

- `--now`: Report for the current date.
- `--yesterday`: Report for the previous date.

#### Revenue Report

```
./superpy.py report-revenue [--today | --yesterday | --date]
```

- `--today`: Report revenue for today.
- `--yesterday`: Report revenue for yesterday.
- `--date`: Report revenue for a specific date in YYYY-MM-DD format.

### Advance Time

```
./superpy.py --advance-time 7
```

Advance the current date by the specified number of days (7 in this example).


Set the current date to the specified date (in YYYY-MM-DD format).

## Setup

Ensure Python 3 is installed on your system.

1. Clone the repository:

```bash
git clone https://github.com/iamTravolta/supermarket-inventory.git
```

2. Navigate to the project directory:

```bash
cd supermarket-inventory
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Author Information

**Name:** Travolta Ogbee  
**Email:** travoltaogbee@hotmail.nl  
**GitHub:** [github.com/iamTravolta](https://github.com/iamTravolta)
