from Course import Course
from Student import Student

from typing import List, Dict

class Scheduler:
	"""Scheduler takes steps WRT open courses and availble"""
 
	def __init__(self, Courses: List[Course], Students: List[Student], course_map: Dict[str, int]) -> None:
		self.courses  = Courses
		self.students = Students
		self.course_map = course_map
  
	def student_can_take_class(self, student: Student, course: Course) -> bool:
		"""returns T/F on whether a Student `student` can take a Course `course`

		Args:
			student (Student): 
			course (Course): 

		Returns:
			bool
		"""

		# approved if no prerequisites exist
		if not course.prerequisites:
			return True
  
		# read in all classes a student has taken
		completed_classes = student.has_taken
  
		# make each class to its integer representation
		completed_classes_int = [self.course_map[_course['code']] for _course in completed_classes]

		# get into prereqs
		prereqs = course.prerequisites

		# map each item to a number
		prereqs_int = [self.course_map[prereq['code']] for prereq in prereqs]

		# if each of the numbers in prereqs appears in completed_classes, this student can take that class
		return all([class_num in completed_classes_int for class_num in prereqs_int])
	
	def select_classes():
		"""select class based on availble classes"""
		pass


	