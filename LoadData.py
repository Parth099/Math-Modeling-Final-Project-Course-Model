import json as JSON
from Course import Course

from typing import List

CourseType = Course

# load data from json file in a text format
def loadJson(path_to_json: str):
    data = None
    with open(path_to_json, 'r') as json_file:
        data = JSON.load(json_file)

    return data

# take json data to <Course>
def jsonToCourse(json_data: list) -> dict[str, CourseType]:

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
    

COURSE_DATA_PATH = "./data/prereq.json"        # path to file to be load
DATA = loadJson(COURSE_DATA_PATH)              # load file
COURSES = jsonToCourse(DATA)                   # file -> json 

