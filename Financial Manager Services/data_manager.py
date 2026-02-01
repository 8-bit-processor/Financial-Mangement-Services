import json
from datetime import datetime
import os

class DataManager:
    def __init__(self, data_file="moneymind_data.json"):
        self.data_file = data_file
        self.data = {
            "income": [],
            "expenses": [],
            "debts": [],
            "assets": [],
            "investments": []
        }
        self._load_data()
        print(f"Data manager initialized using file: {self.data_file}")

    def _load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
                print("Data loaded successfully.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {self.data_file}: {e}. Initializing with empty data.")
                # If file is corrupt, start fresh
                self.data = {
                    "income": [],
                    "expenses": [],
                    "debts": [],
                    "assets": [],
                    "investments": []
                }
            except Exception as e:
                print(f"An unexpected error occurred while loading data: {e}. Initializing with empty data.")
                self.data = {
                    "income": [],
                    "expenses": [],
                    "debts": [],
                    "assets": [],
                    "investments": []
                }
        else:
            print(f"Data file '{self.data_file}' not found. Starting with empty data.")
            self.save_data() # Create an empty file for the first run

    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_income(self, date: str, source: str, amount: float, notes: str = None, recurring: bool = False):
        income_entry = {
            "id": self._get_next_id("income"),
            "date": date,
            "source": source,
            "amount": amount,
            "notes": notes,
            "recurring": bool(recurring)
        }
        self.data["income"].append(income_entry)
        print(f"Added income: {source} - {amount}")
        return income_entry["id"]

    def get_income(self):
        return self.data["income"]

    def update_income(self, income_id: int, date: str = None, source: str = None, amount: float = None, notes: str = None, recurring: bool = None):
        for entry in self.data["income"]:
            if entry["id"] == income_id:
                if date is not None: entry["date"] = date
                if source is not None: entry["source"] = source
                if amount is not None: entry["amount"] = amount
                if notes is not None: entry["notes"] = notes
                if recurring is not None: entry["recurring"] = bool(recurring)
                self.save_data()
                print(f"Updated income with ID {income_id}")
                return True
        print(f"Income with ID {income_id} not found.")
        return False

    def delete_item(self, category: str, item_id: int):
        if category not in self.data:
            print(f"Category '{category}' not found.")
            return False

        initial_len = len(self.data[category])
        self.data[category] = [item for item in self.data[category] if item["id"] != item_id]
        if len(self.data[category]) < initial_len:
            self.save_data()
            print(f"Deleted item with ID {item_id} from {category}.")
            return True
        print(f"Item with ID {item_id} not found in {category}.")
        return False

    def add_expense(self, date: str, category: str, amount: float, description: str = None, is_tax_deductible: bool = False, recurring: bool = False):
        expense_entry = {
            "id": self._get_next_id("expenses"),
            "date": date,
            "category": category,
            "amount": amount,
            "description": description,
            "is_tax_deductible": is_tax_deductible,
            "recurring": bool(recurring)
        }
        self.data["expenses"].append(expense_entry)
        print(f"Added expense: {category} - {amount}")
        return expense_entry["id"]

    def get_expenses(self):
        return self.data["expenses"]

    def add_receipt_to_expense(self, expense_id: int, filepath: str):
        """Attach a receipt file to an expense. Copies the file into a receipts folder and stores the path."""
        import shutil, os, time

        # Ensure receipts folder exists
        receipts_dir = os.path.join(os.path.dirname(self.data_file), 'receipts')
        os.makedirs(receipts_dir, exist_ok=True)

        # Create a unique filename to avoid collisions
        base = os.path.basename(filepath)
        timestamp = int(time.time() * 1000)
        dest_name = f"{timestamp}_{base}"
        dest_path = os.path.join(receipts_dir, dest_name)

        try:
            shutil.copy2(filepath, dest_path)
        except Exception as e:
            print(f"Failed to copy receipt file: {e}")
            return False

        # Find expense and attach
        for entry in self.data["expenses"]:
            if entry["id"] == expense_id:
                entry.setdefault('receipts', []).append(dest_path)
                self.save_data()
                print(f"Attached receipt to expense {expense_id}: {dest_path}")
                return True

        print(f"Expense with ID {expense_id} not found to attach receipt.")
        return False

    def get_receipts_for_expense(self, expense_id: int):
        for entry in self.data["expenses"]:
            if entry["id"] == expense_id:
                return entry.get('receipts', [])
        return []

    def remove_receipt_from_expense(self, expense_id: int, receipt_path: str, delete_file: bool = False) -> bool:
        """Remove a receipt reference from an expense. Optionally delete the file from disk."""
        for entry in self.data["expenses"]:
            if entry["id"] == expense_id:
                receipts = entry.get('receipts', [])
                if receipt_path in receipts:
                    receipts.remove(receipt_path)
                    entry['receipts'] = receipts
                    # Optionally remove the actual file
                    if delete_file:
                        try:
                            if os.path.exists(receipt_path):
                                os.remove(receipt_path)
                        except Exception:
                            pass
                    self.save_data()
                    print(f"Removed receipt from expense {expense_id}: {receipt_path}")
                    return True
                return False
        return False

    def update_expense(self, expense_id: int, date: str = None, category: str = None, amount: float = None, description: str = None, is_tax_deductible: bool = None, recurring: bool = None):
        for entry in self.data["expenses"]:
            if entry["id"] == expense_id:
                if date is not None: entry["date"] = date
                if category is not None: entry["category"] = category
                if amount is not None: entry["amount"] = amount
                if description is not None: entry["description"] = description
                if is_tax_deductible is not None: entry["is_tax_deductible"] = is_tax_deductible
                if recurring is not None: entry["recurring"] = bool(recurring)
                self.save_data()
                print(f"Updated expense with ID {expense_id}")
                return True
        print(f"Expense with ID {expense_id} not found.")
        return False

    def _get_next_id(self, category: str):
        # Generate a simple incremental ID for new entries
        if not self.data[category]:
            return 1
        return max(item["id"] for item in self.data[category]) + 1

    # Placeholder methods for other categories (to be implemented)
    def add_debt(self, name: str, debt_type: str, original_amount: float, current_amount: float, interest_rate: float, minimum_payment: float, due_date: str, notes: str = None):
        debt_entry = {
            "id": self._get_next_id("debts"),
            "name": name,
            "type": debt_type,
            "original_amount": original_amount,
            "current_amount": current_amount,
            "interest_rate": interest_rate,
            "minimum_payment": minimum_payment,
            "due_date": due_date,
            "notes": notes
        }
        self.data["debts"].append(debt_entry)
        print(f"Added debt: {name} - {current_amount}")
        return debt_entry["id"]

    def get_debts(self):
        return self.data["debts"]

    def update_debt(self, debt_id: int, name: str = None, debt_type: str = None, original_amount: float = None, current_amount: float = None, interest_rate: float = None, minimum_payment: float = None, due_date: str = None, notes: str = None):
        for entry in self.data["debts"]:
            if entry["id"] == debt_id:
                if name is not None: entry["name"] = name
                if debt_type is not None: entry["type"] = debt_type
                if original_amount is not None: entry["original_amount"] = original_amount
                if current_amount is not None: entry["current_amount"] = current_amount
                if interest_rate is not None: entry["interest_rate"] = interest_rate
                if minimum_payment is not None: entry["minimum_payment"] = minimum_payment
                if due_date is not None: entry["due_date"] = due_date
                if notes is not None: entry["notes"] = notes
                self.save_data()
                print(f"Updated debt with ID {debt_id}")
                return True
        print(f"Debt with ID {debt_id} not found.")
        return False

    def add_asset(self, name: str, asset_type: str, value: float, date_updated: str, notes: str = None):
        asset_entry = {
            "id": self._get_next_id("assets"),
            "name": name,
            "type": asset_type,
            "value": value,
            "date_updated": date_updated,
            "notes": notes
        }
        self.data["assets"].append(asset_entry)
        print(f"Added asset: {name} - {value}")
        return asset_entry["id"]

    def get_assets(self):
        return self.data["assets"]

    def update_asset(self, asset_id: int, name: str = None, asset_type: str = None, value: float = None, date_updated: str = None, notes: str = None):
        for entry in self.data["assets"]:
            if entry["id"] == asset_id:
                if name is not None: entry["name"] = name
                if asset_type is not None: entry["type"] = asset_type
                if value is not None: entry["value"] = value
                if date_updated is not None: entry["date_updated"] = date_updated
                if notes is not None: entry["notes"] = notes
                self.save_data()
                print(f"Updated asset with ID {asset_id}")
                return True
        print(f"Asset with ID {asset_id} not found.")
        return False

    def add_investment(self, name: str, investment_type: str, quantity: float, purchase_price: float, current_price: float, date_purchased: str, last_updated: str, notes: str = None, asset_id: int = None):
        investment_entry = {
            "id": self._get_next_id("investments"),
            "asset_id": asset_id,
            "name": name,
            "type": investment_type,
            "quantity": quantity,
            "purchase_price": purchase_price,
            "current_price": current_price,
            "date_purchased": date_purchased,
            "last_updated": last_updated,
            "notes": notes
        }
        self.data["investments"].append(investment_entry)
        print(f"Added investment: {name} - {current_price}")
        return investment_entry["id"]

    def get_investments(self):
        return self.data["investments"]

    def update_investment(self, investment_id: int, name: str = None, investment_type: str = None, quantity: float = None, purchase_price: float = None, current_price: float = None, date_purchased: str = None, last_updated: str = None, notes: str = None):
        for entry in self.data["investments"]:
            if entry["id"] == investment_id:
                if name is not None: entry["name"] = name
                if investment_type is not None: entry["type"] = investment_type
                if quantity is not None: entry["quantity"] = quantity
                if purchase_price is not None: entry["purchase_price"] = purchase_price
                if current_price is not None: entry["current_price"] = current_price
                if date_purchased is not None: entry["date_purchased"] = date_purchased
                if last_updated is not None: entry["last_updated"] = last_updated
                if notes is not None: entry["notes"] = notes
                self.save_data()
                print(f"Updated investment with ID {investment_id}")
                return True
        print(f"Investment with ID {investment_id} not found.")
        return False

    # Close method is no longer needed for database connection,
    # but can be used to ensure data is saved on app exit.
    def close(self):
        self.save_data()