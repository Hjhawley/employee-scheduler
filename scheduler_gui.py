import tkinter as tk
from tkinter import messagebox, ttk
import json
import subprocess

SPREAD_GEN_SCRIPT = "spread_gen.py"

NATIONAL_HOLIDAYS = {
    "January": "1",
    "February": "",
    "March": "",
    "April": "",
    "May": "",
    "June": "19",
    "July": "4,24",
    "August": "",
    "September": "",
    "October": "",
    "November": "",
    "December": "24,25,31",
}

ENTRY_WIDTH = 30


class MentorSchedulerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Mentor Scheduler")

        tk.Button(
            self.root, text="Edit Mentor Info", command=self.edit_mentor_info
        ).grid(row=0, columnspan=2)

        tk.Label(self.root, text="Schedule Name:").grid(row=1, column=0, sticky="e")
        self.schedule_name_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.schedule_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Year:").grid(row=2, column=0, sticky="e")
        self.year_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.year_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Month:").grid(row=3, column=0, sticky="e")
        self.months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.month_var = tk.StringVar()
        self.month_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.month_var,
            values=self.months,
            state="readonly",
            width=ENTRY_WIDTH - 4,
        )  # ttk.Combobox has different padding, hence the -4
        self.month_dropdown.bind("<<ComboboxSelected>>", self.on_month_changed)
        self.month_dropdown.grid(row=3, column=1)

        tk.Label(self.root, text="Holidays:").grid(row=4, column=0, sticky="e")
        self.holiday_entry = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.holiday_entry.grid(row=4, column=1)

        tk.Button(
            self.root, text="Generate Schedule", command=self.generate_schedule
        ).grid(row=5, columnspan=2)

    def on_month_changed(self, event):
        selected_month = self.month_var.get()
        holidays = NATIONAL_HOLIDAYS.get(selected_month, "")
        self.holiday_entry.delete(0, tk.END)
        self.holiday_entry.insert(0, holidays)

    def edit_mentor_info(self):
        with open("mentor_info.json", "r") as file:
            self.mentor_data = json.load(file)

        self.mentor_names = ["New Mentor"] + list(
            self.mentor_data["mentor_info"].keys()
        )

        self.edit_window = tk.Toplevel(self.root, width=ENTRY_WIDTH)
        self.edit_window.title("Edit Mentor Information")

        tk.Label(self.edit_window, text="Select Mentor:").grid(
            row=0, column=0, sticky="e"
        )
        self.selected_mentor_var = tk.StringVar(self.edit_window)
        self.selected_mentor_var.set(self.mentor_names[0])  # Set to 'New Mentor'
        self.mentor_dropdown = ttk.Combobox(
            self.edit_window,
            textvariable=self.selected_mentor_var,
            values=self.mentor_names,
            state="readonly",
        )
        self.mentor_dropdown.grid(row=0, column=1)
        self.mentor_dropdown.bind("<<ComboboxSelected>>", self.load_mentor_info)

        # Entry fields for Name, Hours Wanted, Dates Unavailable
        self.name_entry = self.create_label_entry("Name:", 1)
        self.hours_wanted_entry = self.create_label_entry("Hours wanted per week:", 2)
        self.hard_dates_entry = self.create_label_entry("Dates unavailable:", 3)

        # Weekdays unavailable
        tk.Label(self.edit_window, text="Weekdays unavailable:").grid(
            row=4, column=0, sticky="e"
        )
        self.weekdays_checkboxes = {}
        row = 5
        for day in [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]:
            self.weekdays_checkboxes[day] = tk.BooleanVar()
            tk.Checkbutton(
                self.edit_window, text=day, variable=self.weekdays_checkboxes[day]
            ).grid(row=row, column=0, sticky="w")
            row += 1

        # Preferred Weekday (dropdown should be sufficient)
        tk.Label(self.edit_window, text="Prefers to work:").grid(
            row=row, column=0, sticky="e"
        )
        self.preferred_weekday_var = tk.StringVar()
        self.preferred_weekday_dropdown = ttk.Combobox(
            self.edit_window,
            textvariable=self.preferred_weekday_var,
            values=[
                "",
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ],
            state="readonly",
            width=ENTRY_WIDTH,
        )
        self.preferred_weekday_dropdown.grid(row=row, column=1)
        row += 1

        # Save and Delete buttons
        self.save_button = tk.Button(
            self.edit_window, text="Save", command=self.save_mentor_info, width=20
        )
        self.save_button.grid(row=row + 1, columnspan=2)
        self.delete_button = tk.Button(
            self.edit_window,
            text="Delete Mentor",
            command=self.delete_mentor_info,
            width=20,
        )
        self.delete_button.grid(row=row + 2, columnspan=2)

    def create_label_entry(self, label_text, row):
        tk.Label(self.edit_window, text=label_text).grid(row=row, column=0, sticky="e")
        entry = tk.Entry(self.edit_window)
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
            self.preferred_weekday_var.set("")
        else:
            mentor_info = self.mentor_data["mentor_info"][selected_mentor_name]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_mentor_name)
            self.hours_wanted_entry.delete(0, tk.END)
            self.hours_wanted_entry.insert(0, mentor_info.get("hours_wanted", ""))
            self.hard_dates_entry.delete(0, tk.END)
            self.hard_dates_entry.insert(
                0, ",".join(map(str, mentor_info.get("hard_dates", [])))
            )
            for day in self.weekdays_checkboxes:
                self.weekdays_checkboxes[day].set(
                    day in mentor_info.get("weekdays", [])
                )
            pref = mentor_info.get("preferred_weekdays", [])
            self.preferred_weekday_var.set(pref[0] if pref else "")

    def save_mentor_info(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "The name field cannot be empty.")
            return

        hours_wanted = self.get_validated_hours()
        if hours_wanted is None:
            return

        try:
            hard_dates = self.get_validated_dates(self.hard_dates_entry.get().strip())
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        weekdays = [day for day, var in self.weekdays_checkboxes.items() if var.get()]
        preferred_weekday = self.preferred_weekday_var.get().strip()
        preferred_weekdays = [preferred_weekday] if preferred_weekday else []

        # Set weekday_behavior to 'Re' by default
        weekday_behavior = (
            self.mentor_data["mentor_info"]
            .get(name, {})
            .get("weekday_behavior", ["Re"])
        )

        self.mentor_data["mentor_info"][name] = {
            "weekdays": weekdays,
            "preferred_weekdays": preferred_weekdays,
            "weekday_behavior": weekday_behavior,
            "hard_dates": hard_dates,
            "hours_wanted": hours_wanted,
            "soft_dates": [],
        }

        try:
            holiday_dates = self.get_validated_dates(self.holiday_entry.get().strip())
            self.mentor_data["holidays"]["dates"] = holiday_dates
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        with open("mentor_info.json", "w") as file:
            json.dump(self.mentor_data, file, indent=4)

        messagebox.showinfo("Success", "Mentor information saved successfully.")
        self.edit_window.destroy()

    def get_validated_hours(self):
        hours_wanted = self.hours_wanted_entry.get().strip()
        if hours_wanted:
            try:
                return int(hours_wanted)
            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"Invalid entry for hours wanted: '{hours_wanted}'. Please enter a number.",
                )
                return None
        return 0

    def get_validated_dates(self, dates_str):
        try:
            return self.parse_dates(dates_str)
        except ValueError as e:
            raise

    def parse_dates(self, dates_str):
        dates = set()
        for part in dates_str.split(","):
            part = part.strip()
            if not part:  # Skip empty parts
                continue
            if "-" in part:
                try:
                    start, end = map(int, part.split("-"))
                    if start > end:
                        raise ValueError
                    dates.update(range(start, end + 1))
                except ValueError:
                    raise ValueError(f"Invalid date range: '{part}'")
            else:
                try:
                    dates.add(int(part))
                except ValueError:
                    raise ValueError(f"Invalid date: '{part}'")
        return sorted(dates)

    def save_holidays(self):
        holiday_dates_str = self.holiday_entry.get().strip()
        try:
            holiday_dates = self.parse_dates(holiday_dates_str)
            self.mentor_data["holidays"]["dates"] = holiday_dates
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_mentor_info(self):
        selected_mentor_name = self.selected_mentor_var.get()
        if selected_mentor_name == "New Mentor":
            messagebox.showerror("Error", "No mentor selected to delete.")
            return

        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {selected_mentor_name}? This cannot be undone.",
        ):
            del self.mentor_data["mentor_info"][
                selected_mentor_name
            ]  # Remove the mentor from the dictionary
            with open("mentor_info.json", "w") as file:
                json.dump(
                    self.mentor_data, file, indent=4
                )  # Save the updated data back to the file
            messagebox.showinfo(
                "Success", f"{selected_mentor_name} has been deleted successfully."
            )
            self.edit_window.destroy()  # Optionally close the edit window or refresh the mentor list
            self.edit_mentor_info()  # Re-open or refresh the edit window if needed

    def generate_schedule(self):
        schedule_name = self.schedule_name_entry.get().strip()
        year = self.year_entry.get().strip()
        month_name = self.month_var.get().strip()

        holiday_dates_str = self.holiday_entry.get().strip()
        if holiday_dates_str:
            holiday_dates = [
                int(date.strip())
                for date in holiday_dates_str.split(",")
                if date.strip().isdigit()
            ]
        else:
            holiday_dates = []
        with open("mentor_info.json", "r") as file:
            mentor_data = json.load(file)
        mentor_data["holidays"]["dates"] = holiday_dates
        with open("mentor_info.json", "w") as file:
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
        month = str(
            self.months.index(month_name) + 1
        )  # Convert month name to month number
        pay_period_length = "15"  # Hardcoded to always be 15
        try:
            subprocess.run(
                [
                    "python",
                    SPREAD_GEN_SCRIPT,
                    schedule_name,
                    year,
                    month,
                    pay_period_length,
                ],
                check=True,
            )
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
