import tkinter as tk
from tkinter import ttk, messagebox, font # Import font module
from datetime import datetime

class TMTLabsGUI:
    def __init__(self, master, data_manager):
        self.master = master
        master.title("Financial Advisor- Your Smart Financial Assistant")
        master.geometry("1024x768") # Set a default window size

        self.data_manager = data_manager

        # --- Modern Styling ---
        style = ttk.Style()
        # Try to use a modern theme, fallback if not available
        available_themes = style.theme_names()
        if "clam" in available_themes:
            style.theme_use("clam")
        elif "alt" in available_themes:
            style.theme_use("alt")
        else:
            print("Modern themes 'clam' or 'alt' not found, using default.")

        # Define a larger font
        self.default_font = font.Font(family="TkDefaultFont", size=10) # Base font
        self.large_font = font.Font(family="TkDefaultFont", size=12) # For entries and labels
        self.heading_font = font.Font(family="TkDefaultFont", size=11, weight="bold") # For Treeview headings

        # Configure styles for various ttk widgets
        style.configure(".", font=self.default_font) # Apply default font to all widgets
        style.configure("TLabel", font=self.large_font)
        style.configure("TButton", font=self.large_font)
        style.configure("TEntry", font=self.large_font)
        style.configure("TCheckbutton", font=self.large_font)
        style.configure("TLabelframe.Label", font=self.heading_font) # For LabelFrame titles
        style.configure("TNotebook.Tab", font=self.large_font) # For notebook tabs

        # Configure Treeview styling for headers and rows
        style.configure("Treeview.Heading", font=self.heading_font)
        style.configure("Treeview", font=self.default_font) # Content of the treeview
        style.map("Treeview", background=[("selected", "grey")]) # Make selected row look modern
        # --- End Modern Styling ---


        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create frames for each tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.income_frame = ttk.Frame(self.notebook)
        self.expenses_frame = ttk.Frame(self.notebook)
        self.debts_frame = ttk.Frame(self.notebook)
        self.assets_frame = ttk.Frame(self.notebook)
        self.investments_frame = ttk.Frame(self.notebook)
        self.taxes_frame = ttk.Frame(self.notebook)
        self.analysis_frame = ttk.Frame(self.notebook)
        self.refinance_frame = ttk.Frame(self.notebook) # New Refinance Frame
        self.ira_frame = ttk.Frame(self.notebook) # New IRA Frame


        # Add frames as tabs to the notebook
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.income_frame, text="Income")
        self.notebook.add(self.expenses_frame, text="Expenses")
        self.notebook.add(self.debts_frame, text="Debts")
        self.notebook.add(self.assets_frame, text="Assets")
        self.notebook.add(self.investments_frame, text="Investments")
        self.notebook.add(self.taxes_frame, text="Taxes")
        self.notebook.add(self.analysis_frame, text="Analysis")
        self.notebook.add(self.refinance_frame, text="Refinance Calculator") # Add new tab
        self.notebook.add(self.ira_frame, text="IRA Calculator") # Add new IRA tab

        self._setup_dashboard()
        self._setup_income_tab()
        self._setup_expenses_tab()
        self._setup_refinance_calculator_tab() # Call new setup method
        self._setup_ira_tab() # Call new IRA setup method
        # More _setup_ methods will be added for other tabs later

    def _setup_dashboard(self):
        # Placeholder for Dashboard content
        ttk.Label(self.dashboard_frame, text="Welcome to your financial Advisor Dashboard!").pack(pady=20)
        ttk.Label(self.dashboard_frame, text="Summary of your finances will appear here.").pack()
        # This is where Matplotlib charts would eventually go

    def _setup_income_tab(self):
        # Input Frame for adding new income
        input_frame = ttk.LabelFrame(self.income_frame, text="Income Details", padding="10")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Date Input
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.income_date_entry = ttk.Entry(input_frame)
        self.income_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.income_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # Default to current date

        # Source Input
        ttk.Label(input_frame, text="Source:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.income_source_entry = ttk.Entry(input_frame)
        self.income_source_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Amount Input
        ttk.Label(input_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.income_amount_entry = ttk.Entry(input_frame)
        self.income_amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Notes Input
        ttk.Label(input_frame, text="Notes:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.income_notes_entry = ttk.Entry(input_frame)
        self.income_notes_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1) # Make the second column expandable

        # Action Buttons Frame
        action_buttons_frame = ttk.Frame(self.income_frame, padding="10")
        action_buttons_frame.pack(pady=5, padx=10, fill="x")

        ttk.Button(action_buttons_frame, text="Add Income", command=self._add_income).pack(side="left", padx=5)
        ttk.Button(action_buttons_frame, text="Edit Selected", command=self._edit_income_entry_from_button).pack(side="left", padx=5)
        ttk.Button(action_buttons_frame, text="Delete Selected", command=self._delete_income_entry_from_button).pack(side="left", padx=5)


        # Display Frame for income entries
        display_frame = ttk.LabelFrame(self.income_frame, text="All Income Entries", padding="10")
        display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "Date", "Source", "Amount", "Notes")
        self.income_tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.income_tree.pack(side="left", fill="both", expand=True)

        for col in columns:
            self.income_tree.heading(col, text=col)
            if col == "Amount":
                self.income_tree.column(col, anchor="e")
            else:
                self.income_tree.column(col, anchor="center")

        # Adjust specific column widths
        self.income_tree.column("ID", width=50, stretch=tk.NO)
        self.income_tree.column("Date", width=100, stretch=tk.NO)
        self.income_tree.column("Amount", width=100, stretch=tk.NO) # Amount alignment already set above

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.income_tree.yview)
        self.income_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # The _on_income_right_click method is commented out as it's no longer the primary interaction
        # self.income_tree.bind("<Button-3>", self._on_income_right_click)

        self._refresh_income_display() # Initial display of income

    def _add_income(self):
        date = self.income_date_entry.get()
        source = self.income_source_entry.get()
        amount_str = self.income_amount_entry.get()
        notes = self.income_notes_entry.get()

        if not date or not source or not amount_str:
            messagebox.showerror("Input Error", "Date, Source, and Amount cannot be empty.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.")
            return

        # Add income to data manager
        self.data_manager.add_income(date, source, amount, notes)
        self._refresh_income_display()

        # Clear input fields
        self.income_source_entry.delete(0, tk.END)
        self.income_amount_entry.delete(0, tk.END)
        self.income_notes_entry.delete(0, tk.END)
        self.income_date_entry.delete(0, tk.END)
        self.income_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # Reset date to current

    def _refresh_income_display(self):
        # Clear existing entries in the treeview
        for item in self.income_tree.get_children():
            self.income_tree.delete(item)

        # Get fresh data
        income_data = self.data_manager.get_income()

        # Sort by date, newest first (assuming date is YYYY-MM-DD for correct string comparison)
        income_data_sorted = sorted(income_data, key=lambda x: x['date'], reverse=True)

        # Insert new data
        for entry in income_data_sorted:
            self.income_tree.insert("", "end", iid=entry['id'], values=(entry['id'], entry['date'], entry['source'], f"{entry['amount']:.2f}", entry['notes']))

    def _on_income_right_click(self, event): # This method is now only called from context menu, which is removed
        item_id = self.income_tree.identify_row(event.y)
        if not item_id:
            return

        self.income_tree.selection_set(item_id)
        
        # Create a context menu
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Edit Income", command=lambda: self._edit_income_entry(int(item_id)))
        menu.add_command(label="Delete Income", command=lambda: self._delete_income_entry(int(item_id)))
        menu.post(event.x_root, event.y_root)

    def _get_selected_item_id(self, tree_widget):
        selected_item = tree_widget.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an item first.")
            return None
        return int(selected_item) # Treeview iid is the item ID

    def _edit_income_entry(self, income_id):
        # Retrieve the income entry data
        income_entry = next((item for item in self.data_manager.get_income() if item["id"] == income_id), None)
        if not income_entry:
            messagebox.showerror("Error", "Income entry not found.")
            return

        # Open a new dialog window for editing
        edit_dialog = EditIncomeDialog(self.master, income_entry, self.data_manager, self.large_font)
        self.master.wait_window(edit_dialog.top)
        self._refresh_income_display() # Refresh after dialog closes

    def _edit_income_entry_from_button(self):
        income_id = self._get_selected_item_id(self.income_tree)
        if income_id is not None:
            self._edit_income_entry(income_id)

    def _delete_income_entry(self, income_id):
        if messagebox.askyesno("Delete Income", f"Are you sure you want to delete income entry with ID {income_id}?"):
            if self.data_manager.delete_item("income", income_id):
                self._refresh_income_display()
            else:
                messagebox.showerror("Error", "Could not delete income entry.")

    def _delete_income_entry_from_button(self):
        income_id = self._get_selected_item_id(self.income_tree)
        if income_id is not None:
            self._delete_income_entry(income_id)

    def _setup_expenses_tab(self):
        # Input Frame for adding new expense
        input_frame = ttk.LabelFrame(self.expenses_frame, text="Expense Details", padding="10")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Date Input
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.expense_date_entry = ttk.Entry(input_frame)
        self.expense_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.expense_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # Default to current date

        # Category Input
        ttk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.expense_category_entry = ttk.Entry(input_frame) # Could be a Combobox with predefined categories later
        self.expense_category_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Amount Input
        ttk.Label(input_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.expense_amount_entry = ttk.Entry(input_frame)
        self.expense_amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Description Input
        ttk.Label(input_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.expense_description_entry = ttk.Entry(input_frame)
        self.expense_description_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Is Tax Deductible Checkbox
        self.is_tax_deductible_var = tk.BooleanVar(value=False)
        tax_deductible_checkbox = ttk.Checkbutton(input_frame, text="Tax Deductible", variable=self.is_tax_deductible_var)
        tax_deductible_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        input_frame.grid_columnconfigure(1, weight=1) # Make the second column expandable
        
        # Action Buttons Frame
        action_buttons_frame = ttk.Frame(self.expenses_frame, padding="10")
        action_buttons_frame.pack(pady=5, padx=10, fill="x")
        
        ttk.Button(action_buttons_frame, text="Add Expense", command=self._add_expense).pack(side="left", padx=5)
        ttk.Button(action_buttons_frame, text="Edit Selected", command=self._edit_expense_entry_from_button).pack(side="left", padx=5)
        ttk.Button(action_buttons_frame, text="Delete Selected", command=self._delete_expense_entry_from_button).pack(side="left", padx=5)

        # Display Frame for expense entries
        display_frame = ttk.LabelFrame(self.expenses_frame, text="All Expense Entries", padding="10")
        display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "Date", "Category", "Amount", "Description", "Tax Deductible")
        self.expense_tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.expense_tree.pack(side="left", fill="both", expand=True)

        for col in columns:
            self.expense_tree.heading(col, text=col)
            if col == "Amount":
                self.expense_tree.column(col, anchor="e")
            else:
                self.expense_tree.column(col, anchor="center")

        # Adjust specific column widths
        self.expense_tree.column("ID", width=50, stretch=tk.NO)
        self.expense_tree.column("Date", width=100, stretch=tk.NO)
        self.expense_tree.column("Amount", width=100, stretch=tk.NO) # Amount alignment already set above
        self.expense_tree.column("Tax Deductible", width=100, stretch=tk.NO)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.expense_tree.yview)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._refresh_expense_display() # Initial display of expenses

    def _add_expense(self):
        date = self.expense_date_entry.get()
        category = self.expense_category_entry.get()
        amount_str = self.expense_amount_entry.get()
        description = self.expense_description_entry.get()
        is_tax_deductible = self.is_tax_deductible_var.get()

        if not date or not category or not amount_str:
            messagebox.showerror("Input Error", "Date, Category, and Amount cannot be empty.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.")
            return

        # Add expense to data manager
        self.data_manager.add_expense(date, category, amount, description, is_tax_deductible)
        self._refresh_expense_display()

        # Clear input fields
        self.expense_category_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)
        self.expense_description_entry.delete(0, tk.END)
        self.is_tax_deductible_var.set(False) # Reset checkbox
        self.expense_date_entry.delete(0, tk.END)
        self.expense_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # Reset date to current

    def _refresh_expense_display(self):
        # Clear existing entries in the treeview
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)

        # Get fresh data
        expense_data = self.data_manager.get_expenses()

        # Sort by date, newest first (assuming date is YYYY-MM-DD for correct string comparison)
        expense_data_sorted = sorted(expense_data, key=lambda x: x['date'], reverse=True)

        # Insert new data
        for entry in expense_data_sorted:
            self.expense_tree.insert("", "end", iid=entry['id'], values=(entry['id'], entry['date'], entry['category'], f"{entry['amount']:.2f}", entry['description'], "Yes" if entry['is_tax_deductible'] else "No"))

    def _on_expense_right_click(self, event):
        item_id = self.expense_tree.identify_row(event.y)
        if not item_id:
            return

        self.expense_tree.selection_set(item_id)
        
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Edit Expense", command=lambda: self._edit_expense_entry(int(item_id)))
        menu.add_command(label="Delete Expense", command=lambda: self._delete_expense_entry(int(item_id)))
        menu.post(event.x_root, event.y_root)

    def _edit_expense_entry(self, expense_id):
        expense_entry = next((item for item in self.data_manager.get_expenses() if item["id"] == expense_id), None)
        if not expense_entry:
            messagebox.showerror("Error", "Expense entry not found.")
            return

        edit_dialog = EditExpenseDialog(self.master, expense_entry, self.data_manager, self.large_font)
        self.master.wait_window(edit_dialog.top)
        self._refresh_expense_display()

    def _edit_expense_entry_from_button(self):
        expense_id = self._get_selected_item_id(self.expense_tree)
        if expense_id is not None:
            self._edit_expense_entry(expense_id)

    def _delete_expense_entry(self, expense_id):
        if messagebox.askyesno("Delete Expense", f"Are you sure you want to delete expense entry with ID {expense_id}?"):
            if self.data_manager.delete_item("expenses", expense_id):
                self._refresh_expense_display()
            else:
                messagebox.showerror("Error", "Could not delete expense entry.")

    def _delete_expense_entry_from_button(self):
        expense_id = self._get_selected_item_id(self.expense_tree)
        if expense_id is not None:
            self._delete_expense_entry(expense_id)

    # Add similar _setup_ methods for other tabs (debts, assets, investments, taxes, analysis)

    def _setup_refinance_calculator_tab(self):
        calc_frame = ttk.LabelFrame(self.refinance_frame, text="Refinance Calculator", padding="10")
        calc_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Input fields
        input_grid = ttk.Frame(calc_frame)
        input_grid.pack(pady=10, padx=10, fill="x")

        # Current Loan Balance
        ttk.Label(input_grid, text="Current Loan Balance:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.ref_balance_entry = ttk.Entry(input_grid)
        self.ref_balance_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        # Original Loan Term (Years)
        ttk.Label(input_grid, text="Original Loan Term (Years):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.ref_original_term_entry = ttk.Entry(input_grid)
        self.ref_original_term_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        # Original Interest Rate (%)
        ttk.Label(input_grid, text="Original Interest Rate (%):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.ref_original_rate_entry = ttk.Entry(input_grid)
        self.ref_original_rate_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        # New Interest Rate (%)
        ttk.Label(input_grid, text="New Interest Rate (%):").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.ref_new_rate_entry = ttk.Entry(input_grid)
        self.ref_new_rate_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        # New Loan Term (Years)
        ttk.Label(input_grid, text="New Loan Term (Years):").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.ref_new_term_entry = ttk.Entry(input_grid)
        self.ref_new_term_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        # Refinancing Costs
        ttk.Label(input_grid, text="Refinancing Costs:").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.ref_costs_entry = ttk.Entry(input_grid)
        self.ref_costs_entry.grid(row=5, column=1, padx=5, pady=2, sticky="ew")

        input_grid.grid_columnconfigure(1, weight=1)

        # Calculate Button
        ttk.Button(calc_frame, text="Calculate Refinance Savings", command=self._calculate_refinance).pack(pady=10)

        # Results Display
        results_frame = ttk.LabelFrame(calc_frame, text="Refinance Results", padding="10")
        results_frame.pack(pady=10, padx=10, fill="x")

        self.ref_original_payment_label = ttk.Label(results_frame, text="Original Monthly Payment: ")
        self.ref_original_payment_label.pack(anchor="w", pady=2)
        self.ref_new_payment_label = ttk.Label(results_frame, text="New Monthly Payment: ")
        self.ref_new_payment_label.pack(anchor="w", pady=2)
        self.ref_monthly_savings_label = ttk.Label(results_frame, text="Monthly Savings: ")
        self.ref_monthly_savings_label.pack(anchor="w", pady=2)
        self.ref_total_interest_saved_label = ttk.Label(results_frame, text="Total Interest Saved: ")
        self.ref_total_interest_saved_label.pack(anchor="w", pady=2)
        self.ref_breakeven_label = ttk.Label(results_frame, text="Break-even Point: ")
        self.ref_breakeven_label.pack(anchor="w", pady=2)

    def _calculate_refinance(self):
        try:
            current_balance = float(self.ref_balance_entry.get())
            original_term_years = int(self.ref_original_term_entry.get())
            original_rate_percent = float(self.ref_original_rate_entry.get())
            new_rate_percent = float(self.ref_new_rate_entry.get())
            new_term_years = int(self.ref_new_term_entry.get())
            refinance_costs = float(self.ref_costs_entry.get())

            # Convert annual rate percentage to monthly decimal
            original_monthly_rate = (original_rate_percent / 100) / 12
            new_monthly_rate = (new_rate_percent / 100) / 12

            # Calculate original monthly payment (for comparison, assuming original balance was for original term)
            # This is a simplification; a real calculator would need original loan amount and payments made
            # For now, we calculate payment based on current balance for the original terms remaining
            # Let's assume the current balance is what's left for the original terms if not specified
            original_monthly_payment = self._calculate_mortgage_payment(
                current_balance, original_monthly_rate, original_term_years * 12
            )

            # Calculate new monthly payment
            new_monthly_payment = self._calculate_mortgage_payment(
                current_balance + refinance_costs, new_monthly_rate, new_term_years * 12
            )

            monthly_savings = original_monthly_payment - new_monthly_payment
            
            # Total interest saved calculation is complex, depends on payments made etc.
            # Simplified: Compare total payments over new term vs. if old payment continued for new term.
            # This is not a perfect model, but gives an estimate.

            total_new_payments = new_monthly_payment * (new_term_years * 12)
            total_old_payments_if_continued = original_monthly_payment * (new_term_years * 12) # Assuming loan would run for new term
            
            # A more accurate model for total interest saved requires knowing original principal and how many payments
            # have already been made. For now, we'll consider difference in total payments over loan life.
            # If we assume `current_balance` is the remaining principal, then remaining interest on old loan
            # vs total interest on new loan:
            
            # Total interest on new loan
            total_interest_new_loan = (new_monthly_payment * new_term_years * 12) - current_balance - refinance_costs
            
            # Total interest remaining on original loan (simplified)
            total_interest_original_remaining = (original_monthly_payment * original_term_years * 12) - current_balance

            # Total interest saved (simplified)
            total_interest_saved = total_interest_original_remaining - total_interest_new_loan
            

            breakeven_months = refinance_costs / monthly_savings if monthly_savings > 0 else float('inf')

            self.ref_original_payment_label.config(text=f"Original Monthly Payment: ${original_monthly_payment:,.2f}")
            self.ref_new_payment_label.config(text=f"New Monthly Payment: ${new_monthly_payment:,.2f}")
            self.ref_monthly_savings_label.config(text=f"Monthly Savings: ${monthly_savings:,.2f}")
            self.ref_total_interest_saved_label.config(text=f"Total Interest Saved (Estimate): ${total_interest_saved:,.2f}")
            
            if breakeven_months == float('inf'):
                self.ref_breakeven_label.config(text="Break-even Point: Never (no monthly savings)")
            elif breakeven_months <= 0:
                 self.ref_breakeven_label.config(text="Break-even Point: Immediately (positive savings)")
            else:
                self.ref_breakeven_label.config(text=f"Break-even Point: {breakeven_months:.1f} months")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    @staticmethod
    def _calculate_mortgage_payment(principal, monthly_rate, num_payments):
        if monthly_rate == 0:
            return principal / num_payments
        else:
            # M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1]
            # M = monthly payment
            # P = principal loan amount
            # i = monthly interest rate
            # n = number of payments (loan term in months)
            return principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    
    def _setup_ira_tab(self):
        calc_frame = ttk.LabelFrame(self.ira_frame, text="IRA Projection Calculator", padding="10")
        calc_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Input fields
        input_grid = ttk.Frame(calc_frame)
        input_grid.pack(pady=10, padx=10, fill="x")

        # Current Age
        ttk.Label(input_grid, text="Current Age:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.ira_current_age_entry = ttk.Entry(input_grid)
        self.ira_current_age_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        # Retirement Age
        ttk.Label(input_grid, text="Retirement Age:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.ira_retirement_age_entry = ttk.Entry(input_grid)
        self.ira_retirement_age_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        # Current IRA Balance
        ttk.Label(input_grid, text="Current IRA Balance:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.ira_current_balance_entry = ttk.Entry(input_grid)
        self.ira_current_balance_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        # Annual Contribution
        ttk.Label(input_grid, text="Annual Contribution:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.ira_annual_contribution_entry = ttk.Entry(input_grid)
        self.ira_annual_contribution_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        # Annual Rate of Return (%)
        ttk.Label(input_grid, text="Annual Rate of Return (%):").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.ira_annual_rate_entry = ttk.Entry(input_grid)
        self.ira_annual_rate_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        input_grid.grid_columnconfigure(1, weight=1)

        # Calculate Button
        ttk.Button(calc_frame, text="Calculate IRA Projection", command=self._calculate_ira_projection).pack(pady=10)

        # Results Display
        results_frame = ttk.LabelFrame(calc_frame, text="Projection Results", padding="10")
        results_frame.pack(pady=10, padx=10, fill="x")

        self.ira_projected_balance_label = ttk.Label(results_frame, text="Projected Balance at Retirement: ")
        self.ira_projected_balance_label.pack(anchor="w", pady=2)
        self.ira_total_contributions_label = ttk.Label(results_frame, text="Total Contributions: ")
        self.ira_total_contributions_label.pack(anchor="w", pady=2)
        self.ira_total_interest_label = ttk.Label(results_frame, text="Total Interest Earned: ")
        self.ira_total_interest_label.pack(anchor="w", pady=2)

    def _calculate_ira_projection(self):
        try:
            current_age = int(self.ira_current_age_entry.get())
            retirement_age = int(self.ira_retirement_age_entry.get())
            current_balance = float(self.ira_current_balance_entry.get())
            annual_contribution = float(self.ira_annual_contribution_entry.get())
            annual_rate_percent = float(self.ira_annual_rate_entry.get())

            if current_age >= retirement_age:
                messagebox.showwarning("Input Error", "Retirement Age must be greater than Current Age.")
                return

            if annual_rate_percent < 0:
                messagebox.showwarning("Input Error", "Annual Rate of Return cannot be negative.")
                return

            years_to_retirement = retirement_age - current_age
            monthly_rate = (annual_rate_percent / 100) / 12
            monthly_contribution = annual_contribution / 12
            
            projected_balance = current_balance
            total_contributions = 0

            for year in range(years_to_retirement):
                # Account for existing balance growth
                projected_balance *= (1 + (annual_rate_percent / 100))
                # Account for annual contributions (simplified as lump sum at year end)
                # More accurately: monthly contributions compounding
                future_value_of_contributions = monthly_contribution * (((1 + monthly_rate)**12 - 1) / monthly_rate)
                projected_balance += future_value_of_contributions
                total_contributions += annual_contribution

            total_interest_earned = projected_balance - current_balance - total_contributions

            self.ira_projected_balance_label.config(text=f"Projected Balance at Retirement: ${projected_balance:,.2f}")
            self.ira_total_contributions_label.config(text=f"Total Contributions: ${total_contributions:,.2f}")
            self.ira_total_interest_label.config(text=f"Total Interest Earned: ${total_interest_earned:,.2f}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
class EditIncomeDialog:
    def __init__(self, parent, income_data, data_manager, font_setting):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Edit Income ID: {income_data['id']}")
        self.top.transient(parent) # Set to be on top of the parent window
        self.top.grab_set() # Make it modal

        self.income_data = income_data
        self.data_manager = data_manager
        self.font_setting = font_setting # Pass font setting for consistency

        # Apply font to dialog widgets
        style = ttk.Style()
        style.configure("TLabel", font=self.font_setting)
        style.configure("TEntry", font=self.font_setting)
        style.configure("TButton", font=self.font_setting)

        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Date Input
        ttk.Label(main_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(main_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.date_entry.insert(0, income_data["date"])

        # Source Input
        ttk.Label(main_frame, text="Source:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.source_entry = ttk.Entry(main_frame)
        self.source_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.source_entry.insert(0, income_data["source"])

        # Amount Input
        ttk.Label(main_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(main_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.amount_entry.insert(0, str(income_data["amount"]))

        # Notes Input
        ttk.Label(main_frame, text="Notes:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.notes_entry = ttk.Entry(main_frame)
        self.notes_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.notes_entry.insert(0, income_data["notes"] if income_data["notes"] else "")

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save Changes", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side="left", padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def _on_save(self):
        date = self.date_entry.get()
        source = self.source_entry.get()
        amount_str = self.amount_entry.get()
        notes = self.notes_entry.get()

        if not date or not source or not amount_str:
            messagebox.showerror("Input Error", "Date, Source, and Amount cannot be empty.", parent=self.top)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.", parent=self.top)
            return

        if self.data_manager.update_income(self.income_data["id"], date=date, source=source, amount=amount, notes=notes):
            messagebox.showinfo("Success", "Income updated successfully!", parent=self.top)
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Failed to update income.", parent=self.top)

class EditExpenseDialog:
    def __init__(self, parent, expense_data, data_manager, font_setting):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Edit Expense ID: {expense_data['id']}")
        self.top.transient(parent)
        self.top.grab_set()

        self.expense_data = expense_data
        self.data_manager = data_manager
        self.font_setting = font_setting

        style = ttk.Style()
        style.configure("TLabel", font=self.font_setting)
        style.configure("TEntry", font=self.font_setting)
        style.configure("TButton", font=self.font_setting)
        style.configure("TCheckbutton", font=self.font_setting)

        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Date Input
        ttk.Label(main_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(main_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.date_entry.insert(0, expense_data["date"])

        # Category Input
        ttk.Label(main_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.category_entry = ttk.Entry(main_frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.category_entry.insert(0, expense_data["category"])

        # Amount Input
        ttk.Label(main_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(main_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.amount_entry.insert(0, str(expense_data["amount"]))

        # Description Input
        ttk.Label(main_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(main_frame)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.description_entry.insert(0, expense_data["description"] if expense_data["description"] else "")

        # Is Tax Deductible Checkbox
        self.is_tax_deductible_var = tk.BooleanVar(value=expense_data["is_tax_deductible"])
        tax_deductible_checkbox = ttk.Checkbutton(main_frame, text="Tax Deductible", variable=self.is_tax_deductible_var)
        tax_deductible_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save Changes", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side="left", padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def _on_save(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount_str = self.amount_entry.get()
        description = self.description_entry.get()
        is_tax_deductible = self.is_tax_deductible_var.get()

        if not date or not category or not amount_str:
            messagebox.showerror("Input Error", "Date, Category, and Amount cannot be empty.", parent=self.top)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.", parent=self.top)
            return

        if self.data_manager.update_expense(self.expense_data["id"], date=date, category=category, amount=amount, description=description, is_tax_deductible=is_tax_deductible):
            messagebox.showinfo("Success", "Expense updated successfully!", parent=self.top)
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Failed to update expense.", parent=self.top)