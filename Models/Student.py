from typing import List
from Course import Course

from numpy.random import normal


class Student:
    """this class must be created synchronously due to $student_count internal variable"""
    
    student_count = 0
    FAILING_GRADE = 65
    
    def __init__(self, course_plan: List[int]):
        
        # constants
        self.course_plan = course_plan
        self.name = f'Student {Student.student_count}'
        
        # boundary variables
        self.has_finished = False
        self.semester = 1
    
		# state to keep track of what classes student is taking/taken
        self.has_taken:  List[Course] = []
        self.is_taking:  List[Course] = []
        self.has_failed: List[Course] = []
        
        Student.student_count += 1
    
    @staticmethod
    def generate_grade(mu: float, sigma: float):
        """generates a grade based on the normal distribution
        Args:
            mu (float): mean
            sigma (float): stddev

        Returns:
            (float): _description_
        """
        return normal(mu, sigma)
    
    def increment_semester(self) -> None:
        """represents the end of a semester"""
        mu, sigma = 70, 10
        
        for course in self.is_taking:
            received_grade = Student.generate_grade(mu, sigma)
            
            if received_grade <= Student.FAILING_GRADE: self.has_failed.append(course)
            else: self.has_taken.append(course)
            
        # empty out course list for this semester
        self.is_taking = []
        self.semester += 1