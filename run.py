
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    while(True):
        print("please enter sales data from the previous market")
        print("data should be six numbers separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")

        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("data is valid")
            break
    return sales_data
        


def validate_data(values):
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly six values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again")
        return False
    return True

def calculate_surplus_data(sales_row):
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales

        surplus_data.append(surplus)
    return surplus_data


def update_worksheet(data, worksheet):
    print(f"updating {worksheet} data\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} sheet updated successfuly\n")


def get_last_5__entries_sales():
    sales = SHEET.worksheet("sales")
    columns = []
    for col in range(1, 7):
        column = sales.col_values(col)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    print("calculating stock data")
    
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus, "surplus")
    sales_column = get_last_5__entries_sales()
    stock_data = calculate_stock_data(sales_column)
    update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwiches\n")
main()