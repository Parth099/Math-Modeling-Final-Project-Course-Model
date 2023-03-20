"""
This file defines the <Course> Object used to 
"""

# type hint a class from within it self
from typing import List

class Course: 
    def __init__(self, code: str, name: str, classsize: int, creditno: int, coursetype, preqs: List['Course'] = []) -> None:
        self.code          = code
        self.name          = name
        self.creditno      = creditno
        self.classsize     = classsize
        self.prerequisites = preqs
        self.coursetype    = coursetype

        self.grading__mu    = None        
        self.grading__sigma = None

    def __str__(self) -> str:
        return self.code
    
    def __repr__(self) -> str:
        return self.__str__()
