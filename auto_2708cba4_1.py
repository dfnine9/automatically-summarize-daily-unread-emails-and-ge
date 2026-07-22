"""
expense_report.py

This module provides a function to summarize categorized expenses 
and generate a report. It handles errors gracefully and prints 
the results to standard output.
"""

def summarize_expenses(expenses):
    """
    Summarizes categorized expenses.

    Args:
        expenses (dict): A dictionary where keys are categories 
                         and values are lists of expense amounts.

    Returns:
        dict: A dictionary containing the total expense for each category.
    """
    summary = {}
    
    try:
        for category, amounts in expenses.items():
            if not isinstance(amounts, list):
                raise ValueError(f"Amounts for category '{category}' must be a list.")
            total = sum(amounts)
            summary[category] = total
    except Exception as e:
        print(f"Error while summarizing expenses: {e}")
        return {}
    
    return summary

if __name__ == "__main__":
    # Example usage
    expenses = {
        'Food': [10.5, 20.0, 15.75],
        'Transport': [5.0, 3.5],
        'Entertainment': [30.0, 15.0]
    }
    
    report = summarize_expenses(expenses)
    
    print("Expense Summary:")
    for category, total in report.items():
        print(f"{category}: ${total:.2f}")