import networkx as nx
import matplotlib.pyplot as plt 

from random import shuffle

from Course import Course
from LoadData import COURSES, ENUMERATED_COURSES_MAPPING, GRAPH_LABELS

from typing import Tuple, List, Dict, Type


# constant
NODE_COLOR = "#a41e35"
NODES_PER_LAYER = 5

def gen_DAG_from_course_dict(Course_dict: Dict[str, 'Course'], course_to_int_dict: Dict[str, int]):
    # create empty graph
    G = nx.DiGraph()

    node_numbers: List[int] = course_to_int_dict.values()
    [G.add_node(num, subset=num % NODES_PER_LAYER) for num in node_numbers]

    # add the connection
    for course, course_data in Course_dict.items():
        src_integer_value = course_to_int_dict[course]

        # no prerequisites -> no connections
        if not course_data.prerequisites:
            continue

        for prereq in course_data.prerequisites:
            preq_integer_value = course_to_int_dict[prereq.code]
            G.add_edge(preq_integer_value, src_integer_value)

    return G

COURSE_DAG = gen_DAG_from_course_dict(COURSES, ENUMERATED_COURSES_MAPPING)
# TPS = nx.all_topological_sorts(COURSE_DAG)

nx.draw_networkx(COURSE_DAG, 
                with_labels=True, 
                labels=GRAPH_LABELS, 
                pos=nx.multipartite_layout(COURSE_DAG, align="vertical"), 
                node_color=NODE_COLOR)

plt.show()
