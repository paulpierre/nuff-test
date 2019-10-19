import csv, time

"""
Note: Typo in district of columbia (DC) missing 'D' :-x
"""
class Schools():
	def __init__(self):

		self.SCHOOLS = dict()
		self.curr_state = ''
		self.curr_city = ''
		self.results = list()
		self.score_location = 0
		self.score_school = 0
		
		STATE = 5
		MLOCALE = 8
		CITY = 4
		SCHOOL_NAME = 3

		with open('school_data.csv') as csv_file:

			csv_reader = csv.reader(csv_file,delimiter=',')

			for row in csv_reader:

				#skip the header
				if row[0] == 'NCESSCH':
					continue
				
				# lets initialize the data in memory if not set since we can't use default dicts
				if row[STATE] not in self.SCHOOLS:
					self.SCHOOLS[row[STATE]] = dict()

				if row[CITY] not in self.SCHOOLS[row[STATE]]:
					self.SCHOOLS[row[STATE]][row[CITY]]= list()

				self.SCHOOLS[row[STATE]][row[CITY]].append(row[SCHOOL_NAME])


	def __str__(self):
		return '<SCHOOLS>\n{}'.format(self.SCHOOLS)
		
	def search_schools(self,query):

		start_ms = int(round(time.time() * 1000))

		# let's recurse our way down the forest
		def extract(node,search_string):


			# Hash structure: state => city => school

			# ---------------
			# Location search
			# ---------------
			if isinstance(node,dict):

				# iterate through location node
				for k,v in node.items():

					# cheap way to track city & state
					if len(k) == 2:
						self.curr_state = k
					else:
						self.curr_city = k

					# reset score
					self.score_location = 0

					# inline iter to compare each search keyword against location node
					for i in [x.strip().upper() for x in search_string.split(' ')]:
						if i in k:

							
							self.score_location+=1 # bump +1 for location match, normal weight
				
					# if its a dict, recurse!
					if isinstance(node,dict):
						extract(v,search_string)

			# -------------
			# School search
			# -------------
			elif isinstance(node,list): # schools are lists

				# location branch score preserved, but reset the school as we iterate
				self.score_school = 0
				for school_name in node:
					
					#inline iter to compare each search keyword against ranking criteria
					for i in [x.strip().upper() for x in search_string.split(' ')]:
						
						# this is cheating
						if i == 'SCHOOL':
							continue

						# this too, but give weight to schools_name over location in case of collision
						if i in school_name and i not in self.curr_city and i not in self.curr_state:
							self.score_school+=5
						else:

							# if the word does not appear, penalize -- its very hacky
							self.score_school-=1
					
					# if we scored at all tally for the rank and add to results
					if self.score_school > 0 or self.score_location > 0:
						total_score = self.score_school + self.score_location
						self.results.append((total_score,'{} => {}, {}'.format(school_name,self.curr_city,self.curr_state)))

					self.score_school = 0 # reset score

		extract(self.SCHOOLS,query) # start recursion
		
		stop_ms = int(round(time.time() * 1000)) #hit stop watch
		
		results = sorted(self.results)[-3:] #sort tuple ranking, get bottom 3
		print('results:\n{}').format('\n'.join([x[1] for x in results[::-1]])) #invert and join for display
		self.results = list()
		
		
		print('Results for "{}" (search took: {}ms)').format(query,stop_ms - start_ms) # summary


school_search = Schools()
school_search.search_schools('elementary school highland park')
school_search.search_schools('jefferson belleville')
school_search.search_schools('riverside school 44')
school_search.search_schools('granada charter school')
school_search.search_schools('foley high alabama')
school_search.search_schools('KUSKOKWIM')
