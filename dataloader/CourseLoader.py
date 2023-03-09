import sys, os
sys.path.insert(0, os.getcwd()) # add this module to $path to allow python to find it later

from JsonLoader import JsonLoader
from typing import Dict

from Course import Course

class CourseDataLoader(JsonLoader):
	def __init__(self, path: str) -> None:
		# load in json (this generates self.data)
		super().__init__(path)

		# take data and serialize it
		self.course_info = self.jsonToCourse(self.data)

		# create graph labels and integer mappings
		self.course_map, self.graph_labels = self.generateMetaDataFromCourseDict(self.course_info)

		
	def jsonToCourse(json_data: list) -> Dict[str, Course]:
		"""take a json file and turn it into a dict based on the outermost key where each value is a (cached) Course Object"""

		course_dict: dict[str, Course] = {}

		for course in json_data:
			# EXT details out of json array element
			code          = course['code']
			name          = course['name']
			creditno      = course['creditno']
			prerequisites = course['prerequisites']

			# create new entity based on json fragment
			Current_Course = Course(code, name, creditno, [])

			for prereq_code in prerequisites:
				CachedClass = course_dict[prereq_code]
				Current_Course.prerequisites.append(CachedClass)

			# add finished course to cache
			course_dict[code] = Current_Course


		# return the cache
		return course_dict

	def generateMetaDataFromCourseDict(course_dict: Dict[str, Course]):
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