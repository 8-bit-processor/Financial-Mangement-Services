# MoneyMind - Your Smart Financial Assistant

MoneyMind is a personal finance management application built with Python, Tkinter, and Matplotlib. It's designed to help busy individuals track their income, expenses, debts, assets, and investments, providing a clear overview of their financial health through an intuitive graphical interface.

## Features

*   **Dashboard:** Quick summary of your financial status.
*   **Income Management:** Track various income sources.
*   **Expense Tracking:** Log and categorize your daily spending.
*   **Debt Management:** Monitor loans, credit cards, and repayment progress.
*   **Asset & Investment Tracking:** Keep tabs on your wealth and portfolio growth.
*   **Tax Preparation Aid:** Categorize transactions for easier tax filing.
*   **Spending Analysis:** Visual insights into your spending habits and budgeting.

## How to Run

1.  **Ensure Python is installed:** MoneyMind requires Python 3.x. You can download it from [python.org](https://www.python.org/downloads/).

2.  **Navigate to the project directory:**
    ```bash
    cd "C:\Users\FreeP\Desktop\Money Manager"
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

    This will launch the MoneyMind application window.

## Data Storage

The application stores all your financial data in a local JSON file named `moneymind_data.json`. This file will be created automatically in the application's directory when you run it for the first time.

## Requirements

If you want the dashboard visuals, install dependencies first:

```bash
pip install -r requirements.txt
```

Then run the app with `python main.py`.

## Reports & Export

The app now includes a "Reports" tab where you can export filtered data as CSV, Excel (.xlsx), or PDF, and generate a simple tax summary (total income, deductible expenses, estimated taxable income). Install the updated requirements above before using report export features.