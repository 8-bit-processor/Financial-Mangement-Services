import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog # Import font module and filedialog
from datetime import datetime, timedelta

# Optional Matplotlib for dashboard visuals
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except Exception:
    HAS_MATPLOTLIB = False
from collections import defaultdict


class Tooltip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def show(self, text, x, y):
        self.hide()
        try:
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = ttk.Label(tw, text=text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1)
            label.pack(ipadx=4, ipady=2)
        except Exception:
            self.hide()

    def hide(self):
        if self.tipwindow:
            try:
                self.tipwindow.destroy()
            except Exception:
                pass
            self.tipwindow = None

class TMTLabsGUI:
    def __init__(self, master, data_manager):
        self.master = master
        master.title("Financial Advisor- Your Smart Financial Assistant")
        master.geometry("1124x668") # Set a default window size

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
        self.reports_frame = ttk.Frame(self.notebook)
        self.refinance_frame = ttk.Frame(self.notebook) # New Refinance Frame
        self.ira_frame = ttk.Frame(self.notebook) # New IRA Frame
        self.retirement_frame = ttk.Frame(self.notebook) # Retirement Frame


        # Add frames as tabs to the notebook
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.income_frame, text="Income")
        self.notebook.add(self.expenses_frame, text="Expenses")
        self.notebook.add(self.debts_frame, text="Debts")
        self.notebook.add(self.assets_frame, text="Assets")
        self.notebook.add(self.investments_frame, text="Investments")
        self.notebook.add(self.taxes_frame, text="Taxes")
        self.notebook.add(self.reports_frame, text="Reports")
        self.notebook.add(self.analysis_frame, text="Analysis")
        self.notebook.add(self.refinance_frame, text="Refinance Calculator") # Add new tab
        self.notebook.add(self.ira_frame, text="IRA Calculator") # Add new IRA tab
        self.notebook.add(self.retirement_frame, text="Retirement") # Add Retirement tab

        self._setup_dashboard()
        self._setup_income_tab()
        self._setup_expenses_tab()
        self._setup_debts_tab()
        self._setup_assets_tab()
        self._setup_investments_tab()
        self._setup_taxes_tab()
        self._setup_analysis_tab()
        self._setup_reports_tab()
        self._setup_refinance_calculator_tab() # Call new setup method
        self._setup_ira_tab() # Call new IRA setup method
        self._setup_retirement_tab()

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

        # Recurring Checkbox
        self.income_recurring_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(input_frame, text="Recurring", variable=self.income_recurring_var).grid(row=4, column=0, columnspan=2, padx=5, pady=2, sticky="w")

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

        columns = ("ID", "Date", "Source", "Amount", "Notes", "Recurring")
        self.income_tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.income_tree.pack(side="left", fill="both", expand=True)

        # Tooltip for recurring column cells
        self._income_tooltip = Tooltip(self.income_tree)
        # recurring column is the last one
        self._income_recurring_col = f"#{len(columns)}"
        self.income_tree.bind('<Motion>', lambda e: self._on_tree_motion(e, self.income_tree, self._income_recurring_col, 'income'))
        self.income_tree.bind('<Leave>', lambda e: self._income_tooltip.hide())

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

        if not self._validate_date(date):
            messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
            return

        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a non-negative number.")
            return

        # Add income to data manager (include recurring flag)
        recurring_flag = getattr(self, 'income_recurring_var', tk.BooleanVar(value=False)).get()
        self.data_manager.add_income(date, source, amount, notes, recurring=recurring_flag)
        self._refresh_income_display()
        # update dashboard and analysis after income change
        try:
            self._refresh_dashboard()
            self._refresh_analysis_display()
        except Exception:
            pass

        # Clear input fields
        self.income_source_entry.delete(0, tk.END)
        self.income_amount_entry.delete(0, tk.END)
        self.income_notes_entry.delete(0, tk.END)
        try:
            self.income_recurring_var.set(False)
        except Exception:
            pass
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
            recurring_text = "Yes" if entry.get('recurring') else "No"
            self.income_tree.insert("", "end", iid=entry['id'], values=(entry['id'], entry['date'], entry['source'], f"{entry['amount']:.2f}", entry.get('notes',''), recurring_text))

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

    def _on_tree_motion(self, event, tree, recurring_col, kind):
        # Show tooltip when hovering over the Recurring column cells
        try:
            col = tree.identify_column(event.x)
            if col != recurring_col:
                if kind == 'income':
                    self._income_tooltip.hide()
                else:
                    self._expense_tooltip.hide()
                return
            row = tree.identify_row(event.y)
            if not row:
                if kind == 'income':
                    self._income_tooltip.hide()
                else:
                    self._expense_tooltip.hide()
                return
            vals = tree.item(row).get('values', [])
            # recurring column index
            try:
                idx = int(col.replace('#', '')) - 1
                val = vals[idx] if idx < len(vals) else ''
            except Exception:
                val = ''
            text = ("Recurring: This item repeats (used for projections).\n"
                    "Checked = recurring.\nWhen 'Exclude non-recurring items' is on, non-recurring items are ignored.")
            # show tooltip near mouse
            x = event.x_root + 12
            y = event.y_root + 12
            if kind == 'income':
                self._income_tooltip.show(text, x, y)
            else:
                self._expense_tooltip.show(text, x, y)
        except Exception:
            try:
                if kind == 'income':
                    self._income_tooltip.hide()
                else:
                    self._expense_tooltip.hide()
            except Exception:
                pass

    def _get_selected_item_id(self, tree_widget):
        selected_item = tree_widget.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an item first.")
            return None
        return int(selected_item) # Treeview iid is the item ID

    def _validate_date(self, date_str: str) -> bool:
        if not date_str:
            return False
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except Exception:
            return False

    def _on_tree_double_click(self, event, tree_widget, edit_callback):
        item_id = tree_widget.identify_row(event.y)
        if not item_id:
            return
        try:
            edit_callback(int(item_id))
        except Exception:
            return

    def _on_delete_key(self, event=None):
        # Try each tree to find selection and delete
        mapping = [
            (getattr(self, 'income_tree', None), lambda i: self._delete_income_entry(i)),
            (getattr(self, 'expense_tree', None), lambda i: self._delete_expense_entry(i)),
            (getattr(self, 'debt_tree', None), lambda i: self.data_manager.delete_item('debts', i) and self._refresh_debt_display()),
            (getattr(self, 'asset_tree', None), lambda i: self.data_manager.delete_item('assets', i) and self._refresh_asset_display()),
            (getattr(self, 'inv_tree', None), lambda i: self.data_manager.delete_item('investments', i) and self._refresh_investment_display()),
        ]
        for tree, deleter in mapping:
            if tree is None:
                continue
            sel = tree.focus()
            if sel:
                try:
                    item_id = int(sel)
                except Exception:
                    return
                if messagebox.askyesno("Delete", f"Delete item ID {item_id}?"):
                    deleter(item_id)
                return

    def _on_edit_key(self, event=None):
        # Edit selected item in the focused tree
        mapping = [
            (getattr(self, 'income_tree', None), lambda i: self._edit_income_entry(i)),
            (getattr(self, 'expense_tree', None), lambda i: self._edit_expense_entry(i)),
            (getattr(self, 'debt_tree', None), lambda i: self._edit_debt(i)),
            (getattr(self, 'asset_tree', None), lambda i: self._edit_asset(i)),
            (getattr(self, 'inv_tree', None), lambda i: self._edit_investment(i)),
        ]
        for tree, editor in mapping:
            if tree is None:
                continue
            sel = tree.focus()
            if sel:
                try:
                    item_id = int(sel)
                except Exception:
                    return
                editor(item_id)
                return

    def _setup_bindings(self):
        # Keyboard shortcuts
        try:
            self.master.bind('<Delete>', self._on_delete_key)
            self.master.bind('<Control-e>', self._on_edit_key)
            # Refresh with F5
            self.master.bind('<F5>', lambda e: (self._refresh_dashboard(), self._refresh_analysis_display()))
        except Exception:
            pass
        # Double click on rows to edit
        for name in ('income_tree','expense_tree','debt_tree','asset_tree','inv_tree'):
            tree = getattr(self, name, None)
            if tree is not None:
                if name == 'income_tree':
                    tree.bind('<Double-1>', lambda e, t=tree: self._on_tree_double_click(e, t, self._edit_income_entry))
                elif name == 'expense_tree':
                    tree.bind('<Double-1>', lambda e, t=tree: self._on_tree_double_click(e, t, self._edit_expense_entry))
                elif name == 'debt_tree':
                    tree.bind('<Double-1>', lambda e, t=tree: self._on_tree_double_click(e, t, self._edit_debt))
                elif name == 'asset_tree':
                    tree.bind('<Double-1>', lambda e, t=tree: self._on_tree_double_click(e, t, self._edit_asset))
                elif name == 'inv_tree':
                    tree.bind('<Double-1>', lambda e, t=tree: self._on_tree_double_click(e, t, self._edit_investment))

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
        try:
            self._refresh_dashboard()
            self._refresh_analysis_display()
        except Exception:
            pass

    def _edit_income_entry_from_button(self):
        income_id = self._get_selected_item_id(self.income_tree)
        if income_id is not None:
            self._edit_income_entry(income_id)

    def _delete_income_entry(self, income_id):
        if messagebox.askyesno("Delete Income", f"Are you sure you want to delete income entry with ID {income_id}?"):
            if self.data_manager.delete_item("income", income_id):
                self._refresh_income_display()
                try:
                    self._refresh_dashboard()
                    self._refresh_analysis_display()
                except Exception:
                    pass
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
        # Recurring Checkbox for expenses
        self.expense_recurring_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(input_frame, text="Recurring", variable=self.expense_recurring_var).grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        input_frame.grid_columnconfigure(1, weight=1) # Make the second column expandable
        
        # Action Buttons Frame
        action_buttons_frame = ttk.Frame(self.expenses_frame, padding="10")
        action_buttons_frame.pack(pady=5, padx=10, fill="x")
        
        ttk.Button(action_buttons_frame, text="Add Expense", command=self._add_expense).pack(side="left", padx=5)
        ttk.Button(action_buttons_frame, text="Edit Selected", command=self._edit_expense_entry_from_button).pack(side="left", padx=5)
        ttk.Button(action_buttons_frame, text="Delete Selected", command=self._delete_expense_entry_from_button).pack(side="left", padx=5)
        ttk.Button(action_buttons_frame, text="Attach Receipt", command=self._attach_receipt_to_selected_expense).pack(side="left", padx=5)
        ttk.Button(action_buttons_frame, text="View Receipts", command=self._view_receipts_for_selected_expense).pack(side="left", padx=5)

        # Display Frame for expense entries
        display_frame = ttk.LabelFrame(self.expenses_frame, text="All Expense Entries", padding="10")
        display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "Date", "Category", "Amount", "Description", "Tax Deductible", "Recurring")
        self.expense_tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.expense_tree.pack(side="left", fill="both", expand=True)

        # Tooltip for recurring column cells
        self._expense_tooltip = Tooltip(self.expense_tree)
        self._expense_recurring_col = f"#{len(columns)}"
        self.expense_tree.bind('<Motion>', lambda e: self._on_tree_motion(e, self.expense_tree, self._expense_recurring_col, 'expense'))
        self.expense_tree.bind('<Leave>', lambda e: self._expense_tooltip.hide())

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

    def _setup_debts_tab(self):
        input_frame = ttk.LabelFrame(self.debts_frame, text="Debt Details", padding="10")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Name
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.debt_name_entry = ttk.Entry(input_frame)
        self.debt_name_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        # Type
        ttk.Label(input_frame, text="Type:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.debt_type_entry = ttk.Entry(input_frame)
        self.debt_type_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        # Current Amount
        ttk.Label(input_frame, text="Current Amount:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.debt_current_amount_entry = ttk.Entry(input_frame)
        self.debt_current_amount_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        # Interest Rate
        ttk.Label(input_frame, text="Interest Rate (%):").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.debt_interest_entry = ttk.Entry(input_frame)
        self.debt_interest_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        # Minimum Payment
        ttk.Label(input_frame, text="Minimum Payment:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.debt_min_payment_entry = ttk.Entry(input_frame)
        self.debt_min_payment_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        # Due Date
        ttk.Label(input_frame, text="Due Date (YYYY-MM-DD):").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.debt_due_entry = ttk.Entry(input_frame)
        self.debt_due_entry.grid(row=5, column=1, padx=5, pady=2, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1)

        action_frame = ttk.Frame(self.debts_frame, padding="10")
        action_frame.pack(pady=5, padx=10, fill="x")
        ttk.Button(action_frame, text="Add Debt", command=self._add_debt).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Edit Selected", command=self._edit_debt_from_button).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self._delete_debt_from_button).pack(side="left", padx=5)

        display_frame = ttk.LabelFrame(self.debts_frame, text="All Debts", padding="10")
        display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "Name", "Type", "Current", "Interest", "Minimum", "Due", "Notes")
        self.debt_tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.debt_tree.pack(side="left", fill="both", expand=True)
        for col in columns:
            self.debt_tree.heading(col, text=col)
            self.debt_tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.debt_tree.yview)
        self.debt_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._refresh_debt_display()

    def _add_debt(self):
        try:
            name = self.debt_name_entry.get()
            debt_type = self.debt_type_entry.get()
            current_amount = float(self.debt_current_amount_entry.get()) if self.debt_current_amount_entry.get() else 0.0
            interest = float(self.debt_interest_entry.get()) if self.debt_interest_entry.get() else 0.0
            minimum = float(self.debt_min_payment_entry.get()) if self.debt_min_payment_entry.get() else 0.0
            due = self.debt_due_entry.get()
            if not name:
                messagebox.showerror("Input Error", "Name cannot be empty.")
                return
            if due and not self._validate_date(due):
                messagebox.showerror("Input Error", "Due Date must be in YYYY-MM-DD format.")
                return
            if current_amount < 0 or interest < 0 or minimum < 0:
                messagebox.showerror("Input Error", "Amounts and rates must be non-negative.")
                return
            self.data_manager.add_debt(name, debt_type, 0.0, current_amount, interest, minimum, due)
            self._refresh_debt_display()
            self.debt_name_entry.delete(0, tk.END)
            self.debt_type_entry.delete(0, tk.END)
            self.debt_current_amount_entry.delete(0, tk.END)
            self.debt_interest_entry.delete(0, tk.END)
            self.debt_min_payment_entry.delete(0, tk.END)
            self.debt_due_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for amounts.")

    def _refresh_debt_display(self):
        for item in self.debt_tree.get_children():
            self.debt_tree.delete(item)
        for d in sorted(self.data_manager.get_debts(), key=lambda x: x.get('id', 0)):
            self.debt_tree.insert("", "end", iid=d['id'], values=(d['id'], d['name'], d['type'], f"{d['current_amount']:.2f}", f"{d['interest_rate']:.2f}", f"{d['minimum_payment']:.2f}", d['due_date'], d.get('notes', '')))

    def _delete_debt_from_button(self):
        debt_id = self._get_selected_item_id(self.debt_tree)
        if debt_id is not None:
            if messagebox.askyesno("Delete Debt", f"Delete debt ID {debt_id}?"):
                if self.data_manager.delete_item('debts', debt_id):
                    self._refresh_debt_display()
                else:
                    messagebox.showerror("Error", "Could not delete debt.")

    def _edit_debt_from_button(self):
        debt_id = self._get_selected_item_id(self.debt_tree)
        if debt_id is not None:
            self._edit_debt(debt_id)

    def _edit_debt(self, debt_id):
        debt_entry = next((d for d in self.data_manager.get_debts() if d['id'] == debt_id), None)
        if not debt_entry:
            messagebox.showerror("Error", "Debt entry not found.")
            return
        dlg = EditDebtDialog(self.master, debt_entry, self.data_manager, self.large_font)
        self.master.wait_window(dlg.top)
        self._refresh_debt_display()

    def _setup_assets_tab(self):
        input_frame = ttk.LabelFrame(self.assets_frame, text="Asset Details", padding="10")
        input_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.asset_name_entry = ttk.Entry(input_frame)
        self.asset_name_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Type:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.asset_type_entry = ttk.Entry(input_frame)
        self.asset_type_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Value:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.asset_value_entry = ttk.Entry(input_frame)
        self.asset_value_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Date Updated (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.asset_date_entry = ttk.Entry(input_frame)
        self.asset_date_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1)

        action_frame = ttk.Frame(self.assets_frame, padding="10")
        action_frame.pack(pady=5, padx=10, fill="x")
        ttk.Button(action_frame, text="Add Asset", command=self._add_asset).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Edit Selected", command=self._edit_asset_from_button).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self._delete_asset_from_button).pack(side="left", padx=5)

        display_frame = ttk.LabelFrame(self.assets_frame, text="All Assets", padding="10")
        display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "Name", "Type", "Value", "Updated", "Notes")
        self.asset_tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.asset_tree.pack(side="left", fill="both", expand=True)
        for col in columns:
            self.asset_tree.heading(col, text=col)
            self.asset_tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.asset_tree.yview)
        self.asset_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._refresh_asset_display()

    def _add_asset(self):
        try:
            name = self.asset_name_entry.get()
            asset_type = self.asset_type_entry.get()
            value = float(self.asset_value_entry.get()) if self.asset_value_entry.get() else 0.0
            date_updated = self.asset_date_entry.get()
            if not name:
                messagebox.showerror("Input Error", "Name cannot be empty.")
                return
            if date_updated and not self._validate_date(date_updated):
                messagebox.showerror("Input Error", "Date Updated must be in YYYY-MM-DD format.")
                return
            if value < 0:
                messagebox.showerror("Input Error", "Value must be non-negative.")
                return
            self.data_manager.add_asset(name, asset_type, value, date_updated)
            self._refresh_asset_display()
            self.asset_name_entry.delete(0, tk.END)
            self.asset_type_entry.delete(0, tk.END)
            self.asset_value_entry.delete(0, tk.END)
            self.asset_date_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for value.")

    def _refresh_asset_display(self):
        for item in self.asset_tree.get_children():
            self.asset_tree.delete(item)
        for a in sorted(self.data_manager.get_assets(), key=lambda x: x.get('id', 0)):
            self.asset_tree.insert("", "end", iid=a['id'], values=(a['id'], a['name'], a['type'], f"{a['value']:.2f}", a['date_updated'], a.get('notes', '')))

    def _delete_asset_from_button(self):
        asset_id = self._get_selected_item_id(self.asset_tree)
        if asset_id is not None:
            if messagebox.askyesno("Delete Asset", f"Delete asset ID {asset_id}?"):
                if self.data_manager.delete_item('assets', asset_id):
                    self._refresh_asset_display()
                else:
                    messagebox.showerror("Error", "Could not delete asset.")

    def _edit_asset_from_button(self):
        asset_id = self._get_selected_item_id(self.asset_tree)
        if asset_id is not None:
            self._edit_asset(asset_id)

    def _edit_asset(self, asset_id):
        asset_entry = next((a for a in self.data_manager.get_assets() if a['id'] == asset_id), None)
        if not asset_entry:
            messagebox.showerror("Error", "Asset entry not found.")
            return
        dlg = EditAssetDialog(self.master, asset_entry, self.data_manager, self.large_font)
        self.master.wait_window(dlg.top)
        self._refresh_asset_display()

    def _setup_investments_tab(self):
        input_frame = ttk.LabelFrame(self.investments_frame, text="Investment Details", padding="10")
        input_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.inv_name_entry = ttk.Entry(input_frame)
        self.inv_name_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Type:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.inv_type_entry = ttk.Entry(input_frame)
        self.inv_type_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.inv_qty_entry = ttk.Entry(input_frame)
        self.inv_qty_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Purchase Price:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.inv_purchase_entry = ttk.Entry(input_frame)
        self.inv_purchase_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Current Price:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.inv_current_entry = ttk.Entry(input_frame)
        self.inv_current_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1)

        action_frame = ttk.Frame(self.investments_frame, padding="10")
        action_frame.pack(pady=5, padx=10, fill="x")
        ttk.Button(action_frame, text="Add Investment", command=self._add_investment).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Edit Selected", command=self._edit_investment_from_button).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self._delete_investment_from_button).pack(side="left", padx=5)

        display_frame = ttk.LabelFrame(self.investments_frame, text="All Investments", padding="10")
        display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "Name", "Type", "Quantity", "Purchase", "Current", "Notes")
        self.inv_tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.inv_tree.pack(side="left", fill="both", expand=True)
        for col in columns:
            self.inv_tree.heading(col, text=col)
            self.inv_tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.inv_tree.yview)
        self.inv_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._refresh_investment_display()

    def _setup_taxes_tab(self):
        # Taxes tab: list expenses for tax reporting and allow attaching receipts
        top = ttk.Frame(self.taxes_frame, padding="10")
        top.pack(fill="both", expand=True)

        ttk.Label(top, text="Tax-related Expenses", font=self.heading_font).pack(anchor="w")

        # Quick form to add common tax expenses
        form_frame = ttk.Frame(self.taxes_frame, padding="6")
        form_frame.pack(fill="x", padx=10, pady=6)

        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=4, pady=2, sticky='w')
        self.taxes_date_entry = ttk.Entry(form_frame, width=12)
        self.taxes_date_entry.grid(row=0, column=1, padx=4, pady=2, sticky='w')
        self.taxes_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        ttk.Label(form_frame, text="Tax Type:").grid(row=0, column=2, padx=4, pady=2, sticky='w')
        self.taxes_type_cb = ttk.Combobox(form_frame, values=['Income Tax','State Tax','Property Tax'], state='readonly', width=18)
        self.taxes_type_cb.grid(row=0, column=3, padx=4, pady=2, sticky='w')
        self.taxes_type_cb.set('Income Tax')
        # boolean var for deductible flag — create before using in handler
        self.taxes_deductible_var = tk.BooleanVar(value=False)
        # set default deductible flag depending on selected tax type
        def _on_tax_type_change(event=None):
            t = self.taxes_type_cb.get()
            # Property tax is often deductible (depending on locale) — default True
            if t == 'Property Tax':
                self.taxes_deductible_var.set(True)
            else:
                self.taxes_deductible_var.set(False)
        self.taxes_type_cb.bind('<<ComboboxSelected>>', _on_tax_type_change)
        # initialize checkbox according to default selection
        _on_tax_type_change()

        ttk.Label(form_frame, text="Amount:").grid(row=1, column=0, padx=4, pady=2, sticky='w')
        self.taxes_amount_entry = ttk.Entry(form_frame, width=12)
        self.taxes_amount_entry.grid(row=1, column=1, padx=4, pady=2, sticky='w')

        ttk.Label(form_frame, text="Description:").grid(row=1, column=2, padx=4, pady=2, sticky='w')
        self.taxes_desc_entry = ttk.Entry(form_frame, width=40)
        self.taxes_desc_entry.grid(row=1, column=3, padx=4, pady=2, sticky='w')

        ttk.Checkbutton(form_frame, text='Mark Deductible', variable=self.taxes_deductible_var).grid(row=2, column=1, padx=4, pady=4, sticky='w')

        ttk.Button(form_frame, text='Add Tax Expense', command=self._add_tax_expense_from_taxes).grid(row=2, column=3, padx=4, pady=4, sticky='e')

        # Split view: left = Tax Payments, right = Deductible Expenses
        panes = ttk.Panedwindow(self.taxes_frame, orient=tk.HORIZONTAL)
        panes.pack(fill="both", expand=True, padx=10, pady=10)

        # Left pane: Tax Payments
        left = ttk.Labelframe(panes, text='Tax Payments', padding=8)
        panes.add(left, weight=1)
        cols_pay = ("ID", "Date", "Type", "Amount", "Description")
        # total label for tax payments
        self.taxpayments_total_label = ttk.Label(left, text='Total: $0.00', font=self.large_font)
        self.taxpayments_total_label.pack(anchor='ne')
        self.taxpayments_tree = ttk.Treeview(left, columns=cols_pay, show='headings')
        self.taxpayments_tree.pack(side='left', fill='both', expand=True)
        for c in cols_pay:
            self.taxpayments_tree.heading(c, text=c)
            self.taxpayments_tree.column(c, anchor='center')
        self.taxpayments_tree.column('ID', width=50, stretch=tk.NO)
        self.taxpayments_tree.column('Date', width=100, stretch=tk.NO)
        self.taxpayments_tree.column('Amount', width=100, anchor='e', stretch=tk.NO)
        sb1 = ttk.Scrollbar(left, orient='vertical', command=self.taxpayments_tree.yview)
        self.taxpayments_tree.configure(yscrollcommand=sb1.set)
        sb1.pack(side='right', fill='y')

        left_btns = ttk.Frame(left, padding=6)
        left_btns.pack(fill='x')
        ttk.Button(left_btns, text='Attach Receipt', command=self._attach_receipt_to_taxpayment).pack(side='left', padx=4)
        ttk.Button(left_btns, text='View Receipts', command=self._view_receipts_for_taxpayment).pack(side='left', padx=4)
        ttk.Button(left_btns, text='Mark as Deductible', command=self._mark_taxpayment_as_deductible).pack(side='left', padx=4)

        # Right pane: Deductible Expenses
        right = ttk.Labelframe(panes, text='Deductible Expenses', padding=8)
        panes.add(right, weight=1)
        cols_ded = ("ID", "Date", "Category", "Amount", "Description")
        # total label for deductible expenses
        self.deductible_total_label = ttk.Label(right, text='Total: $0.00', font=self.large_font)
        self.deductible_total_label.pack(anchor='ne')
        
        
        self.deductible_tree = ttk.Treeview(right, columns=cols_ded, show='headings')
        self.deductible_tree = ttk.Treeview(right, columns=cols_ded, show='headings')
        self.deductible_tree.pack(side='left', fill='both', expand=True)
        for c in cols_ded:
            self.deductible_tree.heading(c, text=c)
            self.deductible_tree.column(c, anchor='center')
        self.deductible_tree.column('ID', width=50, stretch=tk.NO)
        self.deductible_tree.column('Date', width=100, stretch=tk.NO)
        self.deductible_tree.column('Amount', width=100, anchor='e', stretch=tk.NO)
        sb2 = ttk.Scrollbar(right, orient='vertical', command=self.deductible_tree.yview)
        self.deductible_tree.configure(yscrollcommand=sb2.set)
        sb2.pack(side='right', fill='y')

        right_btns = ttk.Frame(right, padding=6)
        right_btns.pack(fill='x')
        ttk.Button(right_btns, text='Attach Receipt', command=self._attach_receipt_to_deductible).pack(side='left', padx=4)
        ttk.Button(right_btns, text='View Receipts', command=self._view_receipts_for_deductible).pack(side='left', padx=4)
        ttk.Button(right_btns, text='Unmark Deductible', command=self._unmark_deductible).pack(side='left', padx=4)

        # Global refresh button
        btn_frame = ttk.Frame(self.taxes_frame, padding="4")
        btn_frame.pack(fill='x')
        ttk.Button(btn_frame, text='Refresh Taxes View', command=self._refresh_taxes_display).pack(side='left', padx=6)

        self._refresh_taxes_display()

    def _refresh_taxes_display(self):
        # Populate the taxes_expense_tree with current expenses
        # Refresh both Tax Payments and Deductible lists
        for tree in (getattr(self, 'taxpayments_tree', None), getattr(self, 'deductible_tree', None)):
            if tree is None:
                continue
            for item in tree.get_children():
                tree.delete(item)

        tax_payments = [e for e in self.data_manager.get_expenses() if e.get('category') in ('Income Tax', 'State Tax', 'Property Tax')]
        deductibles = [e for e in self.data_manager.get_expenses() if e.get('is_tax_deductible')]

        for entry in sorted(tax_payments, key=lambda x: x.get('date',''), reverse=True):
            try:
                self.taxpayments_tree.insert('', 'end', iid=entry['id'], values=(entry['id'], entry.get('date',''), entry.get('category',''), f"{entry.get('amount',0.0):.2f}", entry.get('description','')))
            except Exception:
                continue
        # update tax payments total
        try:
            total_tp = sum(float(e.get('amount', 0.0)) for e in tax_payments)
            self.taxpayments_total_label.config(text=f"Total: ${total_tp:,.2f}")
        except Exception:
            pass
        for entry in sorted(deductibles, key=lambda x: x.get('date',''), reverse=True):
            try:
                self.deductible_tree.insert('', 'end', iid=entry['id'], values=(entry['id'], entry.get('date',''), entry.get('category',''), f"{entry.get('amount',0.0):.2f}", entry.get('description','')))
            except Exception:
                continue
        # update deductible total
        try:
            total_d = sum(float(e.get('amount', 0.0)) for e in deductibles)
            self.deductible_total_label.config(text=f"Total: ${total_d:,.2f}")
        except Exception:
            pass

    def _attach_receipt_from_taxes(self):
        # Deprecated: kept for compatibility
        sel = getattr(self, 'taxpayments_tree', None)
        if sel is None:
            messagebox.showwarning("Not available", "Tax payments tree not available.")
            return
        cur = sel.focus()
        if not cur:
            messagebox.showwarning("Selection Error", "Please select an item in Tax Payments first.")
            return
        try:
            eid = int(cur)
        except Exception:
            messagebox.showerror("Error", "Invalid selection.")
            return
        self.expense_tree.selection_set(eid)
        self.expense_tree.focus(eid)
        self._attach_receipt_to_selected_expense()

    def _attach_receipt_to_taxpayment(self):
        cur = self.taxpayments_tree.focus()
        if not cur:
            messagebox.showwarning("Selection Error", "Please select a tax payment first.")
            return
        try:
            eid = int(cur)
        except Exception:
            messagebox.showerror("Error", "Invalid selection.")
            return
        self.expense_tree.selection_set(eid)
        self.expense_tree.focus(eid)
        self._attach_receipt_to_selected_expense()

    def _attach_receipt_to_deductible(self):
        cur = self.deductible_tree.focus()
        if not cur:
            messagebox.showwarning("Selection Error", "Please select a deductible expense first.")
            return
        try:
            eid = int(cur)
        except Exception:
            messagebox.showerror("Error", "Invalid selection.")
            return
        self.expense_tree.selection_set(eid)
        self.expense_tree.focus(eid)
        self._attach_receipt_to_selected_expense()

    def _add_tax_expense_from_taxes(self):
        date = self.taxes_date_entry.get()
        ttype = self.taxes_type_cb.get()
        amount_str = self.taxes_amount_entry.get()
        desc = self.taxes_desc_entry.get()
        is_deduct = self.taxes_deductible_var.get()
        if not date or not ttype or not amount_str:
            messagebox.showerror('Input Error', 'Date, Tax Type, and Amount are required.')
            return
        if not self._validate_date(date):
            messagebox.showerror('Input Error', 'Date must be in YYYY-MM-DD format.')
            return
        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror('Input Error', 'Amount must be a non-negative number.')
            return

        # Add expense to data manager with the selected category
        self.data_manager.add_expense(date, ttype, amount, desc, is_deduct)
        self._refresh_taxes_display()
        self._refresh_expense_display()
        # Clear small form
        self.taxes_amount_entry.delete(0, tk.END)
        self.taxes_desc_entry.delete(0, tk.END)

    def _mark_taxpayment_as_deductible(self):
        cur = self.taxpayments_tree.focus()
        if not cur:
            messagebox.showwarning('Selection Error', 'Select a tax payment first.')
            return
        try:
            eid = int(cur)
        except Exception:
            messagebox.showerror('Error', 'Invalid selection.')
            return
        # Mark the expense as deductible
        if self.data_manager.update_expense(eid, is_tax_deductible=True):
            messagebox.showinfo('Updated', 'Marked as deductible.')
            self._refresh_taxes_display()
            self._refresh_expense_display()
            try:
                self._refresh_dashboard()
                self._refresh_analysis_display()
            except Exception:
                pass
        else:
            messagebox.showerror('Error', 'Failed to update entry.')

    def _unmark_deductible(self):
        cur = self.deductible_tree.focus()
        if not cur:
            messagebox.showwarning('Selection Error', 'Select a deductible expense first.')
            return
        try:
            eid = int(cur)
        except Exception:
            messagebox.showerror('Error', 'Invalid selection.')
            return
        if self.data_manager.update_expense(eid, is_tax_deductible=False):
            messagebox.showinfo('Updated', 'Unmarked as deductible.')
            self._refresh_taxes_display()
            self._refresh_expense_display()
            try:
                self._refresh_dashboard()
                self._refresh_analysis_display()
            except Exception:
                pass
        else:
            messagebox.showerror('Error', 'Failed to update entry.')

    def _view_receipts_from_taxes(self):
        # Deprecated: view receipts for tax payments
        cur = getattr(self, 'taxpayments_tree', None)
        if cur is None:
            messagebox.showwarning("Not available", "Tax payments tree not available.")
            return
        sel = cur.focus()
        if not sel:
            messagebox.showwarning("Selection Error", "Please select an expense first.")
            return
        try:
            eid = int(sel)
        except Exception:
            messagebox.showerror("Error", "Invalid selection.")
            return
        self.expense_tree.selection_set(eid)
        self.expense_tree.focus(eid)
        self._view_receipts_for_selected_expense()

    def _view_receipts_for_taxpayment(self):
        cur = self.taxpayments_tree.focus()
        if not cur:
            messagebox.showwarning("Selection Error", "Please select a tax payment first.")
            return
        try:
            eid = int(cur)
        except Exception:
            messagebox.showerror("Error", "Invalid selection.")
            return
        self.expense_tree.selection_set(eid)
        self.expense_tree.focus(eid)
        self._view_receipts_for_selected_expense()

    def _view_receipts_for_deductible(self):
        cur = self.deductible_tree.focus()
        if not cur:
            messagebox.showwarning("Selection Error", "Please select a deductible expense first.")
            return
        try:
            eid = int(cur)
        except Exception:
            messagebox.showerror("Error", "Invalid selection.")
            return
        self.expense_tree.selection_set(eid)
        self.expense_tree.focus(eid)
        self._view_receipts_for_selected_expense()

    def _add_investment(self):
        try:
            name = self.inv_name_entry.get()
            inv_type = self.inv_type_entry.get()
            qty = float(self.inv_qty_entry.get()) if self.inv_qty_entry.get() else 0.0
            purchase = float(self.inv_purchase_entry.get()) if self.inv_purchase_entry.get() else 0.0
            current = float(self.inv_current_entry.get()) if self.inv_current_entry.get() else 0.0
            if not name:
                messagebox.showerror("Input Error", "Name cannot be empty.")
                return
            if qty < 0 or purchase < 0 or current < 0:
                messagebox.showerror("Input Error", "Quantity and prices must be non-negative.")
                return
            self.data_manager.add_investment(name, inv_type, qty, purchase, current, '', '')
            self._refresh_investment_display()
            self.inv_name_entry.delete(0, tk.END)
            self.inv_type_entry.delete(0, tk.END)
            self.inv_qty_entry.delete(0, tk.END)
            self.inv_purchase_entry.delete(0, tk.END)
            self.inv_current_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for amounts.")

    def _refresh_investment_display(self):
        for item in self.inv_tree.get_children():
            self.inv_tree.delete(item)
        for inv in sorted(self.data_manager.get_investments(), key=lambda x: x.get('id', 0)):
            self.inv_tree.insert("", "end", iid=inv['id'], values=(inv['id'], inv['name'], inv['type'], f"{inv['quantity']:.2f}", f"{inv['purchase_price']:.2f}", f"{inv['current_price']:.2f}", inv.get('notes', '')))

    def _delete_investment_from_button(self):
        inv_id = self._get_selected_item_id(self.inv_tree)
        if inv_id is not None:
            if messagebox.askyesno("Delete Investment", f"Delete investment ID {inv_id}?"):
                if self.data_manager.delete_item('investments', inv_id):
                    self._refresh_investment_display()
                else:
                    messagebox.showerror("Error", "Could not delete investment.")

    def _edit_investment_from_button(self):
        inv_id = self._get_selected_item_id(self.inv_tree)
        if inv_id is not None:
            self._edit_investment(inv_id)

    def _edit_investment(self, inv_id):
        inv_entry = next((i for i in self.data_manager.get_investments() if i['id'] == inv_id), None)
        if not inv_entry:
            messagebox.showerror("Error", "Investment entry not found.")
            return
        dlg = EditInvestmentDialog(self.master, inv_entry, self.data_manager, self.large_font)
        self.master.wait_window(dlg.top)
        self._refresh_investment_display()

    def _setup_analysis_tab(self):
        # Analysis summary and charts
        summary_frame = ttk.Frame(self.analysis_frame, padding="10")
        summary_frame.pack(fill="x")

        self.analysis_networth_label = ttk.Label(summary_frame, text="Net Worth: $")
        self.analysis_networth_label.pack(anchor="w")
        # Income/Expense summary labels
        self.analysis_income_total_label = ttk.Label(summary_frame, text="Total Income (range): $0.00")
        self.analysis_income_total_label.pack(anchor="w")
        self.analysis_expense_total_label = ttk.Label(summary_frame, text="Total Expenses (range): $0.00")
        self.analysis_expense_total_label.pack(anchor="w")
        self.analysis_balance_label = ttk.Label(summary_frame, text="Balance (Income - Expenses): $0.00")
        self.analysis_balance_label.pack(anchor="w")
        # Projection button
        proj_btn = ttk.Button(summary_frame, text="Project Annual Trajectory", command=self._project_annual_trajectory)
        proj_btn.pack(anchor='e', pady=4)
        # Option: exclude one-off / non-recurring items from projections
        self.exclude_one_off_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(summary_frame, text="Exclude non-recurring items", variable=self.exclude_one_off_var).pack(anchor='w')
        ttk.Label(summary_frame, text="Uses last 12 months; ignores future dates. 'Recurring' flag preferred.", font=self.default_font).pack(anchor='w')

        chart_frame = ttk.Frame(self.analysis_frame)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        if HAS_MATPLOTLIB:
            # three panels: expense distribution, investment chart, annual projection
            self.analysis_fig = plt.Figure(figsize=(9, 4), dpi=100)
            self.analysis_ax1 = self.analysis_fig.add_subplot(131)
            self.analysis_ax2 = self.analysis_fig.add_subplot(132)
            self.analysis_ax3 = self.analysis_fig.add_subplot(133)

            self.analysis_canvas = FigureCanvasTkAgg(self.analysis_fig, master=chart_frame)
            self.analysis_canvas.get_tk_widget().pack(fill="both", expand=True)

            ttk.Button(self.analysis_frame, text="Refresh Analysis", command=self._refresh_analysis_display).pack(pady=5)
            self._refresh_analysis_display()
        else:
            ttk.Label(chart_frame, text="Install matplotlib (pip install -r requirements.txt) to view analysis charts.").pack(padx=10, pady=10)

    def _setup_reports_tab(self):
        # Reports and exports
        top = ttk.Frame(self.reports_frame, padding="10")
        top.pack(fill="x")

        ttk.Label(top, text="Reports & Exports", font=self.heading_font).grid(row=0, column=0, sticky="w")

        # Date range inputs
        range_frame = ttk.Frame(self.reports_frame, padding="10")
        range_frame.pack(fill="x")

        ttk.Label(range_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.report_start_entry = ttk.Entry(range_frame)
        self.report_start_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(range_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.report_end_entry = ttk.Entry(range_frame)
        self.report_end_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        range_frame.grid_columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(self.reports_frame, padding="10")
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Export CSV", command=self._export_csv).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Preview Report", command=self._preview_report).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Export Excel", command=self._export_excel).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Export PDF", command=self._export_pdf).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Generate Tax Summary", command=self._generate_tax_summary).pack(side="left", padx=5)

        self.report_status_label = ttk.Label(self.reports_frame, text="")
        self.report_status_label.pack(fill="x", padx=10, pady=5)

    def _parse_date_range(self):
        start = self.report_start_entry.get().strip()
        end = self.report_end_entry.get().strip()
        start_dt = None
        end_dt = None
        try:
            if start:
                start_dt = datetime.strptime(start, '%Y-%m-%d')
            if end:
                end_dt = datetime.strptime(end, '%Y-%m-%d')
        except Exception:
            messagebox.showerror("Input Error", "Dates must be in YYYY-MM-DD format.")
            return None, None
        return start_dt, end_dt

    def _gather_report_data(self, start_dt=None, end_dt=None):
        # Returns dict of lists for income and expenses and other items
        incomes = self.data_manager.get_income()
        expenses = self.data_manager.get_expenses()
        debts = self.data_manager.get_debts()
        assets = self.data_manager.get_assets()
        investments = self.data_manager.get_investments()

        def in_range(item_date_str):
            if not item_date_str:
                return True
            try:
                d = datetime.strptime(item_date_str, '%Y-%m-%d')
            except Exception:
                return True
            if start_dt and d < start_dt:
                return False
            if end_dt and d > end_dt:
                return False
            return True

        inc_filtered = [i for i in incomes if in_range(i.get('date'))]
        exp_filtered = [e for e in expenses if in_range(e.get('date'))]

        return {
            'income': inc_filtered,
            'expenses': exp_filtered,
            'debts': debts,
            'assets': assets,
            'investments': investments
        }

    def _export_csv(self):
        try:
            import pandas as pd
        except Exception:
            messagebox.showerror("Missing Dependency", "Install pandas (pip install -r requirements.txt) to export reports.")
            return

        start_dt, end_dt = self._parse_date_range()
        if start_dt is None and end_dt is None and (self.report_start_entry.get().strip() or self.report_end_entry.get().strip()):
            return

        data = self._gather_report_data(start_dt, end_dt)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        # Income
        df_inc = pd.DataFrame(data['income'])
        df_exp = pd.DataFrame(data['expenses'])
        base = f"moneymind_report_{timestamp}"
        inc_file = base + "_income.csv"
        exp_file = base + "_expenses.csv"
        df_inc.to_csv(inc_file, index=False)
        df_exp.to_csv(exp_file, index=False)
        self.report_status_label.config(text=f"Exported CSV: {inc_file}, {exp_file}")
        messagebox.showinfo("Export Complete", f"Exported CSV files:\n{inc_file}\n{exp_file}")

    def _export_excel(self):
        try:
            import pandas as pd
        except Exception:
            messagebox.showerror("Missing Dependency", "Install pandas and openpyxl (pip install -r requirements.txt) to export Excel.")
            return

        start_dt, end_dt = self._parse_date_range()
        if start_dt is None and end_dt is None and (self.report_start_entry.get().strip() or self.report_end_entry.get().strip()):
            return

        data = self._gather_report_data(start_dt, end_dt)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        base = f"moneymind_report_{timestamp}.xlsx"

        # Create a report folder to hold receipts and other assets
        import os, shutil
        report_folder = f"moneymind_report_{timestamp}_files"
        receipts_folder = os.path.join(report_folder, 'receipts')
        os.makedirs(receipts_folder, exist_ok=True)


        # Copy all receipt files referenced in expenses into the report receipts folder
        def copy_receipts_for_list(exp_list, prefix):
            out = []
            for e in exp_list:
                exp_copy = e.copy()
                receipts = e.get('receipts', []) or []
                rel_paths = []
                for r in receipts:
                    try:
                        if os.path.exists(r):
                            dest_name = f"{prefix}_{e.get('id')}_{os.path.basename(r)}"
                            dest_path = os.path.join(receipts_folder, dest_name)
                            shutil.copy2(r, dest_path)
                            rel_paths.append(os.path.join('receipts', dest_name))
                    except Exception:
                        continue
                exp_copy['receipt_files'] = ';'.join(rel_paths)
                out.append(exp_copy)
            return out

        tax_payments = [e for e in data['expenses'] if e.get('category') in ('Income Tax', 'State Tax', 'Property Tax')]
        deductibles = [e for e in data['expenses'] if e.get('is_tax_deductible')]
        other_expenses = [e for e in data['expenses'] if e not in tax_payments and e not in deductibles]

        taxpayments_copy = copy_receipts_for_list(tax_payments, 'taxpay')
        deductibles_copy = copy_receipts_for_list(deductibles, 'ded')
        others_copy = copy_receipts_for_list(other_expenses, 'oth')

        with pd.ExcelWriter(base, engine='openpyxl') as writer:
            pd.DataFrame(data['income']).to_excel(writer, sheet_name='Income', index=False)
            pd.DataFrame(taxpayments_copy).to_excel(writer, sheet_name='TaxPayments', index=False)
            pd.DataFrame(deductibles_copy).to_excel(writer, sheet_name='DeductibleExpenses', index=False)
            pd.DataFrame(others_copy).to_excel(writer, sheet_name='OtherExpenses', index=False)
            pd.DataFrame(data['assets']).to_excel(writer, sheet_name='Assets', index=False)
            pd.DataFrame(data['debts']).to_excel(writer, sheet_name='Debts', index=False)
            pd.DataFrame(data['investments']).to_excel(writer, sheet_name='Investments', index=False)

        self.report_status_label.config(text=f"Exported Excel: {base} (+files in {report_folder})")
        messagebox.showinfo("Export Complete", f"Exported Excel file:\n{base}\nAdditional files copied to folder:\n{report_folder}")

    def _export_pdf(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
        except Exception:
            messagebox.showerror("Missing Dependency", "Install reportlab (pip install -r requirements.txt) to export PDF.")
            return

        start_dt, end_dt = self._parse_date_range()
        if start_dt is None and end_dt is None and (self.report_start_entry.get().strip() or self.report_end_entry.get().strip()):
            return

        data = self._gather_report_data(start_dt, end_dt)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        fname = f"moneymind_report_{timestamp}.pdf"

        doc = SimpleDocTemplate(fname, pagesize=letter)
        styles = getSampleStyleSheet()
        elems = []

        elems.append(Paragraph("MoneyMind Report", styles['Title']))
        elems.append(Spacer(1, 12))

        # Summary
        total_income = sum(float(i.get('amount', 0)) for i in data['income'])
        total_expenses = sum(float(e.get('amount', 0)) for e in data['expenses'])
        elems.append(Paragraph(f"Total Income: ${total_income:,.2f}", styles['Normal']))
        elems.append(Paragraph(f"Total Expenses: ${total_expenses:,.2f}", styles['Normal']))
        elems.append(Spacer(1, 12))

        # Expenses by category table
        exp_by_cat = {}
        for e in data['expenses']:
            cat = e.get('category', 'Uncategorized')
            exp_by_cat[cat] = exp_by_cat.get(cat, 0.0) + float(e.get('amount', 0))

        table_data = [["Category", "Amount"]]
        for k, v in exp_by_cat.items():
            table_data.append([k, f"${v:,.2f}"])

        t = Table(table_data, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey), ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),('ALIGN',(1,1),(-1,-1),'RIGHT'),('GRID',(0,0),(-1,-1),0.5,colors.black)]))
        elems.append(Paragraph("Expenses by Category", styles['Heading2']))
        elems.append(t)

        # Optionally include receipt images for expenses
        from reportlab.platypus import Image as RLImage

        # After table, include receipts (first image per expense) if present
        for e in data['expenses']:
            receipts = e.get('receipts', [])
            if receipts:
                elems.append(Spacer(1, 12))
                elems.append(Paragraph(f"Receipts for Expense ID {e.get('id')}: {e.get('description','')}", styles['Heading3']))
                # add first receipt image
                first = receipts[0]
                try:
                    img = RLImage(first)
                    img._restrictSize(400, 300)
                    elems.append(img)
                except Exception as ex:
                    elems.append(Paragraph(f"Could not embed image: {ex}", styles['Normal']))

        doc.build(elems)
        self.report_status_label.config(text=f"Exported PDF: {fname}")
        messagebox.showinfo("Export Complete", f"Exported PDF file:\n{fname}")

    def _generate_tax_summary(self):
        # Simple tax summary: total income, deductible expenses, estimated taxable income
        start_dt, end_dt = self._parse_date_range()
        if start_dt is None and end_dt is None and (self.report_start_entry.get().strip() or self.report_end_entry.get().strip()):
            return
        data = self._gather_report_data(start_dt, end_dt)
        total_income = sum(float(i.get('amount', 0)) for i in data['income'])
        deductible = sum(float(e.get('amount', 0)) for e in data['expenses'] if e.get('is_tax_deductible'))
        taxable = total_income - deductible
        txt = f"Total Income: ${total_income:,.2f}\nDeductible Expenses: ${deductible:,.2f}\nEstimated Taxable Income: ${taxable:,.2f}"
        self.report_status_label.config(text="Tax summary generated")
        messagebox.showinfo("Tax Summary", txt)

    def _preview_report(self):
        start_dt, end_dt = self._parse_date_range()
        if start_dt is None and end_dt is None and (self.report_start_entry.get().strip() or self.report_end_entry.get().strip()):
            return
        data = self._gather_report_data(start_dt, end_dt)

        top = tk.Toplevel(self.master)
        top.title("Report Preview")
        top.geometry("900x600")

        # Summary area
        summary_frame = ttk.Frame(top, padding=10)
        summary_frame.pack(fill='x')
        total_income = sum(float(i.get('amount', 0)) for i in data['income'])
        total_expenses = sum(float(e.get('amount', 0)) for e in data['expenses'])
        deductible = sum(float(e.get('amount', 0)) for e in data['expenses'] if e.get('is_tax_deductible'))
        ttk.Label(summary_frame, text=f"Total Income: ${total_income:,.2f}").pack(anchor='w')
        ttk.Label(summary_frame, text=f"Total Expenses: ${total_expenses:,.2f}").pack(anchor='w')
        ttk.Label(summary_frame, text=f"Deductible Expenses: ${deductible:,.2f}").pack(anchor='w')

        # Main panes: left lists, right preview
        main_panes = ttk.Panedwindow(top, orient=tk.HORIZONTAL)
        main_panes.pack(fill='both', expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_panes)
        right_frame = ttk.Frame(main_panes)
        main_panes.add(left_frame, weight=1)
        main_panes.add(right_frame, weight=2)

        # Income tree
        inc_label = ttk.Label(left_frame, text='Income')
        inc_label.pack(anchor='w')
        inc_tree = ttk.Treeview(left_frame, columns=("Date","Source","Amount"), show='headings', height=8)
        inc_tree.heading('Date', text='Date')
        inc_tree.heading('Source', text='Source')
        inc_tree.heading('Amount', text='Amount')
        inc_tree.pack(fill='x')
        for i in data['income']:
            inc_tree.insert('', 'end', values=(i.get('date',''), i.get('source',''), f"{float(i.get('amount',0)):.2f}"))

        # Expenses tree
        exp_label = ttk.Label(left_frame, text='Expenses')
        exp_label.pack(anchor='w', pady=(8,0))
        exp_tree = ttk.Treeview(left_frame, columns=("ID","Date","Category","Amount","Deductible"), show='headings', height=12)
        for c in ("ID","Date","Category","Amount","Deductible"):
            exp_tree.heading(c, text=c)
        exp_tree.pack(fill='both', expand=True)
        for e in data['expenses']:
            exp_tree.insert('', 'end', iid=e.get('id'), values=(e.get('id'), e.get('date',''), e.get('category',''), f"{float(e.get('amount',0)):.2f}", 'Yes' if e.get('is_tax_deductible') else 'No'))

        # Preview area (right): description + receipt preview
        preview_desc = ttk.Label(right_frame, text='Select an expense to preview details and receipts', wraplength=400, justify='left')
        preview_desc.pack(anchor='nw')
        preview_canvas_frame = ttk.Frame(right_frame)
        preview_canvas_frame.pack(fill='both', expand=True, pady=8)
        preview_label = ttk.Label(preview_canvas_frame, text='Receipt preview')
        preview_label.pack()

        thumb_refs = {}

        def _load_receipts_for_expense(exp_id):
            receipts = self.data_manager.get_receipts_for_expense(int(exp_id))
            # Clear preview
            preview_label.config(image='', text='')
            if not receipts:
                preview_label.config(text='No receipts for this expense')
                return
            # show first image if possible
            try:
                from PIL import Image, ImageTk
                import os
                first = receipts[0]
                if first.lower().endswith('.pdf'):
                    preview_label.config(text=f'PDF file: {os.path.basename(first)}')
                    return
                img = Image.open(first)
                img.thumbnail((400,300))
                photo = ImageTk.PhotoImage(img)
                thumb_refs[first] = photo
                preview_label.config(image=photo, text='')
            except Exception as ex:
                preview_label.config(text=f'Could not preview receipt: {ex}')

        def _on_expense_select(evt):
            w = evt.widget
            if not w.selection():
                return
            sel = w.selection()[0]
            e = w.item(sel)
            vals = e.get('values', [])
            exp_id = vals[0] if vals else None
            if exp_id is None:
                return
            # Update description
            entry = next((x for x in data['expenses'] if x.get('id') == int(exp_id)), None)
            if entry:
                preview_desc.config(text=f"Expense ID: {entry.get('id')}\nDate: {entry.get('date','')}\nCategory: {entry.get('category','')}\nAmount: ${float(entry.get('amount',0)):.2f}\nDescription: {entry.get('description','')}")
                _load_receipts_for_expense(exp_id)

        exp_tree.bind('<<TreeviewSelect>>', _on_expense_select)

        # Close button
        btn_frame = ttk.Frame(top, padding=8)
        btn_frame.pack(fill='x')
        ttk.Button(btn_frame, text='Close Preview', command=top.destroy).pack(side='right', padx=5)

    def _add_expense(self):
        date = self.expense_date_entry.get()
        category = self.expense_category_entry.get()
        amount_str = self.expense_amount_entry.get()
        description = self.expense_description_entry.get()
        is_tax_deductible = self.is_tax_deductible_var.get()
        if not date or not category or not amount_str:
            messagebox.showerror("Input Error", "Date, Category, and Amount cannot be empty.")
            return

        if not self._validate_date(date):
            messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
            return

        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a non-negative number.")
            return

        # Add expense to data manager (include recurring flag)
        rec_flag = getattr(self, 'expense_recurring_var', tk.BooleanVar(value=False)).get()
        self.data_manager.add_expense(date, category, amount, description, is_tax_deductible, recurring=rec_flag)
        self._refresh_expense_display()
        # update dashboard and analysis after expense change
        try:
            self._refresh_dashboard()
            self._refresh_analysis_display()
        except Exception:
            pass

        # Clear input fields
        self.expense_category_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)
        self.expense_description_entry.delete(0, tk.END)
        self.is_tax_deductible_var.set(False) # Reset checkbox
        try:
            self.expense_recurring_var.set(False)
        except Exception:
            pass
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
            recurring_text = "Yes" if entry.get('recurring') else "No"
            self.expense_tree.insert("", "end", iid=entry['id'], values=(entry['id'], entry['date'], entry['category'], f"{entry['amount']:.2f}", entry.get('description',''), "Yes" if entry.get('is_tax_deductible') else "No", recurring_text))

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
        try:
            self._refresh_dashboard()
            self._refresh_analysis_display()
        except Exception:
            pass

    def _edit_expense_entry_from_button(self):
        expense_id = self._get_selected_item_id(self.expense_tree)
        if expense_id is not None:
            self._edit_expense_entry(expense_id)

    def _delete_expense_entry(self, expense_id):
        if messagebox.askyesno("Delete Expense", f"Are you sure you want to delete expense entry with ID {expense_id}?"):
            if self.data_manager.delete_item("expenses", expense_id):
                self._refresh_expense_display()
                try:
                    self._refresh_dashboard()
                    self._refresh_analysis_display()
                except Exception:
                    pass
            else:
                messagebox.showerror("Error", "Could not delete expense entry.")

    def _attach_receipt_to_selected_expense(self):
        expense_id = self._get_selected_item_id(self.expense_tree)
        if expense_id is None:
            return
        filepaths = filedialog.askopenfilenames(title="Select receipt files", filetypes=[("Images/PDF","*.png;*.jpg;*.jpeg;*.gif;*.pdf"), ("All files","*.*")])
        if not filepaths:
            return
        successes = 0
        for fp in filepaths:
            if self.data_manager.add_receipt_to_expense(expense_id, fp):
                successes += 1
        self._refresh_expense_display()
        messagebox.showinfo("Attach Receipts", f"Attached {successes} files to expense ID {expense_id}.")

    def _view_receipts_for_selected_expense(self):
        expense_id = self._get_selected_item_id(self.expense_tree)
        if expense_id is None:
            return
        receipts = self.data_manager.get_receipts_for_expense(expense_id)
        import os
        if not receipts:
            messagebox.showinfo("Receipts", "No receipts attached to this expense.")
            return

        top = tk.Toplevel(self.master)
        top.title(f"Receipts for Expense {expense_id}")
        lf = ttk.LabelFrame(top, text=f"Receipts ({len(receipts)})", padding="10")
        lf.pack(fill="both", expand=True)

        # Left: list of receipt files
        list_frame = ttk.Frame(lf)
        list_frame.pack(side="left", fill="y", padx=5, pady=5)
        listbox = tk.Listbox(list_frame, height=10, width=60)
        listbox.pack(side="left", fill="y", expand=False)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Right: preview area
        preview_frame = ttk.Frame(lf)
        preview_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        preview_label = ttk.Label(preview_frame, text="Preview will appear here")
        preview_label.pack()

        # Keep references to PhotoImage objects to prevent GC
        thumb_refs = {}

        def _load_preview(path):
            # Try to show an image thumbnail if Pillow is available
            try:
                from PIL import Image, ImageTk
            except Exception:
                preview_label.config(text=f"PIL not installed. File: {os.path.basename(path)}")
                return
            try:
                if path.lower().endswith('.pdf'):
                    preview_label.config(text=f"PDF file: {os.path.basename(path)}")
                    return
                img = Image.open(path)
                img.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(img)
                thumb_refs[path] = photo
                preview_label.config(image=photo, text='')
            except Exception as e:
                preview_label.config(text=f"Could not preview: {e}")

        for r in receipts:
            listbox.insert(tk.END, r)

        def _on_select(evt):
            w = evt.widget
            if not w.curselection():
                return
            idx = int(w.curselection()[0])
            path = w.get(idx)
            _load_preview(path)

        listbox.bind('<<ListboxSelect>>', _on_select)

        btn_frame = ttk.Frame(top, padding="8")
        btn_frame.pack(fill="x")

        def _open_selected():
            sel = listbox.curselection()
            if not sel:
                return
            path = listbox.get(sel[0])
            try:
                import os
                os.startfile(path)
            except Exception as e:
                messagebox.showerror("Open Error", f"Could not open file: {e}")

        def _remove_selected():
            sel = listbox.curselection()
            if not sel:
                return
            idx = int(sel[0])
            path = listbox.get(idx)
            if not messagebox.askyesno("Remove Receipt", f"Detach receipt from expense?\n{path}"):
                return
            try:
                ok = self.data_manager.remove_receipt_from_expense(expense_id, path, delete_file=False)
                if ok:
                    listbox.delete(idx)
                    preview_label.config(image='', text='Preview will appear here')
                    messagebox.showinfo("Removed", "Receipt detached from expense.")
                    self._refresh_expense_display()
                else:
                    messagebox.showerror("Error", "Could not remove receipt.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove receipt: {e}")

        ttk.Button(btn_frame, text="Open", command=_open_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Remove (Detach)", command=_remove_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Close", command=top.destroy).pack(side="left", padx=5)

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

            # Compare total payments over the new term (simplified)
            
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

    def _setup_retirement_tab(self):
        frame = ttk.Frame(self.retirement_frame, padding=10)
        frame.pack(fill='both', expand=True)

        header = ttk.Label(frame, text='Retirement Projections', font=self.heading_font)
        header.pack(anchor='w')

        inputs = ttk.Frame(frame)
        inputs.pack(fill='x', pady=8)

        # Current age / retirement age
        ttk.Label(inputs, text='Current Age:').grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.ret_current_age = ttk.Entry(inputs)
        self.ret_current_age.grid(row=0, column=1, padx=5, pady=2, sticky='ew')

        ttk.Label(inputs, text='Retirement Age:').grid(row=0, column=2, padx=5, pady=2, sticky='w')
        self.ret_retire_age = ttk.Entry(inputs)
        self.ret_retire_age.grid(row=0, column=3, padx=5, pady=2, sticky='ew')

        # Current savings (prefill from assets+investments)
        ttk.Label(inputs, text='Current Savings:').grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.ret_current_savings = ttk.Entry(inputs)
        self.ret_current_savings.grid(row=1, column=1, padx=5, pady=2, sticky='ew')

        ttk.Label(inputs, text='Annual Contribution:').grid(row=1, column=2, padx=5, pady=2, sticky='w')
        self.ret_annual_contrib = ttk.Entry(inputs)
        self.ret_annual_contrib.grid(row=1, column=3, padx=5, pady=2, sticky='ew')

        # Expected rate and inflation
        ttk.Label(inputs, text='Expected Annual Return (%):').grid(row=2, column=0, padx=5, pady=2, sticky='w')
        self.ret_rate = ttk.Entry(inputs)
        self.ret_rate.grid(row=2, column=1, padx=5, pady=2, sticky='ew')

        ttk.Label(inputs, text='Inflation Rate (%):').grid(row=2, column=2, padx=5, pady=2, sticky='w')
        self.ret_inflation = ttk.Entry(inputs)
        self.ret_inflation.grid(row=2, column=3, padx=5, pady=2, sticky='ew')

        inputs.grid_columnconfigure(1, weight=1)
        inputs.grid_columnconfigure(3, weight=1)

        # Buttons
        btns = ttk.Frame(frame)
        btns.pack(fill='x', pady=6)
        ttk.Button(btns, text='Auto-fill from Data', command=self._ret_fill_from_data).pack(side='left', padx=5)
        ttk.Button(btns, text='Run Projection', command=self._run_retirement_projection).pack(side='left', padx=5)
        ttk.Button(btns, text='Run Scenario (+1% / -1%)', command=self._run_retirement_scenarios).pack(side='left', padx=5)

        # Output area
        output_frame = ttk.LabelFrame(frame, text='Projection Output', padding=8)
        output_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.ret_output_text = tk.Text(output_frame, height=8)
        self.ret_output_text.pack(fill='both', expand=True)

        # Chart area
        chart_frame = ttk.Frame(frame)
        chart_frame.pack(fill='both', expand=True)
        if HAS_MATPLOTLIB:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib.pyplot as plt
            self.ret_fig = plt.Figure(figsize=(6,3), dpi=100)
            self.ret_ax = self.ret_fig.add_subplot(111)
            self.ret_canvas = FigureCanvasTkAgg(self.ret_fig, master=chart_frame)
            self.ret_canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            ttk.Label(chart_frame, text='Install matplotlib to view projection charts.').pack()

    def _ret_fill_from_data(self):
        # Prefill current savings from assets + investments and a conservative annual contribution from recent income
        assets_total = sum(a.get('value',0.0) for a in self.data_manager.get_assets())
        inv_total = sum(inv.get('quantity',0.0) * inv.get('current_price',0.0) for inv in self.data_manager.get_investments())
        income_recent = self.data_manager.get_income()
        # Average annual income from available income entries
        annual_contrib = 0.0
        try:
            if income_recent:
                avg = sum(float(i.get('amount',0)) for i in income_recent) / max(1, len(income_recent))
                # assume monthly average -> annual
                annual_contrib = avg * 12 * 0.1 # default to 10% of annual income
        except Exception:
            annual_contrib = 0.0

        total = assets_total + inv_total
        self.ret_current_savings.delete(0, tk.END)
        self.ret_current_savings.insert(0, f"{total:.2f}")
        self.ret_annual_contrib.delete(0, tk.END)
        self.ret_annual_contrib.insert(0, f"{annual_contrib:.2f}")

    def _run_retirement_projection(self):
        try:
            current_age = int(self.ret_current_age.get())
            retire_age = int(self.ret_retire_age.get())
            years = retire_age - current_age
            if years <= 0:
                messagebox.showerror('Input Error', 'Retirement age must be greater than current age.')
                return
            P = float(self.ret_current_savings.get() or 0)
            C = float(self.ret_annual_contrib.get() or 0)
            r = float(self.ret_rate.get() or 5.0) / 100.0
            infl = float(self.ret_inflation.get() or 2.0) / 100.0

            # Compute yearly projections
            balances = []
            bal = P
            for y in range(1, years+1):
                bal = bal * (1 + r) + C
                balances.append(bal)

            real_balances = [b / ((1+infl)**i) for i,b in enumerate(balances, start=1)]

            final_nominal = balances[-1] if balances else P
            final_real = real_balances[-1] if real_balances else P

            self.ret_output_text.delete('1.0', tk.END)
            self.ret_output_text.insert(tk.END, f'Projection over {years} years\n')
            self.ret_output_text.insert(tk.END, f'Final (nominal): ${final_nominal:,.2f}\n')
            self.ret_output_text.insert(tk.END, f'Final (real, inflation-adjusted): ${final_real:,.2f}\n\n')
            self.ret_output_text.insert(tk.END, 'Year by year (real-adjusted):\n')
            for i, val in enumerate(real_balances, start=1):
                self.ret_output_text.insert(tk.END, f'Year {i}: ${val:,.2f}\n')

            if HAS_MATPLOTLIB:
                self.ret_ax.clear()
                years_x = list(range(current_age+1, retire_age+1))
                self.ret_ax.plot(years_x, balances, label='Nominal')
                self.ret_ax.plot(years_x, real_balances, label='Real (inflation-adjusted)')
                self.ret_ax.set_title('Retirement Projection')
                self.ret_ax.set_xlabel('Age')
                self.ret_ax.set_ylabel('Balance')
                self.ret_ax.legend()
                self.ret_fig.tight_layout()
                self.ret_canvas.draw()

        except ValueError:
            messagebox.showerror('Input Error', 'Please enter valid numeric inputs for projection.')

    def _run_retirement_scenarios(self):
        # Run baseline, +1%, -1% return scenarios and plot
        try:
            base_r = float(self.ret_rate.get() or 5.0) / 100.0
            rates = [base_r - 0.01, base_r, base_r + 0.01]
            labels = [f'{(base_r-0.01)*100:.1f}%', f'{base_r*100:.1f}%', f'{(base_r+0.01)*100:.1f}%']
            current_age = int(self.ret_current_age.get())
            retire_age = int(self.ret_retire_age.get())
            years = retire_age - current_age
            P = float(self.ret_current_savings.get() or 0)
            C = float(self.ret_annual_contrib.get() or 0)
            infl = float(self.ret_inflation.get() or 2.0) / 100.0

            all_real = []
            ages = list(range(current_age+1, retire_age+1))
            for r in rates:
                bal = P
                balances = []
                for y in range(1, years+1):
                    bal = bal * (1 + r) + C
                    balances.append(bal)
                real_balances = [b / ((1+infl)**i) for i,b in enumerate(balances, start=1)]
                all_real.append(real_balances)

            self.ret_output_text.delete('1.0', tk.END)
            self.ret_output_text.insert(tk.END, 'Scenario comparison (final real values):\n')
            for lab, rl in zip(labels, all_real):
                self.ret_output_text.insert(tk.END, f'{lab}: ${rl[-1]:,.2f}\n')

            if HAS_MATPLOTLIB:
                self.ret_ax.clear()
                for lab, rl in zip(labels, all_real):
                    self.ret_ax.plot(ages, rl, label=lab)
                self.ret_ax.set_title('Scenario Comparison (Real Values)')
                self.ret_ax.set_xlabel('Age')
                self.ret_ax.set_ylabel('Inflation-adjusted Balance')
                self.ret_ax.legend()
                self.ret_fig.tight_layout()
                self.ret_canvas.draw()

        except Exception:
            messagebox.showerror('Error', 'Failed to run scenarios. Check inputs.')

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
    
    def _setup_dashboard(self):
        # Dashboard with quick summary and charts
        dashboard_top = ttk.Frame(self.dashboard_frame, padding="10")
        dashboard_top.pack(fill="x")

        self.dashboard_networth_label = ttk.Label(dashboard_top, text="Net Worth: $")
        self.dashboard_networth_label.pack(anchor="w")

        # Quick income/expense report (totals + recent items)
        report_frame = ttk.Frame(self.dashboard_frame, padding="6")
        report_frame.pack(fill='x', padx=10, pady=4)

        left_rf = ttk.Labelframe(report_frame, text='Income Summary', padding=6)
        left_rf.pack(side='left', fill='both', expand=True, padx=4)
        self.dashboard_income_total_label = ttk.Label(left_rf, text='Total Income: $0.00')
        self.dashboard_income_total_label.pack(anchor='w')
        cols_inc = ('ID','Date','Source','Amount')
        self.income_report_tree = ttk.Treeview(left_rf, columns=cols_inc, show='headings', height=5)
        for c in cols_inc:
            self.income_report_tree.heading(c, text=c)
        # set sensible column widths and anchors
        self.income_report_tree.column('ID', width=50, anchor='center', stretch=False)
        self.income_report_tree.column('Date', width=100, anchor='center', stretch=False)
        self.income_report_tree.column('Source', width=160, anchor='w')
        self.income_report_tree.column('Amount', width=90, anchor='e', stretch=False)
        # horizontal scrollbar for long text
        inc_xsb = ttk.Scrollbar(left_rf, orient='horizontal', command=self.income_report_tree.xview)
        self.income_report_tree.configure(xscrollcommand=inc_xsb.set)
        self.income_report_tree.pack(fill='both', expand=True)
        inc_xsb.pack(fill='x')

        right_rf = ttk.Labelframe(report_frame, text='Expense Summary', padding=6)
        right_rf.pack(side='left', fill='both', expand=True, padx=4)
        self.dashboard_expense_total_label = ttk.Label(right_rf, text='Total Expenses: $0.00')
        self.dashboard_expense_total_label.pack(anchor='w')
        cols_exp = ('ID','Date','Category','Amount')
        self.expense_report_tree = ttk.Treeview(right_rf, columns=cols_exp, show='headings', height=5)
        for c in cols_exp:
            self.expense_report_tree.heading(c, text=c)
        self.expense_report_tree.column('ID', width=50, anchor='center', stretch=False)
        self.expense_report_tree.column('Date', width=100, anchor='center', stretch=False)
        self.expense_report_tree.column('Category', width=160, anchor='w')
        self.expense_report_tree.column('Amount', width=90, anchor='e', stretch=False)
        exp_xsb = ttk.Scrollbar(right_rf, orient='horizontal', command=self.expense_report_tree.xview)
        self.expense_report_tree.configure(xscrollcommand=exp_xsb.set)
        self.expense_report_tree.pack(fill='both', expand=True)
        exp_xsb.pack(fill='x')
        # Balance label (Income - Expenses)
        self.dashboard_balance_label = ttk.Label(report_frame, text='Balance: $0.00')
        self.dashboard_balance_label.pack(side='right', padx=8)

        chart_frame = ttk.Frame(self.dashboard_frame)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if HAS_MATPLOTLIB:
            self.dashboard_fig = plt.Figure(figsize=(8, 4), dpi=100)
            self.db_ax1 = self.dashboard_fig.add_subplot(121)
            self.db_ax2 = self.dashboard_fig.add_subplot(122)

            self.dashboard_canvas = FigureCanvasTkAgg(self.dashboard_fig, master=chart_frame)
            self.dashboard_canvas.get_tk_widget().pack(fill="both", expand=True)

            ttk.Button(self.dashboard_frame, text="Refresh Dashboard", command=self._refresh_dashboard).pack(pady=5)
            self._refresh_dashboard()
        else:
            ttk.Label(chart_frame, text="Install matplotlib (pip install -r requirements.txt) to view dashboard charts.").pack(padx=10, pady=10)

    def _refresh_dashboard(self):
        if not HAS_MATPLOTLIB:
            return
        # Respect optional report date range so dashboard charts match reports
        start_dt, end_dt = None, None
        try:
            start_dt, end_dt = self._parse_date_range()
        except Exception:
            start_dt, end_dt = None, None

        # Compute net worth
        assets = sum(a.get('value', 0.0) for a in self.data_manager.get_assets())
        debts = sum(d.get('current_amount', 0.0) for d in self.data_manager.get_debts())
        networth = assets - debts
        self.dashboard_networth_label.config(text=f"Net Worth: ${networth:,.2f}")
        # Expenses by category (filtered by date range if provided)
        if start_dt is not None or end_dt is not None:
            report_data = self._gather_report_data(start_dt, end_dt)
            expenses = report_data.get('expenses', [])
            incomes = report_data.get('income', [])
        else:
            expenses = self.data_manager.get_expenses()
            incomes = self.data_manager.get_income()
        cat_totals = defaultdict(float)
        for e in expenses:
            cat_totals[e.get('category', 'Uncategorized')] += float(e.get('amount', 0.0))

        self.db_ax1.clear()
        if cat_totals:
            cats = list(cat_totals.keys())
            vals = [cat_totals[c] for c in cats]
            self.db_ax1.bar(cats, vals)
            self.db_ax1.set_title('Expenses by Category')
            self.db_ax1.tick_params(axis='x', rotation=45)
        else:
            self.db_ax1.text(0.5, 0.5, 'No expense data', ha='center')

        # Income over time (by date) — uses same date range as expenses when provided
        self.db_ax2.clear()
        incomes_sorted = sorted(incomes, key=lambda x: x.get('date', ''))
        if incomes_sorted:
            dates = [i['date'] for i in incomes_sorted]
            amounts = [float(i['amount']) for i in incomes_sorted]
            # aggregate by date
            date_totals = defaultdict(float)
            for d, a in zip(dates, amounts):
                date_totals[d] += a
            sorted_dates = sorted(date_totals.keys())
            vals = [date_totals[d] for d in sorted_dates]
            self.db_ax2.plot(sorted_dates, vals, marker='o')
            self.db_ax2.set_title('Income by Date')
            self.db_ax2.tick_params(axis='x', rotation=45)
        else:
            self.db_ax2.text(0.5, 0.5, 'No income data', ha='center')

        # Update dashboard income/expense totals and recent items
        try:
            # totals for displayed range
            total_income = sum(float(i.get('amount', 0.0)) for i in incomes)
            total_expenses = sum(float(e.get('amount', 0.0)) for e in expenses)
            self.dashboard_income_total_label.config(text=f"Total Income: ${total_income:,.2f}")
            self.dashboard_expense_total_label.config(text=f"Total Expenses: ${total_expenses:,.2f}")
            # balance display with sign and color
            bal = total_income - total_expenses
            sign = '+' if bal > 0 else ('-' if bal < 0 else '')
            bal_text = f"Balance: {sign}${abs(bal):,.2f}" if sign else f"Balance: ${abs(bal):,.2f}"
            try:
                # color: green positive, red negative, black zero
                fg = 'green' if bal > 0 else ('red' if bal < 0 else 'black')
                self.dashboard_balance_label.config(text=bal_text, foreground=fg)
            except Exception:
                try:
                    self.dashboard_balance_label.config(text=bal_text)
                except Exception:
                    pass

            # refresh recent incomes (most recent first)
            for iid in list(self.income_report_tree.get_children()):
                self.income_report_tree.delete(iid)
            inc_recent = sorted(incomes, key=lambda x: x.get('date',''), reverse=True)[:5]
            for inc in inc_recent:
                try:
                    self.income_report_tree.insert('', 'end', iid=inc.get('id'), values=(inc.get('id'), inc.get('date',''), inc.get('source',''), f"{float(inc.get('amount',0.0)):.2f}"))
                except Exception:
                    continue

            # refresh recent expenses (most recent first)
            for iid in list(self.expense_report_tree.get_children()):
                self.expense_report_tree.delete(iid)
            exp_recent = sorted(expenses, key=lambda x: x.get('date',''), reverse=True)[:5]
            for ex in exp_recent:
                try:
                    self.expense_report_tree.insert('', 'end', iid=ex.get('id'), values=(ex.get('id'), ex.get('date',''), ex.get('category',''), f"{float(ex.get('amount',0.0)):.2f}"))
                except Exception:
                    continue
        except Exception:
            pass

        self.dashboard_fig.tight_layout()
        self.dashboard_canvas.draw()

    def _refresh_analysis_display(self):
        if not HAS_MATPLOTLIB:
            return
        # Update net worth label
        assets = sum(a.get('value', 0.0) for a in self.data_manager.get_assets())
        debts = sum(d.get('current_amount', 0.0) for d in self.data_manager.get_debts())
        networth = assets - debts
        self.analysis_networth_label.config(text=f"Net Worth: ${networth:,.2f}")

        # Expenses by category pie
        expenses = self.data_manager.get_expenses()
        cat_totals = defaultdict(float)
        for e in expenses:
            cat_totals[e.get('category', 'Uncategorized')] += float(e.get('amount', 0.0))

        self.analysis_ax1.clear()
        if cat_totals:
            cats = list(cat_totals.keys())
            vals = [cat_totals[c] for c in cats]
            self.analysis_ax1.pie(vals, labels=cats, autopct='%1.1f%%')
            self.analysis_ax1.set_title('Expense Distribution')
        else:
            self.analysis_ax1.text(0.5, 0.5, 'No expense data', ha='center')

        # Investment value chart (simple current vs purchase)
        investments = self.data_manager.get_investments()
        self.analysis_ax2.clear()
        if investments:
            names = [inv['name'] for inv in investments]
            current_vals = [inv.get('quantity', 0.0) * inv.get('current_price', 0.0) for inv in investments]
            self.analysis_ax2.bar(names, current_vals)
            self.analysis_ax2.set_title('Investments Current Value')
            self.analysis_ax2.tick_params(axis='x', rotation=45)
        else:
            self.analysis_ax2.text(0.5, 0.5, 'No investments', ha='center')

        # Update income/expense totals shown in the summary (respecting report date range if set)
        try:
            start_dt, end_dt = self._parse_date_range()
        except Exception:
            start_dt, end_dt = None, None
        report = self._gather_report_data(start_dt, end_dt) if (start_dt or end_dt) else self._gather_report_data()
        inc_total = sum(float(i.get('amount', 0.0)) for i in report.get('income', []))
        exp_total = sum(float(e.get('amount', 0.0)) for e in report.get('expenses', []))
        balance = inc_total - exp_total
        try:
            self.analysis_income_total_label.config(text=f"Total Income (range): ${inc_total:,.2f}")
            self.analysis_expense_total_label.config(text=f"Total Expenses (range): ${exp_total:,.2f}")
            # show sign and color for analysis balance as well
            sign_a = '+' if balance > 0 else ('-' if balance < 0 else '')
            bal_text_a = f"Balance (Income - Expenses): {sign_a}${abs(balance):,.2f}" if sign_a else f"Balance (Income - Expenses): ${abs(balance):,.2f}"
            fg_a = 'green' if balance > 0 else ('red' if balance < 0 else 'black')
            self.analysis_balance_label.config(text=bal_text_a, foreground=fg_a)
        except Exception:
            try:
                self.analysis_balance_label.config(text=f"Balance (Income - Expenses): ${balance:,.2f}")
            except Exception:
                pass

        # Clear projection axis (projection drawn on-demand)
        try:
            if hasattr(self, 'analysis_ax3'):
                self.analysis_ax3.clear()
                self.analysis_ax3.text(0.5, 0.5, 'Click "Project Annual Trajectory"', ha='center')
        except Exception:
            pass

        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()
    def _project_annual_trajectory(self):
        # Compute simple annual projection using recent income/expense averages
        try:
            start_dt, end_dt = self._parse_date_range()
        except Exception:
            start_dt, end_dt = None, None
        data = self._gather_report_data(start_dt, end_dt)
        incomes = data.get('income', [])
        expenses = data.get('expenses', [])

        # Helper: determine months span
        def months_span(items):
            dates = [d.get('date') for d in items if d.get('date')]
            parsed = []
            for ds in dates:
                try:
                    parsed.append(datetime.strptime(ds, '%Y-%m-%d'))
                except Exception:
                    continue
            if not parsed:
                return 1
            earliest = min(parsed)
            latest = max(parsed)
            span = (latest.year - earliest.year) * 12 + (latest.month - earliest.month) + 1
            return max(1, span)

        # Apply rolling 12-month window (exclude future entries) and optional exclusion of non-recurring items
        now = datetime.now()
        window_start = now - timedelta(days=365)

        def _parse_date(item):
            ds = item.get('date')
            if not ds:
                return None
            try:
                return datetime.strptime(ds, '%Y-%m-%d')
            except Exception:
                return None

        incomes_window = []
        for i in incomes:
            d = _parse_date(i)
            if d and window_start <= d <= now:
                incomes_window.append(i)

        expenses_window = []
        for e in expenses:
            d = _parse_date(e)
            if d and window_start <= d <= now:
                expenses_window.append(e)

        # Optionally exclude non-recurring items based on simple heuristics
        def _is_recurring(item):
            # Prefer explicit flag if present
            if item.get('recurring') is True:
                return True
            if item.get('recurring') is False:
                # explicit False means non-recurring
                return False
            text = ' '.join([str(item.get(k, '')) for k in ('notes', 'source', 'category')]).lower()
            recurring_keywords = ['monthly', 'recurr', 'recurring', 'salary', 'paycheck', 'pension', 'ssi']
            return any(k in text for k in recurring_keywords)

        if getattr(self, 'exclude_one_off_var', None) and self.exclude_one_off_var.get():
            incomes_used = [i for i in incomes_window if _is_recurring(i)]
            expenses_used = [e for e in expenses_window if _is_recurring(e)]
        else:
            incomes_used = incomes_window
            expenses_used = expenses_window

        # Fallback: if filtering removed all data, use the original lists but still ignore future-dated entries
        if not incomes_used and not expenses_used:
            incomes_used = incomes_window or incomes
            expenses_used = expenses_window or expenses

        # Use a fixed 12-month denominator for rolling window averages
        months_denominator = 12

        total_inc = sum(float(i.get('amount', 0.0)) for i in incomes_used)
        total_exp = sum(float(e.get('amount', 0.0)) for e in expenses_used)
        avg_monthly_inc = total_inc / months_denominator
        avg_monthly_exp = total_exp / months_denominator
        monthly_net = avg_monthly_inc - avg_monthly_exp

        # Current net worth
        assets = sum(a.get('value', 0.0) for a in self.data_manager.get_assets())
        debts = sum(d.get('current_amount', 0.0) for d in self.data_manager.get_debts())
        current_net = assets - debts

        # Project 12 months
        months = list(range(1, 13))
        proj = []
        cum = current_net
        for m in months:
            cum += monthly_net
            proj.append(cum)

        # Plot on analysis_ax3
        if not HAS_MATPLOTLIB:
            messagebox.showerror('Missing Dependency', 'Install matplotlib to view projections.')
            return
        try:
            if not hasattr(self, 'analysis_ax3'):
                return
            self.analysis_ax3.clear()
            # Choose color based on monthly net (green for positive, red for negative, black for neutral)
            line_color = 'green' if monthly_net > 0 else ('red' if monthly_net < 0 else 'black')
            self.analysis_ax3.plot(months, proj, marker='o', color=line_color, markerfacecolor=line_color)
            self.analysis_ax3.set_title('Projected Net Worth (12 months)')
            self.analysis_ax3.set_xlabel('Months Ahead')
            self.analysis_ax3.set_ylabel('Net Worth ($)')
            # Tint y-axis and left spine to match projection color for visual cue
            try:
                self.analysis_ax3.tick_params(axis='y', colors=line_color)
                self.analysis_ax3.spines['left'].set_color(line_color)
            except Exception:
                pass
            # Annotate expected end-of-year change
            if proj:
                delta = proj[-1] - proj[0]
                self.analysis_ax3.annotate(f"Δ ${delta:,.2f}", xy=(12, proj[-1]), xytext=(8, proj[-1]), arrowprops=dict(arrowstyle='->', color=line_color), color=line_color)
            self.analysis_fig.tight_layout()
            self.analysis_canvas.draw()
            # Also update summary labels with annualized projections
            annual_inc = avg_monthly_inc * 12
            annual_exp = avg_monthly_exp * 12
            try:
                self.analysis_income_total_label.config(text=f"Total Income (range): ${total_inc:,.2f}  • Annualized: ${annual_inc:,.2f}")
                self.analysis_expense_total_label.config(text=f"Total Expenses (range): ${total_exp:,.2f}  • Annualized: ${annual_exp:,.2f}")
                self.analysis_balance_label.config(text=f"Balance (Income - Expenses): ${monthly_net:,.2f}/mo  • ${monthly_net*12:,.2f}/yr")
                try:
                    # Update net worth label to include projected 12-month net worth
                    if proj:
                        self.analysis_networth_label.config(text=f"Net Worth: ${current_net:,.2f}  • Projected (12mo): ${proj[-1]:,.2f}")
                    else:
                        self.analysis_networth_label.config(text=f"Net Worth: ${current_net:,.2f}")
                except Exception:
                    pass
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror('Error', f'Projection failed: {e}')
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

        # Recurring Checkbox
        self.recurring_var = tk.BooleanVar(value=income_data.get('recurring', False))
        ttk.Checkbutton(main_frame, text="Recurring", variable=self.recurring_var).grid(row=4, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save Changes", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side="left", padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def _on_save(self):
        date = self.date_entry.get()
        source = self.source_entry.get()
        amount_str = self.amount_entry.get()
        notes = self.notes_entry.get()
        recurring = self.recurring_var.get()

        if not date or not source or not amount_str:
            messagebox.showerror("Input Error", "Date, Source, and Amount cannot be empty.", parent=self.top)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.", parent=self.top)
            return

        if self.data_manager.update_income(self.income_data["id"], date=date, source=source, amount=amount, notes=notes, recurring=recurring):
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

        # Recurring Checkbox
        self.recurring_var = tk.BooleanVar(value=expense_data.get('recurring', False))
        ttk.Checkbutton(main_frame, text="Recurring", variable=self.recurring_var).grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save Changes", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side="left", padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def _on_save(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount_str = self.amount_entry.get()
        description = self.description_entry.get()
        is_tax_deductible = self.is_tax_deductible_var.get()
        recurring = self.recurring_var.get()

        if not date or not category or not amount_str:
            messagebox.showerror("Input Error", "Date, Category, and Amount cannot be empty.", parent=self.top)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.", parent=self.top)
            return

        if self.data_manager.update_expense(self.expense_data["id"], date=date, category=category, amount=amount, description=description, is_tax_deductible=is_tax_deductible, recurring=recurring):
            messagebox.showinfo("Success", "Expense updated successfully!", parent=self.top)
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Failed to update expense.", parent=self.top)


class EditDebtDialog:
    def __init__(self, parent, debt_data, data_manager, font_setting):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Edit Debt ID: {debt_data['id']}")
        self.top.transient(parent)
        self.top.grab_set()

        self.debt_data = debt_data
        self.data_manager = data_manager
        self.font_setting = font_setting

        style = ttk.Style()
        style.configure("TLabel", font=self.font_setting)
        style.configure("TEntry", font=self.font_setting)
        style.configure("TButton", font=self.font_setting)

        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(main_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.name_entry.insert(0, debt_data.get('name', ''))

        ttk.Label(main_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.type_entry = ttk.Entry(main_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.type_entry.insert(0, debt_data.get('type', ''))

        ttk.Label(main_frame, text="Current Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.current_entry = ttk.Entry(main_frame)
        self.current_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.current_entry.insert(0, str(debt_data.get('current_amount', 0.0)))

        ttk.Label(main_frame, text="Interest Rate (%):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.interest_entry = ttk.Entry(main_frame)
        self.interest_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.interest_entry.insert(0, str(debt_data.get('interest_rate', 0.0)))

        ttk.Label(main_frame, text="Minimum Payment:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.min_entry = ttk.Entry(main_frame)
        self.min_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.min_entry.insert(0, str(debt_data.get('minimum_payment', 0.0)))

        ttk.Label(main_frame, text="Due Date (YYYY-MM-DD):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.due_entry = ttk.Entry(main_frame)
        self.due_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.due_entry.insert(0, debt_data.get('due_date', ''))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Save Changes", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side="left", padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def _on_save(self):
        name = self.name_entry.get()
        debt_type = self.type_entry.get()
        try:
            current = float(self.current_entry.get()) if self.current_entry.get() else 0.0
            interest = float(self.interest_entry.get()) if self.interest_entry.get() else 0.0
            minimum = float(self.min_entry.get()) if self.min_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.", parent=self.top)
            return
        due = self.due_entry.get()
        if due:
            try:
                datetime.strptime(due, '%Y-%m-%d')
            except Exception:
                messagebox.showerror("Input Error", "Due Date must be in YYYY-MM-DD format.", parent=self.top)
                return

        if current < 0 or interest < 0 or minimum < 0:
            messagebox.showerror("Input Error", "Amounts must be non-negative.", parent=self.top)
            return

        if self.data_manager.update_debt(self.debt_data['id'], name=name, debt_type=debt_type, current_amount=current, interest_rate=interest, minimum_payment=minimum, due_date=due):
            messagebox.showinfo("Success", "Debt updated.", parent=self.top)
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Failed to update debt.", parent=self.top)


class EditAssetDialog:
    def __init__(self, parent, asset_data, data_manager, font_setting):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Edit Asset ID: {asset_data['id']}")
        self.top.transient(parent)
        self.top.grab_set()

        self.asset_data = asset_data
        self.data_manager = data_manager
        self.font_setting = font_setting

        style = ttk.Style()
        style.configure("TLabel", font=self.font_setting)
        style.configure("TEntry", font=self.font_setting)
        style.configure("TButton", font=self.font_setting)

        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(main_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.name_entry.insert(0, asset_data.get('name', ''))

        ttk.Label(main_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.type_entry = ttk.Entry(main_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.type_entry.insert(0, asset_data.get('type', ''))

        ttk.Label(main_frame, text="Value:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.value_entry = ttk.Entry(main_frame)
        self.value_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.value_entry.insert(0, str(asset_data.get('value', 0.0)))

        ttk.Label(main_frame, text="Date Updated (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(main_frame)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.date_entry.insert(0, asset_data.get('date_updated', ''))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Save Changes", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side="left", padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def _on_save(self):
        name = self.name_entry.get()
        asset_type = self.type_entry.get()
        try:
            value = float(self.value_entry.get()) if self.value_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for value.", parent=self.top)
            return
        date_updated = self.date_entry.get()
        if date_updated:
            try:
                datetime.strptime(date_updated, '%Y-%m-%d')
            except Exception:
                messagebox.showerror("Input Error", "Date Updated must be in YYYY-MM-DD format.", parent=self.top)
                return

        if value < 0:
            messagebox.showerror("Input Error", "Value must be non-negative.", parent=self.top)
            return

        if self.data_manager.update_asset(self.asset_data['id'], name=name, asset_type=asset_type, value=value, date_updated=date_updated):
            messagebox.showinfo("Success", "Asset updated.", parent=self.top)
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Failed to update asset.", parent=self.top)


class EditInvestmentDialog:
    def __init__(self, parent, inv_data, data_manager, font_setting):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Edit Investment ID: {inv_data['id']}")
        self.top.transient(parent)
        self.top.grab_set()

        self.inv_data = inv_data
        self.data_manager = data_manager
        self.font_setting = font_setting

        style = ttk.Style()
        style.configure("TLabel", font=self.font_setting)
        style.configure("TEntry", font=self.font_setting)
        style.configure("TButton", font=self.font_setting)

        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(main_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.name_entry.insert(0, inv_data.get('name', ''))

        ttk.Label(main_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.type_entry = ttk.Entry(main_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.type_entry.insert(0, inv_data.get('type', ''))

        ttk.Label(main_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.qty_entry = ttk.Entry(main_frame)
        self.qty_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.qty_entry.insert(0, str(inv_data.get('quantity', 0.0)))

        ttk.Label(main_frame, text="Purchase Price:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.purchase_entry = ttk.Entry(main_frame)
        self.purchase_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.purchase_entry.insert(0, str(inv_data.get('purchase_price', 0.0)))

        ttk.Label(main_frame, text="Current Price:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.current_entry = ttk.Entry(main_frame)
        self.current_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.current_entry.insert(0, str(inv_data.get('current_price', 0.0)))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Save Changes", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side="left", padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def _on_save(self):
        name = self.name_entry.get()
        inv_type = self.type_entry.get()
        try:
            qty = float(self.qty_entry.get()) if self.qty_entry.get() else 0.0
            purchase = float(self.purchase_entry.get()) if self.purchase_entry.get() else 0.0
            current = float(self.current_entry.get()) if self.current_entry.get() else 0.0
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.", parent=self.top)
            return
        if qty < 0 or purchase < 0 or current < 0:
            messagebox.showerror("Input Error", "Numbers must be non-negative.", parent=self.top)
            return

        if self.data_manager.update_investment(self.inv_data['id'], name=name, investment_type=inv_type, quantity=qty, purchase_price=purchase, current_price=current):
            messagebox.showinfo("Success", "Investment updated.", parent=self.top)
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Failed to update investment.", parent=self.top)