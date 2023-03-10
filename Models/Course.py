"""
This file defines the <Course> Object used to 
"""

# type hint a class from within it self
from typing import List

class Course: 
    def __init__(self, code: str, name: str, classsize: int, creditno: int, preqs: List['Course'] = []) -> None:
        self.code          = code
        self.name          = name
        self.creditno      = creditno
        self.classsize     = classsize
        self.prerequisites = preqs

    def __str__(self) -> str:
        return self.code
