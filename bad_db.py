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
					'c_shift': 3
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
					'a_shift': 6,
					'b_shift': 6,
					'c_shift': 4
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
# November
mentor_info = {
	'Braxton': {
		'weekdays': ['Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [10]+[15]+[26],
		'hours_wanted': 32, 
		'soft_dates' : []
	},
	'Kate D': {
		'weekdays': ['Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [5]+[10]+[i for i in range(20,28)],
		'hours_wanted': 25,
		'soft_dates' : []
	},
	'Kite S': {
		'weekdays': ['Sunday','Monday','Tuesday','Thursday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [i for i in range(1,7)]+[19]+[i for i in range(23,28)],
		'hours_wanted': 25,
		'soft_dates' : []
	},
	'Levi': {
		'weekdays': ['Saturday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [i for i in range(3,6)],
		'hours_wanted': 25,
		'soft_dates' : []
	},
	'Mitch': {
		'weekdays': ['Sunday','Monday','Wednesday'],
		'weekday_behavior': ['Re'],
		'hard_dates': [5]+[10]+[12]+[19]+[24],
		'hours_wanted': 23,
		'soft_dates' : []
	},
}

holidays = {
	'shift_info': {
		'holiday_a_shift': 9,
		'holiday_b_shift': 9
	},
	'dates': [24], #add during relevant month, include only day, Example: when scheduling for july add 4 to this list
}