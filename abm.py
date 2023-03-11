import sys, os
sys.path.insert(0, os.getcwd()) # add this module to $path to allow python to find it later

import networkx as nx
import matplotlib.pylab as plt

from dataloader.CourseLoader import CourseDataLoader
from GraphGeneration.DAGGenerator import DAGGenerator

from Scheduling.Models.Student import Student
from Scheduling.Scheduler import Scheduler


COURSE_DATA_PATH = "./data/prereq.json"        # path to file to be load
CDL = CourseDataLoader(COURSE_DATA_PATH)
DAG = DAGGenerator(CDL.course_info, CDL.course_map)

DEFAULT_LABELS = CDL.graph_labels

fig, ax =  DAG.draw_graph(DEFAULT_LABELS)
orders = DAG.generate_K_topological_orderings(1, 0.001)

students = [Student(order, CDL.course_map) for order in orders]
courses  = CDL.course_info

scheduler = Scheduler(courses, students, CDL.course_map)
scheduler.assign_classes()

while 1:
    for stu in scheduler.students:
        print(f'{stu.name} in Semester: {stu.semester}')
        print("Taking: ", stu.is_taking)
        print("Taken : ", stu.has_taken)
        print("Failed: ", stu.has_failed)  
        print("-" * 50)
        
    input()
    scheduler.increment_semester()
    scheduler.assign_classes()

    