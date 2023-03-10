from typing import List
from Course import Course


class Student:
    def __init__(self, course_plan: List[int]):
        self.course_plan = course_plan
        
        # boundary variable
        self.hasFinished = False
    
		# state to keep track of what classes student is taking/taken
        self.hasTaking: List[Course] = []
        self.isTaken: List[Course]   = []
        
        