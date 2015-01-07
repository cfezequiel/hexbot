# hexbot
Robot path planning algorithm for terrain represented as a hex grid.
Coded in Python.

## Files

- `path.py`: Python script for running the least cost path algorithm
- `data.csv`: Sample hex grid CSV file
- `data_int.csv`: Integer representation of hex grid (for verification)

### path.py:

Computes the least cost path from source (top-left) to destination 
(bottom right).
Output is a list of characters indicating steps that robot should take to
traverse the grid towards the destination.
- 'u' - up
- 'd' - down
- 'l' - left
- 'r' - right

Example:
r, r, d, d, r, d, d, r, r, d

```
Command:
$ python path.py <hexgrid CSV file>
```

## Third-party libraries
The **pygraph** library was used for representing the graph data structure in
Python and for implementing Dijkstr's algorithm.

Website: https://code.google.com/p/python-graph/


## Notes

### Algorithm

The problem of finding a least cost path from source to destination in a grid of
values representing terrain can be represented as a graph problem, and can be
solved in polynomial time using Dijkstra's algorithm.

Djikstra's algorithm was chosen in order to find the least cost path since it is
a well-known and is commonly used for solving least cost or shortest path
problems (assuming nonnegative costs).


### Performance

The algorithm implementation (inclusive of data conversion) has a total complexity of 
approximately O(n^2) or big-O of n-squared.

The steps performed are broken down as follows:

1. Read hexgrid from file (with row/column iteration of data entries): O(n^2)
2. Create directed graph (row/column iteration for nodes and edges): O(n^2)
3. Shortest path via Dijkstra's (with sorted list): O(|V| + |E|) approx. O(n^2)
4. Reverse tracing of path from destination to origin: O(n)


### Memory

Use of data structures was minimized to the following:

- A graph data structure was used for representing the grid for path planning.
  - This is implemented as an adjacency list using dictionaries (for nodes and edges).
- Another data structure was used to store the hex grid data as list of lists.
- A list for storing the least cost path.
- Another list for storing the directions of the least cost path.

Since the input data is small, memory usage was not an issue.

No C extensions for allocating/deallocating memory were explicitly used by the
code author.

### Output

Based on the data from `hexgrid.csv`, the least cost path output is:

r, r, d, d, r, d, d, r, r, d

