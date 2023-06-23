import datetime as dt

seasonal_shift_info = {
	'summer': {
		'dates': {
				'start': dt.datetime(dt.date.today().year, 5, 1), 
				'end':  dt.datetime(dt.date.today().year, 7, 31)
				},
		'shift_info': {
				'Sunday': {
					'12-8_shift': 8,
					}, 
				'Monday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
				},
				'Tuesday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
				},
				'Wednesday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
				},
				'Thursday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
				},
				'Friday': {
					'4-12_shift': 8,
				},
				'Saturday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
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
					'12-8_shift': 8,
					}, 
				'Monday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
				},
				'Tuesday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
				},
				'Wednesday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
				},
				'Thursday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
				},
				'Friday': {
					'4-12_shift': 8,
				},
				'Saturday': {
					'12-8_shift': 8,
					'4-12_shift': 8,
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
# June
mentor_info = {
	    'Asher': {
		'weekdays': ['Tuesday','Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [14]+[20]+[23]+[24],
		'hours_wanted': 36,
		'soft_dates' : []
	},
    'Avree': {
		'weekdays': ['Thursday','Friday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [4]+[i for i in range(12,16)]+[i for i in range(22,27)],
		'hours_wanted': 36,
		'soft_dates' : []
	},
	'Braxton': {
		'weekdays': ['Sunday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [i for i in range(1,9)],
		'hours_wanted': 40,
		'soft_dates' : []
	},
}

holidays = {
	'shift_info': {
		'holiday_shift': 8
	},
	'dates': [], # add during relevant month, include only day, Example: when scheduling for july add 4 to this list
}

# ex: python spread_gen_tsc.py july_sched_tsc 2023 7 15