"""
expense_categorizer.py

This script reads expense data from a CSV file and categorizes each expense 
based on predefined categories. It handles errors gracefully and prints the 
results to standard output. To run the script, use the command: python expense_categorizer.py
"""

import csv
import sys

def categorize_expense(amount, description):
    """Categorizes an expense based on the description."""
    categories = {
        'Food': ['restaurant', 'groceries', 'snack'],
        'Transport': ['bus', 'train', 'taxi', 'fuel'],
        'Entertainment': ['movie', 'concert', 'game'],
        'Utilities': ['electricity', 'water', 'internet'],
        'Other': []
    }
    
    for category, keywords in categories.items():
        if any(keyword in description.lower() for keyword in keywords):
            return category
    return 'Other'

def read_expenses(file_path):
    """Reads expenses from a CSV file and categorizes them."""
    expenses = []
    
    try:
        with open(file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                amount = float(row['Amount'])
                description = row['Description']
                category = categorize_expense(amount, description)
                expenses.append((amount, description, category))
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error processing the data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    
    return expenses

def print_expenses(expenses):
    """Prints categorized expenses to standard output."""
    for amount, description, category in expenses:
        print(f"{amount:.2f} - {description} - Category: {category}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python expense_categorizer.py <path_to_csv_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    categorized_expenses = read_expenses(file_path)
    print_expenses(categorized_expenses)