import json as JSON
from Course import Course

from typing import List, Union, Tuple, Dict

CourseType = Course

# load data from json file in a text format
def loadJson(path_to_json: str):
    data = None
    with open(path_to_json, 'r') as json_file:
        data = JSON.load(json_file)

    return data

# take json data to <Course>
def jsonToCourse(json_data: list) -> Dict[str, CourseType]:
    """take a json file and turn it into a dict based on the outermost key where each value is a (cached) Course Object"""

    course_dict: dict[str, CourseType] = {}

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
    
def generateMetaDataFromCourseDict(course_dict: Dict[str, CourseType]):
    """
    Generates:
        (1) dict where integer maps to course_name\n
        (2) reversed dict (1)
    """

    # dict (1)
    int_to_name: Dict[int, str] = dict(enumerate(course_dict.keys()))


    # dict (2) 
    name_to_int: Dict[str, int] = {value: key for (key, value) in int_to_name.items() }

    return int_to_name, name_to_int
    




COURSE_DATA_PATH = "./data/prereq.json"        # path to file to be load
DATA = loadJson(COURSE_DATA_PATH)              # load file
COURSES = jsonToCourse(DATA)                   # file -> json 

GRAPH_LABELS, ENUMERATED_COURSES_MAPPING = generateMetaDataFromCourseDict(COURSES) # metadata to label graph nodes
