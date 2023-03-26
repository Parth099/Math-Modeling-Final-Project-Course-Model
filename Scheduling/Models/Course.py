"""
This file defines the <Course> Object used to 
"""

# type hint a class from within it self
from typing import List

class Course: 
    def __init__(self, code: str, name: str, classsize: int, creditno: int, coursetype, preqs: List['Course'], requirements: List[str]) -> None:
        self.code          = code         # unique class id
        self.name          = name         # Name
        self.creditno      = creditno     
        self.classsize     = classsize 
        self.prerequisites = preqs
        self.coursetype    = coursetype   # type of class EX: gened, major, ...
        self.requirements  = requirements # list of requirements needed to be met to join class (bucketing)

        self.grading__mu    = None        
        self.grading__sigma = None

    def __str__(self) -> str:
        return self.code
    
    def __repr__(self) -> str:
        return self.__str__()
