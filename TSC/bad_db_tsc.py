import datetime as dt

seasonal_shift_info = {
	'summer': {
		'dates': {
				'start': dt.datetime(dt.date.today().year, 5, 1), 
				'end':  dt.datetime(dt.date.today().year, 7, 31)
				},
		'shift_info': {
				'Sunday': {
					'12-10_shift': 10,
					}, 
				'Monday': {
					'12-6_shift': 6,
					'6-10_shift': 4,
				},
				'Tuesday': {
					'12-6_shift': 6,
					'6-10_shift': 4,
				},
				'Wednesday': {
					'12-6_shift': 6,
					'6-10_shift': 4,
				},
				'Thursday': {
					'12-6_shift': 6,
					'6-10_shift': 4,
				},
				'Friday': {
					'4-10_shift': 6,
				},
				'Saturday': {
					'12-10_shift': 10,
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
					'12-10_shift': 10,
					}, 
				'Monday': {
					'12-6_shift': 6,
					'6-10_shift': 4,
				},
				'Tuesday': {
					'12-6_shift': 6,
					'6-10_shift': 4,
				},
				'Wednesday': {
					'12-6_shift': 6,
					'6-10_shift': 4,
				},
				'Thursday': {
					'12-6_shift': 6,
					'6-10_shift': 4,
				},
				'Friday': {
					'4-10_shift': 6,
				},
				'Saturday': {
					'12-10_shift': 10,
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
# September
mentor_info = {
	    'Asher': {
		'weekdays': ['Monday','Tuesday','Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [1]+[9],
		'hours_wanted': 24,
		'soft_dates' : []
	},
    'Avree': {
		'weekdays': ['Thursday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [i for i in range(1,5)]+[i for i in range(15,18)],
		'hours_wanted': 24,
		'soft_dates' : []
	},
	'Braxton': {
		'weekdays': ['Friday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [2]+[15]+[16]+[29]+[30],
		'hours_wanted': 40,
		'soft_dates' : []
	},
}

holidays = {
	'shift_info': {
		'holiday_shift': []
	},
	'dates': [], # add during relevant month, include only day, Example: when scheduling for july add 4 to this list
}

# ex: python spread_gen_tsc.py sep_sched_tsc 2023 9 15