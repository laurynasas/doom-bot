class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reachable = None
    def __str__(self):
        return str(self.x) + " | " + str(self.y)

class Line:
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def __init__(self, a, b):
        self.a = self.Point(*a)
        self.b = self.Point(*b)

    def __str__(self):
        return str(self.a.x) + " " + str(self.a.y) + "; " + str(self.b.x) + " " + str(self.b.y)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vertex:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node


class Helper:
    @staticmethod
    def is_node_reachable(vertex, one_sided_lines):
        for line in one_sided_lines:
            if Helper.intersect(vertex.start_node, vertex.end_node, line.a, line.b):
                vertex.end_node.reachable = False
                return
        vertex.end_node.reachable = True

    @staticmethod
    def map_out_graph(node, map_width, map_length, vertex_length, graph):
        if node.x - vertex_length >= map_width[0]:
            future_left_node = Node(node.x - vertex_length, node.y)
            graph.append_node(future_left_node)
            Helper.map_out_graph(future_left_node, map_width, map_length, vertex_length, graph)

        if node.x + vertex_length <= map_width[1]:
            future_right_node = Node(node.x + vertex_length, node.y)
            graph.append_node(future_right_node)
            Helper.map_out_graph(future_right_node, map_width, map_length, vertex_length, graph)

        if node.y + vertex_length <= map_length[1]:
            future_up_node = Node(node.x, node.y + vertex_length)
            graph.append_node(future_up_node)
            Helper.map_out_graph(future_up_node, map_width, map_length, vertex_length, graph)
        return graph

    @classmethod
    def ccw(cls, A, B, C):
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    # Return true if line segments AB and CD intersect
    @classmethod
    def intersect(cls, A, B, C, D):
        return cls.ccw(A, C, D) != cls.ccw(B, C, D) and cls.ccw(A, B, C) != cls.ccw(A, B, D)


class Graph:
    def __init__(self):
        self.nodes = []

    def append_node(self, new_node):
        self.nodes.append(new_node)


if __name__ == "__main__":

    from mapper import Wad
    import sys
    wad = Wad("./Doom1.WAD")
    level_1 = wad.levels[0]

    lines = []

    for line in level_1.lines:
        lines.append(Line(level_1.vertices[line.a], level_1.vertices[line.b]))
        # print lines[-1]

    lines_x = []
    lines_y = []
    for line in lines:
        lines_x.extend([line.a.x, line.b.x])
        lines_y.extend([line.a.y, line.b.y])

    MAP_WIDTH = ((min(lines_x)), max(lines_x))
    MAP_LENGTH = ((min(lines_y)), max(lines_y))

    helper = Helper()
    start_pos = [1056, 3616]
    vertex_length = 1000
    player = Player(*start_pos)
    init_node = Node(player.x, player.y)

    sys.setrecursionlimit(15000)

    graph = Graph()
    print helper.map_out_graph(init_node, MAP_WIDTH, MAP_LENGTH, vertex_length, graph)
