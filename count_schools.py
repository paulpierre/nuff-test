import csv, time, itertools

"""
Note: Typo in csv, district of columbia (DC) missing 'D' :/
"""
class Schools():
	def __init__(self):
		self.SCHOOLS = dict()
		self.school_count = 0
		self.school_count_by_state = dict()
		self.school_count_by_metro = dict()
		self.school_count_by_city = dict()

		STATE = 5
		MLOCALE = 8
		CITY = 4
		SCHOOL_ID = 0

		with open('school_data.csv') as csv_file:

			csv_reader = csv.reader(csv_file,delimiter=',')

			for row in csv_reader:

				#skip the header
				if row[0] == 'NCESSCH':
					continue
				
				# lets initialize if not set since we can't use default dicts
				if row[STATE] not in self.SCHOOLS:
					self.SCHOOLS[row[STATE]] = dict()
					self.school_count_by_state[row[STATE]] = 0
 					#print('Adding state: {}').format(row[STATE])


				if row[MLOCALE] not in self.SCHOOLS[row[STATE]]:
					self.SCHOOLS[row[STATE]][row[MLOCALE]] = dict()
					self.school_count_by_metro[row[MLOCALE]] = 0
					#print('Adding metro locale: {}').format(row[MLOCALE])

				if row[CITY] not in self.SCHOOLS[row[STATE]][row[MLOCALE]]:
					self.SCHOOLS[row[STATE]][row[MLOCALE]][row[CITY]] = list()
					self.school_count_by_city[row[CITY]] = 0
					#print('Adding city: {}').format(row[CITY])					

				self.SCHOOLS[row[STATE]][row[MLOCALE]][row[CITY]].append(row[SCHOOL_ID])


				self.school_count +=1
				self.school_count_by_state[row[STATE]] +=1
				self.school_count_by_metro[row[MLOCALE]] +=1
				self.school_count_by_city[row[CITY]] +=1

	def __str__(self):
		return '<SCHOOLS>\n{}'.format(self.SCHOOLS)
		
	def get_total_schools(self):
		return '\nTotal schools: {}'.format(self.school_count)

	def get_schools_by_state(self):
		return '\nSchools by state:\n{}'.format('\n'.join(['{}: {}'.format(i,self.school_count_by_state[i]) for i in sorted(self.school_count_by_state)]))

	def get_schools_by_metro(self):
		return '\nSchools by metro locale:\n{}'.format('\n'.join(['{}: {}'.format(i,self.school_count_by_metro[i]) for i in sorted(self.school_count_by_metro)]))

	def get_city_most_schools(self):
		return '\nCity with most schools: {}'.format(sorted(self.school_count_by_city.items(), key=lambda kv: kv[1])[len(self.school_count_by_city)-1])

	def get_city_min_one_school(self):
		return '\nUnique cities with at least one school: {}'.format(len(self.school_count_by_city))




escuela = Schools()
print(escuela.get_total_schools())
print(escuela.get_schools_by_state())
print(escuela.get_schools_by_metro())
print(escuela.get_city_most_schools())
print(escuela.get_city_min_one_school())


# total schools

# schools by state

# schools by metro centric locale

# city with the most schools (how many?)

# how many unique cities have at least 1 school
