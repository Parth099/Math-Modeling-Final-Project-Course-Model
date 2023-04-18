from collections import defaultdict

from dataloader.JsonLoader import JsonLoader
from typing import Dict, DefaultDict, List, Set

from Scheduling.Models.Course import Course


class CourseDataLoader(JsonLoader):
    """object that loads in course data based on a json object"""

    def __init__(self, path: str) -> None:
        # load in json (this generates self.data)
        super().__init__(path)

        # raise ERROR if self.data is none or empty
        if(self.data is None):
            raise ValueError("File data is None")

        # take data and serialize it
        # this variable maps name of course to all of its information
        self.__course_json_data = self.data['courses']
        self.grad_reqs = self.data['requirements']

        # take json info to its python class
        self.course_info = self.jsonToCourse(self.__course_json_data)

        # create graph labels and integer mappings
        self.course_map, _ = self.generateMetaDataFromCourseDict(
            self.course_info)

    def jsonToCourse(self, json_data: list) -> Dict[str, Course]:
        """take a json file and turn it into a dict based on the outermost key where each value is a (cached) Course Object"""

        course_dict: dict[str, Course] = {}
        course_type_dict: DefaultDict[str, List[Course]] = defaultdict(list)

        # preload courses so prereqs can be loaded
        for course in json_data:
            # EXT details out of json array element
            code = course['code']
            name = course['name']
            creditno = course['creditno']
            classsize = course['classsize']
            coursetype = course['coursetype']
            requirements = course['requirements']

            # add finished course to cache
            course_dict[code] = Course(code, name, classsize, creditno, coursetype, [], requirements)

            # add course to a cache that sorts by coursetype
            course_type_dict[coursetype].append(course_dict[code])

        # load in course prereqs and merge requirements
        for course in json_data:
            code = course['code']
            Current_Course = course_dict[code]

            # insert prereqs
            for prereq_code in course['prerequisites']:
                Cached_Class = course_dict[prereq_code]
                Current_Course.prerequisites.append(Cached_Class)

            # merge requirements and mask them as prereqs
            req_list: List[Course] = []
            for req in Current_Course.requirements:
                # collect all required classes
                req_list += course_type_dict[req]

            # shake off non unique elements
            req_set: Set[Course] = set(req_list)
            
            # push to prereqs
            for req in req_set:
                Current_Course.prerequisites.append(req)

        # return the cache
        return course_dict

    def generateMetaDataFromCourseDict(self, course_dict: Dict[str, Course]):
        """
        Generates:
                (1) dict where integer maps to course_name\n
                (2) reversed dict (1)
        """

        # dict (1)
        int_to_name: Dict[int, str] = dict(enumerate(course_dict.keys()))

        # dict (2)
        name_to_int: Dict[str, int] = {
            value: key for (key, value) in int_to_name.items()}

        # labels, map
        return name_to_int, int_to_name,
