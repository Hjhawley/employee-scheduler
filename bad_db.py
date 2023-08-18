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
                    'backup': 4,
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
                    'backup': 4,
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
    'Devon (one Sat C shift)': {
		'weekdays': ['Sunday','Monday','Thursday','Saturday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [8]+[9]+[10]+[16]+[17]+[18]+[19],
		'hours_wanted': 18,
		'soft_dates' : []
	},
	'Ella': {
		'weekdays': ['Wednesday','Saturday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [1]+[2]+[3]+[4],
		'hours_wanted': 24,
		'soft_dates' : []
	},
	'Jonah': {
		'weekdays': ['Sunday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [1]+[2]+[3]+[4],
		'hours_wanted': 24,
		'soft_dates' : []
	},
	'Levi (one Sat C shift)': {
		'weekdays': ['Saturday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [14]+[17],
		'hours_wanted': 24,
		'soft_dates' : []
	},
	'Mitch': {
		'weekdays': ['Sunday','Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [2]+[3]+[4]+[9],
		'hours_wanted': 20,
		'soft_dates' : []
	},
    'Roxy': {
		'weekdays': ['Monday','Thursday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [15]+[16],
		'hours_wanted': 24,
		'soft_dates' : []
	},
    'Sam': {
		'weekdays': ['Saturday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [i for i in range(20,25)],
		'hours_wanted': 19,
		'soft_dates' : []
	},
}

holidays = {
	'shift_info': {
		'holiday_a_shift': 9,
		'holiday_b_shift': 9
	},
	'dates': [4], # add during relevant month, include only day, Example: when scheduling for july add 4 to this list
}

# ex: python spread_gen.py sep_sched 2023 9 15