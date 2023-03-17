from dataloader.JsonLoader import JsonLoader
from typing import Dict

from Scheduling.Models.Course import Course

class CourseDataLoader(JsonLoader):
	"""object that loads in course data based on a json object"""
    
	def __init__(self, path: str) -> None:
		# load in json (this generates self.data)
		super().__init__(path)

		# raise ERROR if self.data is none or empty
		if(self.data is None):
			raise ValueError("File data is None")

		# take data and serialize it
		# this variable maps name of course to all of its information
		self.course_info = self.jsonToCourse(self.data) 

		# create graph labels and integer mappings
		self.course_map, _ = self.generateMetaDataFromCourseDict(self.course_info)

		
	def jsonToCourse(self, json_data: list) -> Dict[str, Course]:
		"""take a json file and turn it into a dict based on the outermost key where each value is a (cached) Course Object"""

		course_dict: dict[str, Course] = {}

		# preload courses so prereqs can be loaded
		for course in json_data:
			# EXT details out of json array element
			code          = course['code']
			name          = course['name']
			creditno      = course['creditno']
			classsize     = course['classsize']

			# add finished course to cache
			course_dict[code] = Course(code, name, classsize, creditno, [])
   
		# load in course prereqs  
		for course in json_data:
			code = course['code']
			Current_Course = course_dict[code]
   
			for prereq_code in course['prerequisites']:
				CachedClass = course_dict[prereq_code]
				Current_Course.prerequisites.append(CachedClass)


		# return the cache
		return course_dict

	def generateMetaDataFromCourseDict(self, course_dict: Dict[str, Course]):
		"""
		Generates:
			(1) dict where integer maps to course_name\n
			(2) reversed dict (1)
		"""

		# dict (1)
		int_to_name: Dict[int, str] = dict(enumerate(course_dict.keys()))


		# dict (2) 
		name_to_int: Dict[str, int] = {value: key for (key, value) in int_to_name.items() }


		# labels, map
		return  name_to_int, int_to_name,