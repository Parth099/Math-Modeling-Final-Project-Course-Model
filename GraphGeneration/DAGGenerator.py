import networkx as nx

from Models.Course import Course
from typing import Dict


class DAGGenerator():

    # static vars
    NODE_COLOR = "#a41e35"
    NODES_PER_LAYER = 5

    def __init__(self, course_info: Dict[str, Course], course_name_to_index: Dict[str, int]):
        
        # generate empty graph
        self.G = nx.DiGraph()

        # add all the nodes first before adding connections
        node_values: list[int] = course_name_to_index.values()
        [self.G.add_node(node, subset=node % DAGGenerator.NODES_PER_LAYER) for node in node_values]

        # add connections
        for course, data in course_info.items():
            # get dest: in the context of prereqs; the destination is the current node
            destination_node = course_name_to_index[course]

            # if no connections, move on
            if not data.prerequisites:
                continue

            for prereq in data.prerequisites:
                # get destination mapping
                source_node = course_name_to_index[prereq.code]

                # add connection
                self.G.add_edge(source_node, destination_node)

    def draw_graph(self, graph_labels: Dict[int, str]):
        '''draws a graph given `graph_labels`'''
        nx.draw_networkx(self.G, 
                    with_labels=True, 
                    labels=graph_labels, 
                    pos=nx.multipartite_layout(self.G, align="vertical"), 
                    node_color=DAGGenerator.NODE_COLOR)

