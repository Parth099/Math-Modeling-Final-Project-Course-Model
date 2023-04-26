#! important
# add this module to $path to allow python to find it later
import sys
import os
sys.path.insert(0, os.getcwd())

from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from GraphGeneration.DAGGenerator import DAGGenerator

from dataloader.CourseLoader import CourseDataLoader

from Scheduling.Scheduler import Scheduler
from Scheduling.Models.Student import Student


"""
Questions an this ABM can answer:
    1.  Given a course list of prereqs how long will students take to complete it?
        Params: Class-sizes (not yet implmented), Grade dists (data not yet collected)
        
    2. How will classsizes create an emergence of bottlenecking classes (small classsize vs large student body)
        Will there be a group of students moving together?
    
    3. Effectness of "weed-out classess"
"""

### KEEP TRACK OF STUDENTS PER LEVEL
class CourseABM():

    def __init__(self, datapath: str, num_students: int) -> None:
        COURSE_DATA_PATH = datapath        # path to file to be load

        CDL      = CourseDataLoader(COURSE_DATA_PATH)
        self.DAG = DAGGenerator(CDL.course_info, CDL.course_map)

        self.students  = [Student(CDL.course_map) for _ in range(num_students)]
        self.courses   = CDL.course_info
        self.scheduler = Scheduler(self.students, self.courses, CDL.course_map, CDL.grad_reqs)

        self.has_run = False

    # run semesters
    def run(self, verbose=False):
        while not all([stu.is_finished for stu in self.students]):
            self.scheduler.assign_classes() # could be multi thread
            self.scheduler.increment_semester() # could be multi threaded

            if verbose: print("INCREMENT SEMESTER")

        self.has_run = True

    def gen_graphs(self):

        if not self.has_run:
            raise RuntimeError("gen_graph called before run()")

        for semester in range(self.scheduler.get_highest_semester()):
            pass_count, fail_count = self.scheduler.get_passing_and_failing_counts(semester)

            # default label is empty (no data about a class is shown)
            labels = defaultdict(str)

            # count up passes and fails
            for key in pass_count:
                _label = f'Passed: {pass_count[key]}\nFailed: {fail_count[key]}'
                labels[key] = _label


            self.DAG.draw_graph_via_PYG(labels, f'Semeter {semester}').draw(f'./img/sample-{semester}.png')

    def gen_semester_dist(self):
        semester_counts = [stu.semester for stu in self.students]

        # make bins discreet to help with charts
        bins = np.arange(6-0.5, np.max(semester_counts)+3-0.5, 1)
        plt.hist(semester_counts, bins=bins, edgecolor="black")

        # save to destination
        plt.savefig("./img/sem-hist.png")
        

ABM = CourseABM("./data/prereq.json", 150)
ABM.run()
ABM.gen_graphs()
ABM.gen_semester_dist()

# behaviors
#   grad semester WRT grading averages and STD dist
#   random grading vs behavior based grading