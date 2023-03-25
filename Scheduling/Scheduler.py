from Scheduling.Models.Course import Course
from Scheduling.Models.Student import Student

from random import shuffle
from typing import List, Dict, Counter

from collections import Counter


class Scheduler:
    """Scheduler takes steps WRT open courses and availble"""

    CREDITS_THRESHOLD = 14

    def __init__(self, Students: List[Student], Courses: Dict[str, Course], course_map: Dict[str, int]) -> None:
        self.students = Students
        self.course_map = course_map
        self.__courses = Courses

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

    def read_class_capacity(self, courses: Dict[int, Course]):
        self.__class_caps = {int_code: course.classsize for (
            int_code, course) in courses.items()}

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

        # approved if no prerequisites exist
        if not course.prerequisites:
            return True

        # read in all classes a student has taken
        completed_classes = student.has_taken

        # make each class to its integer representation
        completed_classes_int = [self.course_map[_course.code]
                                 for _course in completed_classes]

        # get into prereqs
        prereqs = course.prerequisites

        # map each item to a number
        prereqs_int = [self.course_map[prereq.code] for prereq in prereqs]

        # if each of the numbers in prereqs appears in completed_classes, this student can take that class
        return all([class_num in completed_classes_int for class_num in prereqs_int])

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
