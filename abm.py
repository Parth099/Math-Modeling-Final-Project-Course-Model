from collections import defaultdict
from Scheduling.Scheduler import Scheduler
from Scheduling.Models.Student import Student
from GraphGeneration.DAGGenerator import DAGGenerator
from dataloader.CourseLoader import CourseDataLoader
import sys
import os
# add this module to $path to allow python to find it later
sys.path.insert(0, os.getcwd())


"""
Questions an this ABM can answer:
    1.  Given a course list of prereqs how long will students take to complete it?
        Params: Class-sizes (not yet implmented), Grade dists (data not yet collected)
        
    2. How will classsizes create an emergence of bottlenecking classes (small classsize vs large student body)
        Will there be a group of students moving together?
    
    3. Effectness of "weed-out classess"
"""


COURSE_DATA_PATH = "./data/prereq.json"        # path to file to be load
CDL = CourseDataLoader(COURSE_DATA_PATH)
DAG = DAGGenerator(CDL.course_info, CDL.course_map)

students = [Student(CDL.course_map) for _ in range(100)]
courses = CDL.course_info

scheduler = Scheduler(students, courses, CDL.course_map, CDL.grad_reqs)

# run semesters
while not all([stu.is_finished for stu in students]):
    scheduler.assign_classes()
    scheduler.increment_semester()

# read semester data
for semester in range(scheduler.get_highest_semester()):
    pass_count, fail_count = scheduler.get_passing_and_failing_counts(semester)
    labels = defaultdict(str)

    for key in pass_count:
        _label = f'Passed: {pass_count[key]}\nFailed: {fail_count[key]}'
        labels[key] = _label


    DAG.draw_graph_via_PYG(labels).draw(f'./img/sample-{semester}.png')
