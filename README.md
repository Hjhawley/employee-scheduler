# How to use the schedule generator

Edit 'mentor_info.json' to enter mentor info. For example, 'weekdays': ['Monday','Wednesday'], 'weekday_behavior': ['Re'] will make sure that a mentor is not scheduled on Mondays or Wednesdays. 'hard_dates': [2]+[23] will make sure they are not scheduled on the 2nd or the 23rd. Adjusting 'hours_wanted' (per week) will try to give more hours to the mentors who want them.

Use following command:
>python spread_gen.py [filename] [year] [month] [pay period length]

This will generate a new schedule as a .csv spreadsheet with the filename you provided.

Example:
>python spread_gen.py august_sched 2022 8 15

This command will generate a schedule for August 2022, with the first pay period ending on the 15th.

It would then create a file called august_sched.csv.