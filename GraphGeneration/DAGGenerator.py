# for graph modeling
import networkx as nx
import pygraphviz as pyg

import matplotlib.pyplot as plt
from random import random as rand

from Scheduling.Models.Course import Course
from typing import Dict, List, DefaultDict, Union

OrderingList = List[List[int]]

class DAGGenerator():

    # static vars
    NODE_COLOR = "#a41e35"
    NODES_PER_LAYER = 5
    
    # node shapes for pyg
    NODE_SHAPE_BY_COURSETYPE = {"major": 'note', 'gened': "oval"}
    NODE_SHAPE_DEFAULT = 'note'
    

    def __init__(self, course_info: Dict[str, Course], course_name_to_index: Dict[str, int]):
        
        # generate empty graph
        self.G: nx.DiGraph = nx.DiGraph()
    
        # store given data
        self.course_info: Dict[str, Course] = course_info

        # add all the nodes first before adding connections
        node_values: list[int] = course_name_to_index.values()
        [self.G.add_node(node, subset=node % DAGGenerator.NODES_PER_LAYER)  for node in node_values]

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

    def draw_graph_via_PLT(self, graph_labels: Dict[int, str]):
        '''draws a graph given `graph_labels`'''
        
        fig, ax = plt.subplots()
        
        nx.draw_networkx(self.G, 
                    with_labels=True, 
                    labels=graph_labels, 
                    pos=nx.multipartite_layout(self.G, align="vertical"), 
                    node_color=DAGGenerator.NODE_COLOR,
                    ax=ax)
        
        return fig, ax

    def __re_generate_PYG_graph_from_internal_data(self, labels: DefaultDict[str, str]):
        """private method to generate a PYG model of the working graph from already stored data
        """        
        G = pyg.AGraph(directed=True, prog="dot")
        
        # add in all nodes
        for course_name in self.course_info.keys():
            
            # obtain course type (major, gened, ...)
            coursetype = self.course_info.get(course_name).coursetype
            
            # determine how to display its shape by coursetype
            _shape = DAGGenerator.NODE_SHAPE_BY_COURSETYPE.get(coursetype, DAGGenerator.NODE_SHAPE_DEFAULT)
            
            # generate labels (pass-fail counts)
            _label = f'{course_name}\n\n{labels[course_name]}'
            
            G.add_node(course_name, label=_label, shape=_shape)
            
        
        
        # add in connections
        for course_name, course_info in self.course_info.items():
            
            if not course_info.prerequisites: continue
            
            for prereq in course_info.prerequisites:
                G.add_edge(prereq.code, course_name)
                
        return G
        
        
    
    def draw_graph_via_PYG(self, labels: DefaultDict[str, str], title: str):
        """Draw a graph from given data via pygraphviz

        Args:
            graph_labels (Dict[int, str]): labels on the graph's nodes
        """
        G = self.__re_generate_PYG_graph_from_internal_data(labels)
        G.layout("dot")

        G.graph_attr["label"]   = title
        
        G.node_attr["shape"]    = 'note'
        G.node_attr["color"]    = "#a41e35"
        return G
 
    
    def generate_K_topological_orderings(self, K: int, ordering_acceptance_prob: float) -> OrderingList:
        """generates `k` topological_orderings of the initialized graph

        Args:
            K (int): number of orderings wanted
            ordering_acceptance_prob (float): chance to accept an ordering to be in the list. 
                The lower it is the more "random" the orderings will be

        Returns:
            List[List[int]]: orderings
        """
        
        orderings: OrderingList = []
        
        while len(orderings) < K:
            
            # nx.all_topological_sorts -> Generator
            for ordering in nx.all_topological_sorts(self.G):
                # reject orderings randomly
                if rand() > ordering_acceptance_prob: continue
                
                orderings.append(ordering)
                
                # end generator cycle if all orderings were generated
                if len(orderings) >= K: break
        
        return orderings

            