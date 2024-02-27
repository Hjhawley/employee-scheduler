import tkinter as tk
from tkinter import messagebox, ttk
import subprocess

SPREAD_GEN_SCRIPT = 'spread_gen.py'

class MentorSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Mentor Scheduler')
        
        # Mentor Management Section
        tk.Button(self.root, text="Add/Edit Mentor Info", command=self.edit_mentor_info).grid(row=0, columnspan=2)
        
        # Schedule Name
        tk.Label(self.root, text="Schedule Name:").grid(row=1, column=0)
        self.schedule_name_entry = tk.Entry(self.root)
        self.schedule_name_entry.grid(row=1, column=1)
        
        # Year
        tk.Label(self.root, text="Year:").grid(row=2, column=0)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=2, column=1)
        
        # Month Dropdown Menu
        tk.Label(self.root, text="Month:").grid(row=3, column=0)
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.month_var = tk.StringVar()
        self.month_dropdown = ttk.Combobox(self.root, textvariable=self.month_var, values=self.months, state="readonly")
        self.month_dropdown.grid(row=3, column=1)
        self.month_var.set('January')  # Default value
        
        # Generate Button
        tk.Button(self.root, text="Generate Schedule", command=self.generate_schedule).grid(row=4, columnspan=2)

    def edit_mentor_info(self):
        # Placeholder for mentor info editing functionality
        messagebox.showinfo("Edit Mentor Info", "This feature is under construction.")

    def generate_schedule(self):
        schedule_name = self.schedule_name_entry.get()
        year = self.year_entry.get()
        month = str(self.months.index(self.month_var.get()) + 1)  # Convert month name to month number
        pay_period_length = '15'  # Hardcoded to always be 15
        
        # Call spread_gen.py with subprocess
        try:
            subprocess.run(['python', SPREAD_GEN_SCRIPT, schedule_name, year, month, pay_period_length], check=True)
            messagebox.showinfo("Success", "Schedule generated successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", "Failed to generate schedule.")

def main():
    root = tk.Tk()
    app = MentorSchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
