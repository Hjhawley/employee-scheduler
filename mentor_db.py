import datetime as dt

seasonal_shift_info = {
	'summer': {
		'dates': {
				'start': dt.datetime(dt.date.today().year, 5, 1), 
				'end':  dt.datetime(dt.date.today().year, 7, 31)
				},
		'shift_info': {
				'Sunday': {
					'a_shift': 10,
					'b_shift': 10,
					},
				'Monday': {
					'a_shift': 8,
					'b_shift': 8,
					'c_shift': 5,
				},
				'Tuesday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 4,
				},
				'Wednesday': {
					'a_shift': 7,
					'b_shift': 7,
				},
				'Thursday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 4.
				},
				'Friday': {
					'a_shift': 8,
					'b_shift': 8,
					'c_shift': 4,
				},
				'Saturday': {
					'a_shift': 11,
					'b_shift': 11,
					'c_shift': 4,
				},
			},
		},

	'winter': {
		'dates': {
			'start': dt.datetime(dt.date.today().year, 8, 1), 
			'end':  dt.datetime(dt.date.today().year + 1, 4, 30)
			},
		'shift_info': {
				'Sunday': {
					'a_shift': 9,
					'b_shift': 9,
					},
				'Monday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 5,
					},
				'Tuesday': {
					'a_shift': 6,
					'b_shift': 6,
					'c_shift': 4,
					},
				'Wednesday': {
					'a_shift': 6,
					'b_shift': 6,
					},
				'Thursday': {
					'a_shift': 6,
					'b_shift': 6,
					'c_shift': 4,
				},
				'Friday': {
					'a_shift': 8,
					'b_shift': 8,
					'c_shift': 4,
				},
				'Saturday': {
					'a_shift': 11,
					'b_shift': 11,
					'c_shift': 4,
				},
			},
		},
	}

# [Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday]
"""Weekday_behavior explained:
	'Inv': Ignore hard_dates and only allow mentor to work on days in weekdays
	'Pe': Look at hard_dates and remove any date that matches a weekday
	'Re': Look at hard dates and add any date that matches a weekday
	
Note if weekdays field is empty we ignore weekday behavior.
"""

# March
mentor_info = {
    'Asher': {
		'weekdays': ['Monday','Thursday','Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [9]+[i for i in range(11,16)],
		'hours_wanted': 16, # Wants 24-30 per week in Jan
		'soft_dates' : []
	},
    'Ashley': {
		'weekdays': ['Thursday','Friday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [],
		'hours_wanted': 25,
		'soft_dates' : []
	},
    'Avree': {
		'weekdays': ['Tuesday','Thursday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [4]+[i for i in range(9,17)],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Braxton': {
		'weekdays': ['Thursday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [i for i in range(10,17)],
		'hours_wanted': 26, # Prioritize Braxton's hours as per seniority
		'soft_dates' : []
	},
    'Ella': {
		'weekdays': ['Sunday','Monday','Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [2]+[i for i in range(8,18)]+[23]+[24]+[29]+[30]+[31],
		'hours_wanted': 21,
		'soft_dates' : []
	},
	'Jonah': {
		'weekdays': ['Sunday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [2],
		'hours_wanted': 18,
		'soft_dates' : []
	},
	'Levi': {
		'weekdays': ['Saturday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [],
		'hours_wanted': 16,
		'soft_dates' : []
	},
	'Mitch': {
		'weekdays': ['Tuesday', 'Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [i for i in range(10,18)]+[27]+[28],
		'hours_wanted': 16,
		'soft_dates' : []
	},
    'Roxy': {
		'weekdays': ['Tuesday','Thursday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [],
		'hours_wanted': 25,
		'soft_dates' : []
	},
    'Sam': {
		'weekdays': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [],
		'hours_wanted': 18,
		'soft_dates' : []
	},
}

holidays = {
	'shift_info': {
		'holiday_a_shift': 9,
		'holiday_b_shift': 9
	},
	'dates': [], # Example: when scheduling for July, add 4 to this list
}

# ex: python spread_gen.py mar_sched 2024 3 15
