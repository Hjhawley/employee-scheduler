import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import subprocess

SPREAD_GEN_SCRIPT = 'spread_gen.py'

class MentorSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Mentor Scheduler')
        
        # Mentor Management Section
        tk.Button(self.root, text="Edit Mentor Info", command=self.edit_mentor_info).grid(row=0, columnspan=2)
        
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
        
        # Generate Button
        tk.Button(self.root, text="Generate Schedule", command=self.generate_schedule).grid(row=4, columnspan=2)

    def edit_mentor_info(self):
        # Open the JSON file and read the mentor information
        with open('mentor_db.json', 'r') as file:
            self.mentor_data = json.load(file)
        
        self.mentor_names = ["New Mentor"] + list(self.mentor_data['mentor_info'].keys())
        
        # Create a new window for editing mentor information
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Mentor Information")

        # Dropdown menu to select an existing mentor to edit
        tk.Label(self.edit_window, text="Select Mentor:").grid(row=0, column=0)
        self.selected_mentor_var = tk.StringVar(self.edit_window)
        self.selected_mentor_var.set(self.mentor_names[0])  # Set to 'New Mentor'
        self.mentor_dropdown = ttk.Combobox(self.edit_window, textvariable=self.selected_mentor_var, values=self.mentor_names, state="readonly")
        self.mentor_dropdown.grid(row=0, column=1)
        self.mentor_dropdown.bind('<<ComboboxSelected>>', self.load_mentor_info)

        # Entry fields for mentor information
        self.name_entry = self.create_label_entry("Name:", 1)
        tk.Label(self.edit_window, text="Weekdays unavailable:").grid(row=2, column=0, sticky='w', columnspan=2)        
        self.weekdays_checkboxes = {}
        row = 3
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            self.weekdays_checkboxes[day] = tk.BooleanVar()
            tk.Checkbutton(self.edit_window, text=day, variable=self.weekdays_checkboxes[day]).grid(row=row, column=0, sticky='w')
            row += 1
        
        self.hard_dates_entry = self.create_label_entry("Dates unavailable (comma separated):", row)
        row += 1
        self.hours_wanted_entry = self.create_label_entry("Hours Wanted:", row)
        row += 1
        
        # Save button to save edited information or add a new mentor
        self.save_button = tk.Button(self.edit_window, text="Save", command=self.save_mentor_info)
        self.save_button.grid(row=row + 1, column=1)

    def create_label_entry(self, label_text, row):
        tk.Label(self.edit_window, text=label_text).grid(row=row, column=0)
        entry = tk.Entry(self.edit_window)
        entry.grid(row=row, column=1)
        return entry

    def load_mentor_info(self, event):
        # Load the selected mentor's information into the entry fields for editing
        selected_mentor_name = self.selected_mentor_var.get()
        if selected_mentor_name == "New Mentor":
            self.name_entry.delete(0, tk.END)
            self.weekdays_entry.delete(0, tk.END)
            self.hard_dates_entry.delete(0, tk.END)
            self.hours_wanted_entry.delete(0, tk.END)
        else:
            mentor_info = self.mentor_data['mentor_info'][selected_mentor_name]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_mentor_name)
            for day in self.weekdays_checkboxes:
                self.weekdays_checkboxes[day].set(day in mentor_info.get('weekdays', []))
            self.hard_dates_entry.delete(0, tk.END)
            self.hard_dates_entry.insert(0, ','.join(map(str, mentor_info.get('hard_dates', []))))
            self.hours_wanted_entry.delete(0, tk.END)
            self.hours_wanted_entry.insert(0, mentor_info.get('hours_wanted', ''))

    def save_mentor_info(self):
        # Logic to save the edited information back to the JSON file
        name = self.name_entry.get()
        weekdays = [day for day, var in self.weekdays_checkboxes.items() if var.get()]
        hard_dates = [int(date.strip()) for date in self.hard_dates_entry.get().split(',') if date.strip()]
        hours_wanted = int(self.hours_wanted_entry.get()) if self.hours_wanted_entry.get().strip() else 0

        if not name:
            messagebox.showerror("Error", "The name field cannot be empty.")
            return

        # By default, set weekday_behavior to 'Re' if it is not already present
        weekday_behavior = self.mentor_data['mentor_info'].get(name, {}).get('weekday_behavior', ['Re'])

        # Replace or add the mentor information
        self.mentor_data['mentor_info'][name] = {
            "weekdays": weekdays,
            "weekday_behavior": weekday_behavior,
            "hard_dates": hard_dates,
            "hours_wanted": hours_wanted,
            "soft_dates": []
        }

        # Save the updated mentor data back to the JSON file
        with open('mentor_db.json', 'w') as file:
            json.dump(self.mentor_data, file, indent=4)

        messagebox.showinfo("Success", "Mentor information saved successfully.")
        self.edit_window.destroy()

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
