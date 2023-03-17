import sys, os
sys.path.insert(0, os.getcwd()) # add this module to $path to allow python to find it later

from dataloader.CourseLoader import CourseDataLoader
from GraphGeneration.DAGGenerator import DAGGenerator

from Scheduling.Models.Student import Student
from Scheduling.Scheduler import Scheduler

from collections import defaultdict

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

orders = DAG.generate_K_topological_orderings(70, 0.001)

students = [Student(order, CDL.course_map) for order in orders]
courses  = CDL.course_info

scheduler = Scheduler(courses, students, CDL.course_map)
scheduler.assign_classes()

while not all([stu.is_finished for stu in students]):

    scheduler.increment_semester()
    scheduler.assign_classes()
    
    
for semester in range(scheduler.get_highest_semester()):
    pass_count, fail_count = scheduler.get_passing_and_failing_counts(semester)
    labels = defaultdict(str)

    for key in pass_count:
        labels[key] = f'Passed: {pass_count[key]}\nFailed: {fail_count[key]}'
        
        
    DAG.draw_graph_via_PYG(labels).draw(f'./img/sample-{semester}.png')



#G = DAG.draw_graph_via_PYG(labels)
#G.draw("./img/sample.png")
