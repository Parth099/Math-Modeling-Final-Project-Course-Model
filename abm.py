import sys, os
sys.path.insert(0, os.getcwd()) # add this module to $path to allow python to find it later

import networkx as nx
import matplotlib.pylab as plt

from dataloader.CourseLoader import CourseDataLoader
from GraphGeneration.DAGGenerator import DAGGenerator


COURSE_DATA_PATH = "./data/prereq.json"        # path to file to be load
CDL = CourseDataLoader(COURSE_DATA_PATH)
DAG = DAGGenerator(CDL.course_info, CDL.course_map)

DEFAULT_LABELS = CDL.graph_labels

fig, ax =  DAG.draw_graph(DEFAULT_LABELS)
plt.show()