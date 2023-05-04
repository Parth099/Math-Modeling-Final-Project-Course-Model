from collections import defaultdict, Counter
from random import shuffle, randint, sample
from typing import List, Dict, DefaultDict


from Scheduling.Models.Course import Course
from Scheduling.Models.Student import Student


class Scheduler:
    """Scheduler takes steps WRT open courses and availble"""

    CREDITS_THRESHOLD = 14

    def __init__(self, Students: List[Student], Courses: Dict[str, Course], course_map: Dict[str, int], requirements: Dict[str, int]) -> None:
        self.students = Students
        self.course_map = course_map
        self.__courses = Courses
        self.requirements = requirements

        self.bottlenecks: DefaultDict[Course, int]  = defaultdict(int)

        # int -> Course Map
        self.courses: Dict[int, Course] = {}

        # create an int -> info map to be used later
        for name, int_mapping in course_map.items():
            self.courses[int_mapping] = Courses.get(name)

            # int -> class limit mapping
        self.__class_caps: Dict[int, int] = {}
        self.read_class_capacity(self.courses)

        # generate requirement layout
        self.buckets = self.__generate_course_buckets()

        # validate bucket information
        self.__validate_courses_with_requirements(self.requirements, self.buckets)

        # assign students their classes
        self.__assign_course_plans(self.students)

    def read_class_capacity(self, courses: Dict[int, Course]):
        self.__class_caps = {int_code: course.classsize for (int_code, course) in courses.items()}

    def update_class_capacity(self, selected_class: int):
        """Update the class capacities
                This function is used to decrement class count by 1 to reserve a spot for a student. 

        Args:
                selected_class (int): numerical ID of the class you trying to effect

        Raises:
                KeyError: on invalid `selected_class`

        Returns:
                _type_: T/F on if the student was placed in the class
        """

        if selected_class not in self.__class_caps:
            raise KeyError(
                f'Tried to alter class capacity, key={selected_class} doesnt exist in dict')

        spaceLeft = self.__class_caps[selected_class] > 0

        if spaceLeft:
            # decrement to reserve a space
            self.__class_caps[selected_class] -= 1
        return spaceLeft

    def student_can_take_class(self, student: Student, course: Course) -> bool:
        """returns T/F on whether a Student `student` can take a Course `course`

        Args:
                student (Student): 
                course (Course): 

        Returns:
                bool
        """
        def has_prereqs_met(prereqs: List[Course]):
            if not prereqs: return True

            # check if all prereqs are a subset of student.has_taken
            return all(course in student.has_taken for course in prereqs)

        def has_requirements_met():
            
            # load in requirements
            requirements = course.requirements
            prereqs = course.prerequisites

            if not requirements: return True, prereqs

            # read in all classes a student has taken
            completed_classes = student.has_taken

            for req in requirements:
                bucket = self.buckets[req]

                # generator expression to utlize short circuting
                if any(course in completed_classes for course in bucket):
                    prereqs = [prereq for prereq in prereqs if prereq not in bucket]
                    continue
                # false return if we ever bypass the continue meaning the requirement has not been met
                return False, None
                
            return True, prereqs

        # returns if requirements have been met and filters down the prereq list based on what reqirememts meet which prereqs
        has_met_requirements, filtered_prereq_list = has_requirements_met()

        return has_met_requirements and has_prereqs_met(filtered_prereq_list)
            
            
    def assign_classes(self):
        """select class based on availble classes"""

        # shuffle array of students to give each one a fair chance of selecting first
        shuffle(self.students)  # (inplace sort)

        for stu in self.students:

            if stu.is_finished:
                continue

            # order the student wants
            ordering = stu.course_plan

            # raise error if ordering is not assign
            if ordering is None:
                raise ValueError("Student has not been assigned a course plan")

            for course in ordering:

                C = self.courses.get(course)

                if C is None:
                    raise ValueError("Course $C is none")

                # if student has registered for enough classes, allow other students to register
                if stu.curr_credit_count >= Scheduler.CREDITS_THRESHOLD:
                    break

                # if class is possible, assign it
                if not self.student_can_take_class(stu, C):
                    continue

                # class is possible to assign so attempt to assign
                class_index = self.course_map.get(C.code, None)

                # assign to student if there is space left
                if self.update_class_capacity(class_index):
                    stu.assign_class(C)
                else:
                    self.bottlenecks[C] += 1 

    def increment_semester(self):
        """Move each student up a semester"""
        for stu in self.students:
            if not stu.is_finished:
                stu.increment_semester()

        # reset capacity
        self.read_class_capacity(self.courses)

    def get_highest_semester(self):
        return max([stu.semester for stu in self.students], default=0)

    def __get_semester_PF_counts(self, semester: int):
        """gets the students counts for passing and total students taking the class by `semester`

        Args:
                semester (int)

        Returns:
                2 Counter objects\n\n
                (1) - passed students count by class name (str)\n
                (2) - total students taking a class by class name (str)
        """

        Pass_count: Counter[str] = Counter()
        class_sizes: Counter[str] = Counter()

        for stu in self.students:
            semester_history = stu._history.get(semester, {})

            Pass_count.update(semester_history)
            class_sizes.update(semester_history.keys())

        return Pass_count, class_sizes

    def get_passing_and_failing_counts(self, semester: int):
        """gets the passing and failing counts for `semester` and returns them in two counter objects

        Args:
                semester (int): semester to get info for

        Returns:
                2 Counter objects\n\n
                (1) - passed students count by class name (str)\n
                (2) - failed students count by class name (str)
        """
        # call helper to get the passed count and class sizes
        pass_count, sizes = self.__get_semester_PF_counts(semester)

        fail_count: Counter[str] = Counter()

        # use helper info (above) to get num failed
        for course, num_currently_taking in sizes.items():
            num_passed = pass_count.get(course, 0)
            fail_count.update({course: num_currently_taking - num_passed})

        return pass_count, fail_count

    def __generate_course_buckets(self):
        """sorts courses by course name

        returns a Dict[str, List[Course]] where str is the course.coursetype
                """

        buckets: Dict[str, List[Course]] = {}

        # sort items by course_type
        for course in self.__courses.values():

            key = course.coursetype

            bucket = buckets.get(key, [])
            bucket.append(course)

            buckets[key] = bucket

        return buckets

    def __validate_courses_with_requirements(self, requirements: Dict[str, int], buckets: Dict[str, List[Course]]):
        """validates bucket information against requirements present

                Raises:
                        ValueError: on invalid config
                """
        for requirement, num_required_classes in requirements.items():

            # if a requirement isnt even present or the number of classes isnt correct
            if requirement not in buckets or len(buckets[requirement]) < num_required_classes:
                raise ValueError(
                    f'Num required of coursetype={requirement} not possible, more required then present\n'
                    f'Num required: {num_required_classes}, Num Present: {len(buckets.get(requirement, []))}')

    def __assign_course_plans(self, Students: List[Student]):
        """Attaches a course plan to a student based on a the requirements of a major

        Args:
            Students (List[Student])
        """
        for student in Students:
            # given a set of courses not all are required, thus method below selects classes required to graduate
            generated_courses = self.__create_course_plan(self.buckets, self.requirements)

            # this randomizes the classes give each student a course map they have some desire to take
            shuffle(generated_courses)
            student.course_plan = generated_courses
        

    def __create_course_plan(self, buckets: Dict[str, List[Course]], requirements: Dict[str, int]):
        """create course plan based on course layout that meets all `requirements`. A `requirement` wih no bucket
        is assumed to be required. 

        Args:
            buckets (Dict[str, List[Course]]): courses sorted by coursetype
            requirements (Dict[str, int]): requirements in terms of classes per bucket label (coursetype)

        Returns:
            List[int]: classes to be taken
        """

        ordering:List[Course] = []

        for bucket_name, classes in buckets.items():

            # if the bucket name corresponds to a requirement only add in the number of courses required
            if bucket_name in requirements:
                # generate a random number of items to select from this bucket based on its min and max values
                #   min = required amount, max = all possible items
                num_to_select = randint(requirements[bucket_name], len(classes))
                randomly_selected_classes = sample(classes, num_to_select)

                # save selected classes that filfil requirements
                ordering += randomly_selected_classes

                # add in relavent prereqs if needed
                for rand_classes in randomly_selected_classes:
                    for prereq in rand_classes.prerequisites:
                        if prereq not in ordering: ordering.append(prereq)

                # if there are no requirements, that course bucket needs to be entirely completed            
            else:
                # else add in all courses
                # this is where all 'major' classes get added to the requirement system
                ordering += classes

        # remap to integer to later use
        return [self.course_map[course.code] for course in ordering]
