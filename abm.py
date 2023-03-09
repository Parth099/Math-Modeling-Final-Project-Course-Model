import networkx as nx
import matplotlib.pylab as plt

from Graph_Generation import COURSE_DAG as G
from Graph_Generation import draw_graph

from LoadData import GRAPH_LABELS

draw_graph(G, GRAPH_LABELS)
plt.savefig('./img/CIS.png')