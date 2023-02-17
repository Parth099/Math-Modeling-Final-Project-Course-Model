import networkx as nx

from Course import Course
from LoadData import COURSES, ENUMERATED_COURSES_MAPPING

from typing import List, Dict

# constants
NODE_COLOR = "#a41e35"
NODES_PER_LAYER = 5

def gen_DAG_from_course_dict(Course_dict: Dict[str, 'Course'], course_to_int_dict: Dict[str, int]):
    # create empty graph
    G = nx.DiGraph()

    node_numbers: List[int] = course_to_int_dict.values()

    # initially gen all nodes and assign them to a layer to later create a multipartite graph
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

def draw_graph(graph_labels: Dict[int, str]):
    nx.draw_networkx(COURSE_DAG, 
                with_labels=True, 
                labels=graph_labels, 
                pos=nx.multipartite_layout(COURSE_DAG, align="vertical"), 
                node_color=NODE_COLOR)

COURSE_DAG = gen_DAG_from_course_dict(COURSES, ENUMERATED_COURSES_MAPPING)


