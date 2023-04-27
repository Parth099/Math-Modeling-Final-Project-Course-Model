#! important
# add this module to $path to allow python to find it later
import sys
import os
sys.path.insert(0, os.getcwd())

from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew

from GraphGeneration.DAGGenerator import DAGGenerator

from dataloader.CourseLoader import CourseDataLoader

from Scheduling.Scheduler import Scheduler
from Scheduling.Models.Student import Student
from Scheduling.Models.Course import Course

from typing import List


"""
Questions an this ABM can answer:
    1.  Given a course list of prereqs how long will students take to complete it?
        Params: Class-sizes (not yet implmented), Grade dists (data not yet collected)
        
    2. How will classsizes create an emergence of bottlenecking classes (small classsize vs large student body)
        Will there be a group of students moving together?
    
    3. Effectness of "weed-out classess"
"""

# colors
BLUE = "#0064cd"
RED  = "#a41e35"

### KEEP TRACK OF STUDENTS PER LEVEL
class CourseABM():

    def __init__(self, datapath: str, num_students: int, USE_HISTORY_BASED_GRADING=True) -> None:
        self.num_students = num_students
        COURSE_DATA_PATH = datapath        # path to file to be load

        CDL      = CourseDataLoader(COURSE_DATA_PATH)
        self.DAG = DAGGenerator(CDL.course_info, CDL.course_map)

        self.students  = [Student(CDL.course_map, HISTORY_BASED_GRADING=USE_HISTORY_BASED_GRADING) for _ in range(num_students)]
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

        for semester in range(self.scheduler.get_highest_semester()+1):
            pass_count, fail_count = self.scheduler.get_passing_and_failing_counts(semester)

            # default label is empty (no data about a class is shown)
            labels = defaultdict(str)

            # count up passes and fails
            for key in pass_count:
                _label = f'Passed: {pass_count[key]}\nFailed: {fail_count[key]}'
                labels[key] = _label


            self.DAG.draw_graph_via_PYG(labels, f'Semeter {semester+1}') \
                .draw(f'./img/sample-{semester}.png', format='png')

    def gen_semester_dist(self, output_name="sem-hist.png"):
        semester_counts = [stu.semester for stu in self.students]
        semester_skew = skew(semester_counts) 
        ave = np.mean(semester_counts)

        # make bins discreet to help with charts
        bins = np.arange(6-0.5, np.max(semester_counts)+3-0.5, 1)
        plt.hist(semester_counts, bins=bins, edgecolor="black")

        plt.title("# Semesters taken Graduation average={__ave:.4f},skew={__skew:.4f}".format(__skew=semester_skew, __ave=ave))
        plt.ylabel("# Students")
        plt.xlabel("# Semesters")

        # save to destination
        plt.savefig(f"./img/{output_name}")
        plt.clf()

        return semester_skew, ave

    def gen_bottleneck_chart(self, output_name="sem-bn.png"):
        bottlenecks = self.scheduler.bottlenecks

        # sort to get most requested classes at the end
        sorted_bn = sorted(bottlenecks.items(), key=lambda k_v: k_v[1])
        
        # use to chart
        courses: List[Course] = []
        num_req: List[int]    = []
        for c_pair, n_pair in sorted_bn:
            courses.append(c_pair)
            num_req.append(n_pair)

        x_axis = np.arange(len(courses))

        bar_colors = [RED if c.coursetype == 'major' else BLUE for c in courses ]

        plt.bar(x_axis, num_req, width=0.2, tick_label=courses, color=bar_colors)
        plt.title(f"Classes Reqested by Students (Student={self.num_students})")
        plt.savefig(f'./img/{output_name}')


# run script
if __name__ == '__main__':
    ABM = CourseABM("./data/prereq.json", 150, USE_HISTORY_BASED_GRADING=0)
    ABM.run()
    __skew, __ave = ABM.gen_semester_dist()
    ABM.gen_graphs()
    ABM.gen_bottleneck_chart()


