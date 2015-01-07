'''
Compute shortest path along the hex grid terrain model.

Source: top-left-most point
Destination: bottom-right-most point
'''

import sys
from itertools import tee, izip
import csv

from pygraph.classes.digraph import digraph
from pygraph.readwrite.dot import write
from pygraph.algorithms.minmax import shortest_path

def read_hexgrid(filename):
    ''' Read CSV file containing hexgrid data.'''

    grid = []
    with open(filename, 'rb') as fp:
        reader = csv.reader(fp, delimiter=',')
        for row in reader:
            grid.append([int(r, 16)for r in row])

    return grid

def pack(i, j):
    '''Combine two integers into a string.'''

    return '%s_%s' % (i, j)

def unpack(x):
    '''
    Split a string into two integers.

    Separator is underscore '_' character.
    Used together with pack.
    '''

    a, b = x.split('_')
    return (int(a), int(b))

def create_digraph(grid):
    '''Create a directed graph from hex grid.'''

    gr = digraph()

    m = len(grid)
    for i, row in enumerate(grid): 
        for j, cur_val in enumerate(row):
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

                down_val = grid[i+1][j]
                edge_cost = cur_val + down_val
                gr.add_edge((cur, down), wt=edge_cost)
                gr.add_edge((down, cur), wt=edge_cost)

            if j < n - 1:
                right = pack(i, j+1)
                if not gr.has_node(right):
                    gr.add_node(right)
                right_val = grid[i][j+1]
                edge_cost = cur_val + right_val
                gr.add_edge((cur, right), wt=edge_cost)
                gr.add_edge((right, cur), wt=edge_cost)

    return gr

def trace_path(path, dst):
    '''Trace path from destination to source.'''

    cur = dst
    trace = [cur]
    while path[cur]:
        cur = path[cur]
        trace.append(cur)

    trace.reverse()
    return trace 

def pairwise(iterable):
    '''
    Returns list of (current, next) element pairs of input list
    '''

    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def show_move_path(path):
    '''Display path according to direction taken.'''


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

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage: python %s <hexgrid CSV file>' % sys.argv[0].split('/')[-1]
        exit(1)

    # Read hexgrid from file
    filename = sys.argv[1]
    grid = read_hexgrid(filename)

    # Create a directed graph from the grid
    gr = create_digraph(grid)

    # Get shortest path to all nodes from source node using Dijkstra's
    src = pack(0,0)
    paths, _ = shortest_path(gr, src)

    # Trace the output path from source to given destination
    dst = pack(5,5)
    path = trace_path(paths, dst)

    # Display path as directions (e.g. 'r' for right, 'd' for down)
    print ', '.join(show_move_path(path))


