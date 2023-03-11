from typing import List
from Course import Course


class Student:
    """this class must be created synchronously due to $student_count interval variable"""
    
    student_count = 0
    
    def __init__(self, course_plan: List[int]):
        
        # constants
        self.course_plan = course_plan
        self.name = f'Student {Student.student_count}'
        
        # boundary variable
        self.hasFinished = False
    
		# state to keep track of what classes student is taking/taken
        self.hasTaking: List[Course] = []
        self.isTaken: List[Course]   = []
        
        Student.student_count += 1
    