import tkinter as tk
from data_manager import DataManager
from gui import TMTLabsGUI

def main():
    # Initialize the database manager
    db_manager = DataManager()

    # Create the main Tkinter window
    root = tk.Tk()

    # Initialize the GUI with the main window and data manager
    app = TMTLabsGUI(root, db_manager)

    # Start the Tkinter event loop
    root.mainloop()

    # Ensure the database connection is closed when the application exits
    db_manager.close()

if __name__ == "__main__":
    main()
