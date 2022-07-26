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
					'c_shift': 3
					},
				'Tuesday': {
					'a_shift': 6,
					'b_shift': 6,
					'c_shift': 3
					},				
				'Wednesday': {
					'a_shift': 6,
					'b_shift': 6,
					},
				'Thursday': {
					'a_shift': 6,
					'b_shift': 6,
					'c_shift': 3
				},
				'Friday': {
					'a_shift': 8,
					'b_shift': 8,
					'c_shift': 3
				},
				'Saturday': {
					'a_shift': 11,
					'b_shift': 11,
					'c_shift': 4
				},
			},
		},
	}

#June info
mentor_info = {
	'Devon': {
		'hard_dates': [],
		'hours_wanted': 14,
		'soft_dates' : []
	},
	'Kate D': {
		'hard_dates': [],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Delcie':{
		'hard_dates': [],
		'hours_wanted': 20, 
		'soft_dates' : []
	},
	'Braxton': {
		'hard_dates': [],
		'hours_wanted': 20, 
		'soft_dates' : []
	},
	'Mitch': {
		'hard_dates': [],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Levi': {
		'hard_dates': [],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Kate S': {
		'hard_dates': [],
		'hours_wanted': 15,
		'soft_dates' : [] 
	}
}

holidays = {
	'shift_info': {
		'a_shift': 9,
		'b_shift': 9
	},
	'dates': [3,4], #add during relevant month, include only day, Example: when scheduling for july add 4 to this list
}