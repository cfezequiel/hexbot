from itertools import tee, izip
import csv

#Third-party libraries
from pygraph.classes.digraph import digraph
from pygraph.readwrite.dot import write
from pygraph.algorithms.minmax import shortest_path

# Read csv file containing data
input_file = 'data.csv'
data = []
with open(input_file, 'rb') as fp:
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        data.append(row)

# Build graph from data
def get_edge_cost(src, dst):
    src_val = int('0x' + src, 16)
    dst_val = int('0x' + dst, 16)
    result = src_val + dst_val
    return result

gr = digraph()

# Combine two integers into a string
pack = lambda i, j: '%s_%s' % (i, j)

m = len(data)
for i, row in enumerate(data): 
    for j, cur_val in enumerate(row): #O(n^2)
        n = len(row)
        # Add node if possible
        cur = pack(i,j)
        if not gr.has_node(cur):
            gr.add_node(cur)

        # Add node and edge (if possible)
        if i < m - 1:
            down = pack(i+1, j)
            if not gr.has_node(down):
                gr.add_node(down)

            down_val = data[i+1][j]
            edge_cost = get_edge_cost(cur_val, down_val)
            gr.add_edge((cur, down), wt=edge_cost)
            gr.add_edge((down, cur), wt=edge_cost)

        if j < n - 1:
            right = pack(i, j+1)
            if not gr.has_node(right):
                gr.add_node(right)
            right_val = data[i][j+1]
            edge_cost = get_edge_cost(cur_val, right_val)
            gr.add_edge((cur, right), wt=edge_cost)
            gr.add_edge((right, cur), wt=edge_cost)


# Get shortest path to all nodes from source node using Dijkstra's
src = '0_0'
path, dist = shortest_path(gr, src) #O(n^2)

# Get directional path

def trace_path(path, dst):
    '''Trace path from destination to source.'''
    cur = dst
    trace = [cur]
    while path[cur]:
        cur = path[cur]
        trace.append(cur)

    trace.reverse()
    return trace 

path = trace_path(path, '5_5')

def pairwise(iterable):
    '''
    Returns list of (current, next) element pairs of input list
    '''

    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def show_dir_path(path):
    '''Display path according to direction taken.'''

    def unpack(x):
        a, b = x.split('_')
        return (int(a), int(b))

    moves = []
    for cur, next_ in pairwise(path):
        cur = unpack(cur)
        next_ = unpack(next_)
        if cur[0] > next_[0]: #up
            move = 'u'
        elif cur[0] < next_[0]: #down
            move = 'd'
        elif cur[1] > next_[1]: #left
            move = 'l'
        elif cur[1] < next_[1]: #right
            move = 'r'
        else:
            move = '-'

        moves.append(move)

    return moves
    

print show_dir_path(path)

