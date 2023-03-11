from Models.Course import Course
from Models.Student import Student

from random import shuffle

from typing import List, Dict

class Scheduler:
	"""Scheduler takes steps WRT open courses and availble"""
 
	CREDITS_THRESHOLD = 14
 
	def __init__(self, Courses: Dict[str, Course], Students: List[Student], course_map: Dict[str, int]) -> None:
		self.students = Students
		self.course_map = course_map
  
		self.courses: Dict[int, Course]  = {}

		# create an int -> info map to be used later
		for name, int_mapping in course_map.items():
			self.courses[int_mapping] = Courses.get(name)
	
  
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
	
	def select_classes(self):
		"""select class based on availble classes"""
		
		# shuffle array of students to give each one a fair chance of selecting first
		shuffle(self.students) # (inplace sort)
  
		for stu in self.students:
			
			# order the student wants
			ordering = stu.course_plan

			for course in ordering:
		
				C = self.courses.get(course)
    
				if C is None:
					raise ValueError("Course $C is none")
    
				# if student has registered for enough classes, allow other students to register
				if stu.curr_credit_count >= Scheduler.CREDITS_THRESHOLD:
					break
 
				if self.student_can_take_class(stu, C):
					stu.assign_class(C)

	


	