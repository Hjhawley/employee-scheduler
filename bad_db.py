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

#September info
mentor_info = {
	'Devon': {
		'hard_dates': [1]+[2]+[4]+[6]+[8]+[9]+[11]+[13]+[15]+[16]+[18]+[19]+[20]+[22]+[25]+[27]+[29],
		'hours_wanted': 15,
		'soft_dates' : []
	},
	'Kate D': {
		'hard_dates': [7]+[14]+[21]+[28],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Delcie':{
		'hard_dates': [i for i in range(2,6)]+[17],
		'hours_wanted': 27, 
		'soft_dates' : []
	},
	'Braxton': {
		'hard_dates': [3],
		'hours_wanted': 27, 
		'soft_dates' : []
	},
	'Mitch': {
		'hard_dates': [],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Levi': {
		'hard_dates': [12]+[13],
		'hours_wanted': 20,
		'soft_dates' : []
	},
	'Kite S': {
		'hard_dates': [i for i in range(1,7)]+[8]+[12]+[13]+[i for i in range(15,21)]+[22]+[27]+[29],
		'hours_wanted': 15,
		'soft_dates' : [] 
	}
}

holidays = {
	'shift_info': {
		'holiday_a_shift': 9,
		'holiday_b_shift': 9
	},
	'dates': [5], #add during relevant month, include only day, Example: when scheduling for july add 4 to this list
}