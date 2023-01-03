import datetime as dt

seasonal_shift_info = {
	'summer': {
		'dates': {
				'start': dt.datetime(dt.date.today().year, 5, 1), 
				'end':  dt.datetime(dt.date.today().year, 7, 31)
				},
		'shift_info': {
				'Sunday': {
					'a_shift': 9,
					'b_shift': 9
					}, 
				'Monday': {
					'a_shift': 6,
					'b_shift': 7,
					'c_shift': 3
				},
				'Tuesday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 3
				},
								
				'Wednesday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 3
				},
				'Thursday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 3
				},
				'Friday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 3
				},
				'Saturday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 3,
					'd_shift' : 3
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
					'b_shift': 9
					}, 
				'Monday': {
					'a_shift': 7,
					'b_shift': 7,
					'c_shift': 5
					},
				'Tuesday': {
					'a_shift': 6,
					'b_shift': 6,
					'c_shift': 4
					},				
				'Wednesday': {
					'a_shift': 6,
					'b_shift': 6,
					},
				'Thursday': {
					'a_shift': 6,
					'b_shift': 6,
					'c_shift': 4
				},
				'Friday': {
					'a_shift': 8,
					'b_shift': 8,
					'c_shift': 4
				},
				'Saturday': {
					'a_shift': 11,
					'b_shift': 11,
					'c_shift': 4,
					'd_shift': 4
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
# February
mentor_info = {
	'Braxton (Thu C shift)': {
		'weekdays': ['Monday','Wednesday','Friday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [23]+[24]+[25],
		'hours_wanted': 25,
		'soft_dates' : []
	},
	'Ella (Sat C shift)': {
		'weekdays': ['Tuesday','Wednesday','Friday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [2]+[14]+[18],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Josie': {
		'weekdays': ['Sunday','Thursday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Kate S (Mon C shift)': {
		'weekdays': ['Sunday','Tuesday','Thursday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [24]+[25]+[26],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Levi (Thu C shift)': {
		'weekdays': ['Saturday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [12],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Mitch': {
		'weekdays': ['Sunday', 'Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [],
		'hours_wanted': 20,
		'soft_dates' : []
	},
}

holidays = {
	'shift_info': {
		'holiday_a_shift': 9,
		'holiday_b_shift': 9
	},
	'dates': [20], #add during relevant month, include only day, Example: when scheduling for july add 4 to this list
}

# ex: python spread_gen.py JanSched 2023 1 15