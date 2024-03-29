from typing import List, Dict, DefaultDict
from Scheduling.Models.Course import Course

from collections import defaultdict

from numpy.random import normal
from numpy import mean


class Student:
    """this class must be created synchronously due to $student_count internal variable"""
    
    student_count = 0
    FAILING_GRADE = 63
    
    DEFAULT_GRADE_MEAN = 75
    DEFAULT_GRADE_SDEV = 10

    # use past course history to impact current grade
    HISTORY_BASED_GRADING = False
    
    def __init__(self, course_map: Dict[str, int], course_plan: List[int]=[], HISTORY_BASED_GRADING=False):
        """Initialize a student

        Args:
            course_map (Dict[str, int]): course to integer mapping to help calulate prereqs\n
            course_plan (List[int], optional): Courses to take. Defaults to [].\n
            HISTORY_BASED_GRADING (bool, optional): Use history based grading or random? . Defaults to False (history based grading).
        """

        # alter class state
        Student.HISTORY_BASED_GRADING = HISTORY_BASED_GRADING
        
        # constants
        self.course_plan = course_plan
        self.name = f'Student {Student.student_count}'
        self.course_map = course_map
        
        # boundary variables
        self.semester = 0
        self.is_finished = False
        
    
		# state to keep track of what classes student is taking/taken
        self.has_taken:  List[Course] = [] # can also be used as a history
        self.is_taking:  List[Course] = []  
        self.has_failed: DefaultDict[str, int] = defaultdict(int) # keeps count of number of failures WRT course
        self.grades: Dict[str, float] = {}     # keeps track of latest grades per course
        
        self.curr_credit_count = 0
        self.credit_count = 0

        # update school count
        Student.student_count += 1
        
        # history (pass fail only)
        # map semester (into) to all courses taken that semester (str[]) with their P/F state
        self._history: Dict[int, Dict[str, bool]] = {}
        
        
    def assign_class(self, course: Course):
        self.is_taking.append(course)
        self.curr_credit_count += course.creditno
    
    def update_finished_status(self):
        self.is_finished = len(self.course_plan) == 0 # no classes left to take!
    
    def generate_grade(self, course: Course):
        """generates a grade based on the normal distribution given a course\nA grade is generated using the history of the student
        Args:
            course (Course)
        Returns:
            (float): generated Grades
        """

        mu = Student.DEFAULT_GRADE_MEAN;    
        past_grades = self.get_grades_for_courses(course.prerequisites)
        
        # if HISTORY_BASED_GRADING check what the student got for prev classes
        if Student.HISTORY_BASED_GRADING and past_grades:
            mu = mean(past_grades)

        grade = normal(mu, Student.DEFAULT_GRADE_SDEV)

        return min(grade, 100) # do not give grades over 100
    
    def get_grades_for_courses(self, courses: List[Course]):
        """gets grades for class given a list of classes

        Args:
            courses (List[Course]): courses to retrive grades for

        Returns:
            List of grades (floats)
        """
        return [self.grades[course.code] for course in courses if course.code in self.grades]
    
    def increment_semester(self) -> None:
        """represents the end of a semester, this function assigns grades and places courses into correct categories: passed + failing"""
        
        # history fragment keeps history of this semster
        history_fragment: Dict[str, bool] = {}
        for course in self.is_taking:
            received_grade = self.generate_grade(course)
            hasPassed = received_grade > Student.FAILING_GRADE
            
            if hasPassed: 
                self.has_taken.append(course)
                passed_class = self.course_map.get(course.code)
                
                # remove class from plan now that it is used
                if passed_class in self.course_plan: self.course_plan.remove(passed_class)

            else: self.has_failed[course.code] += 1
            
            history_fragment[course.code] = int(hasPassed)
            self.grades[course.code] = received_grade
            
        # history
        self._history[self.semester] = history_fragment
            
        # empty out course list for this semester
        self.is_taking = []
        self.credit_count += self.curr_credit_count  
        self.curr_credit_count = 0

        # check if student has graduated
        if not self.update_finished_status():
            self.semester += 1        
        
        
    