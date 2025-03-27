import json
import datetime as dt
import operator
from calendar import monthrange
from typing import List, Dict, Union, Tuple
from bisect import bisect_left
import numpy as np

with open('mentor_info.json', 'r') as file:
    data = json.load(file)
    seasonal_shift_info = data['seasonal_shift_info']
    mentor_info = data['mentor_info']
    holidays = data['holidays']

def get_truth(inp, relate, cut):
	ops = {'>': operator.gt,
			'<': operator.lt,
			'>=': operator.ge,
			'<=': operator.le,
			'==': operator.eq}
	return ops[relate](inp, cut)

def BinarySearch(a, x):
	i = bisect_left(a, x)
	if i != len(a) and a[i] == x:
		return i
	else:
		return -1

class Mentor():
    """represents Mentor specific scheduling information for a single pay period"""

    def __init__(self, name: str, hours_wanted: int, hard_dates: List[int],
                 soft_dates: List[int], len_pay: int, preferred_weekdays: List[str] = None):
        self.name = name
        self.hours_wanted = hours_wanted
        self.hard_dates = [int(date) for date in hard_dates]
        self.soft_dates = [int(date) for date in soft_dates]
        self.hours_pay = 0
        self.days_left = len_pay - len(hard_dates)
        self.preferred_weekdays = preferred_weekdays if preferred_weekdays is not None else []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def legal_shift_add(self, shift_len: int):
        """checks if adding new shifts leads to overtime"""
        return self.hours_pay + shift_len <= 80 

    def __radd__(self, other):
        return other + self.get_available_hours()

    def get_available_hours(self) -> int:
        """get remaining hours this mentor wants in current pay period"""
        return self.hours_wanted - self.hours_pay
	

class Day():
	"""Class represents a scheduled Day"""

	def __init__(self, date_info: dt.datetime):
		self.date_info = date_info
		self.week_day_map = {'Sunday': 6, 'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5}
		self.weekday = date_info.weekday()
		self.season = self.get_season()
		self.shifts = self.get_shifts(self.season, self.weekday)
		self.mentors_on_shift: Dict[str, Mentor] = {shift: None for shift in self.shifts} 
		self.total_hours = sum(self.shifts.values())
		self.assigned_hours = 0
		self.potential_mentors: List[Mentor] = []
		self.priority_value = 0
		

	def get_mentor_days(self) -> int:
		"""Get number of mentors who can still theoretically work on this day"""
		return len(self.potential_mentors)

	def get_available_mentor_hours(self) -> int:
		"""get number of hours mentors could still theoretically work on this day"""
		return sum(self.potential_mentors)

	def add_potential_mentor(self, mentor: Mentor):
		"""Adds mentor to potential_mentors field"""
		self.potential_mentors.append(mentor)
	
	def available_shifts(self) -> bool:
		"""Check if this day has any more shifts available. Returns a bool"""
		return None in self.mentors_on_shift.values()

	def add_shift(self, mentor: Mentor) -> bool:
		"""Tries to add mentor to next available open shift slot. Returns bool indicating success status.
		Raises error if  empty shift is not available"""
		for shift, slot in self.mentors_on_shift.items():
			if slot is None:
				legal_add = mentor.legal_shift_add(self.shifts[shift])

				if legal_add:
					self.mentors_on_shift[shift] = mentor
					mentor.hours_pay += self.shifts[shift]
					return True
				return False

		raise ValueError("Tried to fill shift in full day, this should never happen")

	def add_lowest_shift(self, mentor: Mentor) -> bool:
		"""adds mentor to shift with lowest number of hours required. Useful for avoiding overtime.
		Returns bool indicating success status"""
		lowest_hours = 100
		cur_shift = None

		for shift, slot in self.mentors_on_shift.items():
			if slot is None:

				shift_len = self.shifts[shift]
				if shift_len < lowest_hours:
					lowest_hours = shift_len
					cur_shift = shift

		legal_add = mentor.legal_shift_add(lowest_hours)

		if legal_add:
			self.mentors_on_shift[cur_shift] = mentor
			mentor.hours_pay += self.shifts[shift]
			return True
	
		return False

	def remove_shift(self):
		pass

	def get_needed_hours(self) -> int:
		return self.total_hours - self.assigned_hours

	def get_season(self) -> str:
		"""Get season to which this day belongs based on the month."""
		month = self.date_info.month

		summer_months = [5, 6, 7]  # May, June, July
		winter_months = [8, 9, 10, 11, 12, 1, 2, 3, 4]  # Every other month

		if month in summer_months:
			return 'summer'
		elif month in winter_months:
			return 'winter'
		else:
			raise ValueError('Could not find season that matched given date')
	
	def get_shifts(self, season: str, day: int) -> Dict[str, int]:
		"""get the shifts required for this day"""
		if self.date_info.day in holidays['dates']:
			return holidays['shift_info'].copy()

		#I hate this, but I also hate the idea of numerical keys though im  not sure if this monstrosity justifies 
		#not using them. 
		position = list(self.week_day_map.values()).index(day) #get index of key of shift for given weekday
		shift_info_keys = list(seasonal_shift_info[season]['shift_info'].keys())
		weekday = shift_info_keys[position]
		return seasonal_shift_info[season]['shift_info'][weekday].copy()

class Schedule():

	def __init__(self, year: int, month: int, len_p1: int):
		self.week_day_map = {'Sunday': 6, 'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5}
		self.len_p1 = len_p1
		self.month = month
		self.year = year
		len_month = monthrange(year, month)[1] #get num days in month, used to calc len_p2
		self.m1 = self.create_mentor_info(len_p1, '<=', len_p1)
		self.pay1 = self.create_pay_days(self.m1, dt.datetime(year, month, 1), dt.datetime(year, month, len_p1))
		self.assigned_days: List[Day] = []

		self.assign_all_shifts(self.pay1, self.m1)
		self.m2 = self.create_mentor_info(len_month - len_p1, '>', len_p1)
		self.pay2 = self.create_pay_days(self.m2, start_date = dt.datetime(year, month, len_month - (len_month - len_p1) + 1), end_date= dt.datetime(year, month, len_month), offset = len_p1)
		self.assign_all_shifts(self.pay2, self.m2)

	def get_dates_of_weekday(self, day: str) -> List[int]:
		"""given a day of the week ex: Sunday, return all dates in passed month that correspond to that weekday"""
		len_month = monthrange(self.year, self.month)[1]
		idx = 0
		for i in range(7): #7 days in a week
			if self.week_day_map[day] == dt.datetime(self.year, self.month, i + 1).weekday():
				idx = i + 1
				break
		
		dates = range(idx, len_month + 1, 7)
		return dates
	
	def get_all_weekday_dates(self, weekdays: List[str]):
		dates = []
		for day in weekdays:
			dates += self.get_dates_of_weekday(day)
		dates.sort()
		return dates

	def hard_date_adj(self, hard_dates: List[int], weekdays: List[str], behavior: str) -> List[int]:
		if len(weekdays) == 0:
			return hard_dates
		
		len_month = monthrange(self.year, self.month)[1]

		allowed_dates = self.get_all_weekday_dates(weekdays)

		if behavior[0] == "Inv":
			res_dates = range(1, len_month + 1)
			res_dates = [date for date in res_dates if date not in allowed_dates]
			return res_dates
		elif behavior[0] == "Pe":
			res_dates = [date for date in hard_dates if date not in allowed_dates]
			return res_dates
		elif behavior[0] == "Re":
			res_dates = list(np.unique(hard_dates + allowed_dates))
			res_dates.sort()
			return res_dates
		else:
			raise ValueError("Got bad behavior keyword {0}".format(behavior))

	def create_mentor_info(self, len_pay: int, comparator: str, end_day: int = 1) -> List[Mentor]:
		"""Create initial default list of mentors for a given pay period"""
		mentor_list = [None for _ in mentor_info]
		idx = 0

		for name, info in mentor_info.items():
			c_info = info.copy()
			new_dates = self.hard_date_adj(info['hard_dates'], info["weekdays"], info["weekday_behavior"])
			c_info['hard_dates'] = [date for date in new_dates if get_truth(date, comparator, end_day)]
			c_info['name'] = name
			c_info['hours_wanted'] = c_info['hours_wanted'] * 2  #2 weeks
			c_info['len_pay'] = len_pay
			c_info['preferred_weekdays'] = info.get('preferred_weekdays', [])
			c_info = {
				'hard_dates': c_info['hard_dates'],
				'name': name,
				'hours_wanted': c_info['hours_wanted'],
				'len_pay': len_pay,
				'soft_dates': c_info['soft_dates'],
				'preferred_weekdays': c_info['preferred_weekdays']
			}

			mentor_list[idx] = Mentor(**c_info)
			idx += 1

		return mentor_list


	def create_pay_days(self, mentors: List[Mentor], start_date: dt.datetime, end_date: dt.datetime, offset: int = 0) -> List[Day]:
		"""Create initial set of empty days for a given pay period
		
		Args:
			start_date: start of pay period
			end_date: end of pay period
			offset: used in second pay period for indexing purposes, should be equal to length of first pay period
		"""
		cur_date = start_date
		num_days = end_date.day - start_date.day + 1
		days: List[Day] = [None for _ in range(num_days)]
		idx  = 0

		while cur_date <= end_date:
			days[idx] = Day(cur_date)
			cur_date += dt.timedelta(days=1)
			idx += 1
		
		for mentor in mentors:

			#gets all available days in pay period which mentor can work
			available_days = [i for i in range(start_date.day, end_date.day + 1)]
			available_days = [x for x in available_days if x not in mentor.hard_dates] 
			#assign which mentors can work on given day
			for date in available_days:
				days[date - offset - 1].add_potential_mentor(mentor)

		return days


	def prioritize_days(self, pay_days: List[Day]):
		"""We prioritize using mentors available for each days shift over total number of workable shifts over pay period"""
		total_available_days = sum([day.get_mentor_days() for day in pay_days]) #total workable shifts
		for day in pay_days:
			# Normal priority:
			base_priority = day.get_mentor_days() / (total_available_days + 1)

			# Assign a special priority to Saturday
			if day.date_info.weekday() == 5:
				day.priority_value = -999999
			else:
				day.priority_value = base_priority

		# Sort ascending by priority_value, then descending by available_mentor_hours
		pay_days.sort(key=lambda day: (day.priority_value, -day.get_available_mentor_hours()))
  
  
	def filter_saturday_candidates(self, candidates: List[Mentor], current_day: Day, assigned_days: List[Day]) -> List[Mentor]:
		# Only apply if the current day is a Saturday, but not the first Saturday of the month
		if current_day.date_info.weekday() != 5 or current_day.date_info.day <= 7:
			return candidates
		previous_saturday = None
		for day in sorted(assigned_days, key=lambda d: d.date_info, reverse=True):
			if day.date_info.weekday() == 5 and day.date_info < current_day.date_info:
				previous_saturday = day
				break
		if not previous_saturday:
			return candidates
		# exclude mentors who worked last Saturday
		mentors_last_saturday = {mentor for mentor in previous_saturday.mentors_on_shift.values() if mentor is not None}
		filtered = [mentor for mentor in candidates if mentor not in mentors_last_saturday]
		# If filtering leaves you with any candidates, use them; otherwise fall back
		return filtered if filtered else candidates


	def assign_shift(self, pay_days: List[Day]) -> Union[int, Mentor]:
		"""Assign first shift in highest priority day if possible.
		Returns:
			1 if all Mentors lost a day otherwise returns mentor who was assigned.
		"""
		day = pay_days[0]  # Highest priority day (after sorting)
		update_mentors = True #prevents double updating mentors available days on recursive calls
		day_name = day.date_info.strftime("%A")
		
		# Prefer mentors who have this weekday in their preferred_weekdays
		preferred_candidates = [mentor for mentor in day.potential_mentors if day_name in mentor.preferred_weekdays]
		# If at least one mentor prefers this day, consider only those; otherwise use all available mentors.
		candidates = preferred_candidates if preferred_candidates else day.potential_mentors

		# Apply the Saturday filter if the day is Saturday.
		candidates = self.filter_saturday_candidates(candidates, day, self.assigned_days)

		highest_prio = -100
		cur_mentor = None

		for mentor in candidates:
			cur_prio = mentor.get_available_hours() / mentor.days_left
			if cur_prio > highest_prio:
				highest_prio = cur_prio
				cur_mentor = mentor

		if cur_mentor is None:
			self.assigned_days.append(pay_days[0])
			del pay_days[0]  # Remove day if no mentor is available
			return 1

		success = day.add_shift(cur_mentor)

		if not success:
			update_mentors = False #recursive call will update mentor days don't assign in this stack call
			success = day.add_lowest_shift(cur_mentor)
			if not success:
				day.potential_mentors.remove(cur_mentor)
				self.prioritize_days(pay_days)
				return self.assign_shift(pay_days)

		if update_mentors:
			# Update mentor days_left based on assignment
			if len(day.potential_mentors) == 1 or not day.available_shifts():
				for mentor in day.potential_mentors:
					mentor.days_left -= 1
				self.assigned_days.append(pay_days[0])
				del pay_days[0]
				return 1
			else:
				cur_mentor.days_left -= 1
				day.potential_mentors.remove(cur_mentor)
				return cur_mentor


	def mentor_cleanup(self, mentor_update: Union[int, Mentor], pay_days: List[Day], mentors: List[Mentor]):
		"""Removes mentors who are no longer eligible to work this pay period for potential mentors in all days"""
		mentors_to_update = []

		if type(mentor_update) is Mentor: #we can just check passed mentor
			if mentor_update.days_left == 0 or mentor_update.get_available_hours() <= 0:
				mentors_to_update.append(mentor_update)
		elif type(mentor_update) is int: #need to check all mentors
			for mentor in mentors:
				if mentor.days_left == 0 or mentor.get_available_hours() <= 0:
					mentors_to_update.append(mentor)
		else:
			raise ValueError("got bad datatype {0} must pas int or Mentor".format(type(mentor_update)))

		for day in pay_days:
			day.potential_mentors = [mentor for mentor in day.potential_mentors if mentor not in mentors_to_update]

			
	def assign_all_shifts(self, pay_days: List[Day], mentors: List[Mentor]):
		"""Assigns all shifts for given pay period"""
		unassigned_days = len(pay_days)

		while unassigned_days > 0:
			#not particularly efficient since we end up needing to sort entire list for every single lookup as values change constantly
			#However can't think of easy clean solution that can replicate this functionality and it's not worth the hassle
			#to be to clever about it.
			self.prioritize_days(pay_days)
			mentor = self.assign_shift(pay_days)
			if mentor is not None:
				self.mentor_cleanup(mentor, pay_days, mentors)
			unassigned_days = len(pay_days)
		
		self.assigned_days.sort(key=lambda day:(day.date_info.day)) #sort days in calendar order
