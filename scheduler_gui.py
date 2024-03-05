import tkinter as tk
from tkinter import messagebox, ttk
import json
import subprocess

SPREAD_GEN_SCRIPT = 'spread_gen.py'

NATIONAL_HOLIDAYS = {
    'January': '1',
    'February': '',
    'March': '',
    'April': '',
    'May': '',
    'June': '19',
    'July': '4,24',
    'August': '',
    'September': '',
    'October': '',
    'November': '',
    'December': '24,25,31',
}

ENTRY_WIDTH = 25

class MentorSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Mentor Scheduler')

        tk.Button(self.root, text="Edit Mentor Info", command=self.edit_mentor_info).grid(row=0, columnspan=2)

        tk.Label(self.root, text="Schedule Name:").grid(row=1, column=0, sticky='e')
        self.schedule_name_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.schedule_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Year:").grid(row=2, column=0, sticky='e')
        self.year_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.year_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Month:").grid(row=3, column=0, sticky='e')
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.month_var = tk.StringVar()
        self.month_dropdown = ttk.Combobox(self.root, textvariable=self.month_var, values=self.months, state="readonly", width=ENTRY_WIDTH - 4)  # ttk.Combobox has different padding, hence the -4
        self.month_dropdown.bind('<<ComboboxSelected>>', self.on_month_changed)
        self.month_dropdown.grid(row=3, column=1)

        tk.Label(self.root, text="Holidays:").grid(row=4, column=0, sticky='e')
        self.holiday_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.holiday_entry.grid(row=4, column=1)

        tk.Button(self.root, text="Generate Schedule", command=self.generate_schedule).grid(row=5, columnspan=2)

    def on_month_changed(self, event):
        selected_month = self.month_var.get()
        holidays = NATIONAL_HOLIDAYS.get(selected_month, '')
        self.holiday_entry.delete(0, tk.END)
        self.holiday_entry.insert(0, holidays)

    def edit_mentor_info(self):
        with open('mentor_info.json', 'r') as file:
            self.mentor_data = json.load(file)

        self.mentor_names = ["New Mentor"] + list(self.mentor_data['mentor_info'].keys())

        self.edit_window = tk.Toplevel(self.root, width=ENTRY_WIDTH)
        self.edit_window.title("Edit Mentor Information")

        tk.Label(self.edit_window, text="Select Mentor:").grid(row=0, column=0, sticky='e')
        self.selected_mentor_var = tk.StringVar(self.edit_window)
        self.selected_mentor_var.set(self.mentor_names[0])  # Set to 'New Mentor'
        self.mentor_dropdown = ttk.Combobox(self.edit_window, textvariable=self.selected_mentor_var, values=self.mentor_names, state="readonly")
        self.mentor_dropdown.grid(row=0, column=1)
        self.mentor_dropdown.bind('<<ComboboxSelected>>', self.load_mentor_info)

        # Entry fields
        self.name_entry = self.create_label_entry("Name:", 1)
        self.hours_wanted_entry = self.create_label_entry("Hours wanted per week:", 2)
        self.hard_dates_entry = self.create_label_entry("Dates unavailable:", 3)
        tk.Label(self.edit_window, text="Weekdays unavailable:").grid(row=4, column=0, sticky='e')        
        self.weekdays_checkboxes = {}
        row = 4
        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            self.weekdays_checkboxes[day] = tk.BooleanVar()
            tk.Checkbutton(self.edit_window, text=day, variable=self.weekdays_checkboxes[day]).grid(row=row, column=1, sticky='w')
            row += 1
        self.save_button = tk.Button(self.edit_window, text="Save", command=self.save_mentor_info, width=20)
        self.save_button.grid(row=row + 1, columnspan=2)

    def create_label_entry(self, label_text, row):
        tk.Label(self.edit_window, text=label_text).grid(row=row, column=0, sticky='e')
        entry = tk.Entry(self.edit_window, width=ENTRY_WIDTH)
        entry.grid(row=row, column=1)
        return entry

    def load_mentor_info(self, event):
        selected_mentor_name = self.selected_mentor_var.get()
        if selected_mentor_name == "New Mentor":
            self.name_entry.delete(0, tk.END)
            self.hours_wanted_entry.delete(0, tk.END)
            self.hard_dates_entry.delete(0, tk.END)
            for day in self.weekdays_checkboxes:
                self.weekdays_checkboxes[day].set(False)
        else:
            mentor_info = self.mentor_data['mentor_info'][selected_mentor_name]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_mentor_name)
            self.hours_wanted_entry.delete(0, tk.END)
            self.hours_wanted_entry.insert(0, mentor_info.get('hours_wanted', ''))
            self.hard_dates_entry.delete(0, tk.END)
            self.hard_dates_entry.insert(0, ','.join(map(str, mentor_info.get('hard_dates', []))))
            for day in self.weekdays_checkboxes:
                self.weekdays_checkboxes[day].set(day in mentor_info.get('weekdays', []))

    def save_mentor_info(self):
        name = self.name_entry.get()
        weekdays = [day for day, var in self.weekdays_checkboxes.items() if var.get()]

        hard_date_entries = self.hard_dates_entry.get().split(',') if self.hard_dates_entry.get().strip() else []
        hard_dates = []
        for date_str in hard_date_entries:
            try:
                date = int(date_str.strip())
                hard_dates.append(date)
            except ValueError:
                messagebox.showerror("Error", f"Invalid date entry: '{date_str}'. Enter numbers for unavailable dates, separated by commas (no spaces.)")
                return

        hours_wanted = self.hours_wanted_entry.get().strip()
        if hours_wanted:
            try:
                hours_wanted = int(hours_wanted)
            except ValueError:
                messagebox.showerror("Error", f"Invalid entry for hours wanted: '{hours_wanted}'. Please enter a number.")
                return
        else:
            hours_wanted = 0

        if not name:
            messagebox.showerror("Error", "The name field cannot be empty.")
            return

        # By default, set weekday_behavior to 'Re'
        weekday_behavior = self.mentor_data['mentor_info'].get(name, {}).get('weekday_behavior', ['Re'])

        self.mentor_data['mentor_info'][name] = {
            "weekdays": weekdays,
            "weekday_behavior": weekday_behavior,
            "hard_dates": hard_dates,
            "hours_wanted": hours_wanted,
            "soft_dates": []
        }

        holiday_dates_str = self.holiday_entry.get().strip()
        if holiday_dates_str:
            holiday_dates = [int(date.strip()) for date in holiday_dates_str.split(',') if date.strip().isdigit()]
        else:
            holiday_dates = []
        self.mentor_data['holidays']['dates'] = holiday_dates
        with open('mentor_info.json', 'w') as file:
            json.dump(self.mentor_data, file, indent=4)

        messagebox.showinfo("Success", "Mentor information saved successfully.")
        self.edit_window.destroy()

    def generate_schedule(self):
        schedule_name = self.schedule_name_entry.get().strip()
        year = self.year_entry.get().strip()
        month_name = self.month_var.get().strip()

        holiday_dates_str = self.holiday_entry.get().strip()
        if holiday_dates_str:
            holiday_dates = [int(date.strip()) for date in holiday_dates_str.split(',') if date.strip().isdigit()]
        else:
            holiday_dates = []
        with open('mentor_info.json', 'r') as file:
            mentor_data = json.load(file)
        mentor_data['holidays']['dates'] = holiday_dates
        with open('mentor_info.json', 'w') as file:
            json.dump(mentor_data, file, indent=4)

        if not schedule_name:
            messagebox.showerror("Error", "Please enter a schedule name.")
            return
        if not year.isdigit() or len(year) != 4:
            messagebox.showerror("Error", "Please enter a valid year.")
            return
        if month_name not in self.months:
            messagebox.showerror("Error", "Please select a valid month.")
            return
        month = str(self.months.index(month_name) + 1)  # Convert month name to month number
        pay_period_length = '15'  # Hardcoded to always be 15
        try:
            subprocess.run(['python', SPREAD_GEN_SCRIPT, schedule_name, year, month, pay_period_length], check=True)
            messagebox.showinfo("Success", "Schedule generated successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to generate schedule. Error: {e}")
        except ValueError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    app = MentorSchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
