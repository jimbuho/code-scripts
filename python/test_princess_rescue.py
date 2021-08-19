"""

Test Hackerrank IA Princess Rescue in Python

@author dgonzalez

"""
import datetime

class Neighbour:
    """

    A Node Neighbour Representation

    """
    def __init__(self, name, location):
        self.name = name
        self.location = location

class Node:
    """

    A Graph Node Representation

    """
    def __init__(self, name='', color='', neighbours=[]):
        self.name = name
        self.neighbours = neighbours
        self.color = color

    def get_neighbour(self, node):
        """ Returns the node neighbour by name """
        return next((x for x in self.neighbours if x.name == node.name), None)

    def __str__(self):
        return self.name

class Graph:
    """

    The Matrix represented as Graph

    """
    def __init__(self, matrix, size):
        self.nodes = {}
        self.matrix = matrix
        self.size = size

    def build(self):
        """ Transforms the simple matrix input in a graph representation """
        N = self.size

        for i in range(0, N * N):
            row, col = i // N, i % N
            node_name = '%d-%d' % (row,col)
            # Build the Node with neighbours
            self.nodes[node_name] = Node(
                name=node_name, 
                color=self.matrix[row][col], 
                neighbours=self.get_neighbours(row,col)
            )

    def get_neighbours(self, r, c):
        """ Get all the neighbours of (r,c) cell """
        n = []
        if r > 0:
            name = '%d-%d' % (r-1,c)
            n.append(Neighbour(name, 'UP'))
        if r < self.size-1:
            name = '%d-%d' % (r+1,c)
            n.append(Neighbour(name, 'DOWN'))
        if c > 0:
            name = '%d-%d' % (r,c-1)
            n.append(Neighbour(name, 'LEFT'))
        if c < self.size-1:
            name = '%d-%d' % (r,c+1)
            n.append(Neighbour(name, 'RIGHT'))
        return n

    def get_node(self, name):
        """ Returns node by its name """
        return self.nodes[name]

    def get_node_by_color(self, color):
        """ Returns node by color """
        return next((v for v in self.nodes.values() if v.color == color), None)

    def traduce(self, path):
        """ Response the path in order of the movements robot has to do in words """
        last_v = None
        for v in path:
            if last_v:
                node = self.nodes[last_v.name]
                n = node.get_neighbour(v)
                if n:
                    yield n.location

            last_v = v

class BFS:
    """

    BFS Algorithm Implementation
    
    """
    def __init__(self, graph):
        self.graph = graph

    def shortest_path(self, start, goal):
        """ Look for the shorts path from start to goal """
        explored, queue = [], [[start]]

        if not start or not goal:
            print("Start and Goal are required")
            return None
         
        if start == goal:
            print("Start and Goal are same")
            return None
        
        while queue:
            #print('Queue BEFORE', [[n.name for n in q] for q in queue])
            path = queue.pop(0)
            node = path[-1]
            #print('Queue AFTER', [[n.name for n in q] for q in queue])
            
            if node not in explored:
                for neighbour in node.neighbours:
                    new_path = list(path)
                    new_path.append( self.graph.get_node(neighbour.name) )
                    queue.append(new_path)
            
                    # The robot achieves the goal
                    if neighbour.name == goal.name:                        
                        return new_path

                explored.append(node)
        
        print("The path to goal was not reached")
        return None


def displayPathtoPrincess(n, grid):
    """ Print all moves the robot has to do to rescue the princess"""
    start = datetime.datetime.now()

    graph = Graph(grid, n) 
    graph.build()

    bfs = BFS(graph)
    sp = bfs.shortest_path(graph.get_node_by_color('m'), 
                           graph.get_node_by_color('p'))
    
    if sp:
        # We have the solution now, but is needed to traduce it
        route = graph.traduce(sp)

        for p in route:
            print(p)

    end = datetime.datetime.now()
    timelapse = start - end
    print("Execution Timelapse:", timelapse.microseconds, "microseconds")

game = [
    ['-','m','-'],
    ['-','-','-'],
    ['p','-','-'],
]

displayPathtoPrincess(3, game)