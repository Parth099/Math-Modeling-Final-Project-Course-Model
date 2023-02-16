import networkx as nx
import matplotlib.pyplot as plt 

from random import shuffle
from LoadData import COURSES, ENUMERATED_COURSES, ENUMERATED_COURSES_REV, GRAPH_LABELS

from typing import Tuple, List

edges: List[Tuple[int, int]] = []
G = nx.DiGraph()

print(ENUMERATED_COURSES_REV)

for course, course_data in COURSES.items():
    src_integer_value = ENUMERATED_COURSES_REV[course]

    if not course_data.prerequisites:
        G.add_node(src_integer_value)
        continue

    for prereq in course_data.prerequisites:
        preq_integer_value = ENUMERATED_COURSES_REV[prereq.code]
        G.add_edge(preq_integer_value, src_integer_value)


# nx.all_topological_sorts(G)