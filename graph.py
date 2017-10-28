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

    def __init__(self, a, b, one_sided):
        self.a = self.Point(*a)
        self.b = self.Point(*b)
        self.one_sided = one_sided

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
            if Helper.do_intersect((vertex.start_node.x, vertex.start_node.y), (vertex.end_node.x, vertex.end_node.y), (line.a.x, line.a.y), (line.b.x, line.b.y)):
                vertex.end_node.reachable = False
                return False
        vertex.end_node.reachable = True
        return True

    @staticmethod
    def map_out_graph(node, lines, vertex_length, graph, came_from):

        candidate_to_the_north = Node(node.x, node.y + vertex_length)
        candidate_to_the_west = Node(node.x - vertex_length, node.y)
        candidate_to_the_east = Node(node.x + vertex_length, node.y)
        candidate_to_the_south = Node(node.x, node.y - vertex_length)

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_north), lines) and came_from is not Directions.NORTH:
            if not graph.is_mapped(candidate_to_the_north):
                graph.append_node(candidate_to_the_north)
                print "Appended upwards " + candidate_to_the_north.__str__()
                Helper.map_out_graph(candidate_to_the_north, lines, vertex_length, graph, Directions.SOUTH)
            else:
                print "Node already mapped " + candidate_to_the_north.__str__()

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_west), lines) and came_from is not Directions.WEST:
            if not graph.is_mapped(candidate_to_the_west):
                graph.append_node(candidate_to_the_west)
                print "Appended to the left " + candidate_to_the_west.__str__()
                Helper.map_out_graph(candidate_to_the_west, lines, vertex_length, graph, Directions.EAST)
            else:
                print "Node already mapped " + candidate_to_the_west.__str__()

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_east), lines) and came_from is not Directions.EAST:
            if not graph.is_mapped(candidate_to_the_east):
                graph.append_node(candidate_to_the_east)
                print "Appended to the right " + candidate_to_the_east.__str__()
                Helper.map_out_graph(candidate_to_the_east, lines, vertex_length, graph, Directions.WEST)
            else:
                print "Node already mapped " + candidate_to_the_east.__str__()

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_south), lines) and came_from is not Directions.SOUTH:
            if not graph.is_mapped(candidate_to_the_south):
                graph.append_node(candidate_to_the_south)
                print "Appended downwards " + candidate_to_the_south.__str__()
                Helper.map_out_graph(candidate_to_the_south, lines, vertex_length, graph, Directions.NORTH)
            else:
                print "Node already mapped " + candidate_to_the_south.__str__()

        return graph

    @classmethod
    def ccw(cls, A, B, C):
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    # Return true if line segments AB and CD intersect
    @classmethod
    def intersect(cls, A, B, C, D):
        return cls.ccw(A, C, D) != cls.ccw(B, C, D) and cls.ccw(A, B, C) != cls.ccw(A, B, D)

    @classmethod
    def on_segment(p, q, r):
        onSegment = False
        if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
            onSegment = True
        return onSegment

    @classmethod
    def orientation(p, q, r):
        orientation = -1
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            orientation = 0 # co-linear
        if val > 0:
            orientation = 1 # clockwise
        if val < 0:
            orientation = 2 # counter clockwise
        return orientation

    @classmethod
    def do_intersect(p1, q1, p2, q2):
        do_intersect = False

        o1 = Helper.orientation(p1, q1, p2)
        o2 = Helper.orientation(p1, q1, q2)
        o3 = Helper.orientation(p2, q2, p1)
        o4 = Helper.orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            do_intersect = True # general case

        if o1 == 0 and Helper.on_segment(p1, p2, q1):
            do_intersect = True

        if o2 == 0 and Helper.on_segment(p1, q2, q1):
            do_intersect = True

        if o3 == 0 and Helper.on_segment(p2, p1, q2):
            do_intersect = True

        if o4 == 0 and Helper.on_segment(p2, p1, q2):
            do_intersect = True

        return do_intersect



class Graph:
    def __init__(self):
        self.nodes = []

    def append_node(self, new_node):
        self.nodes.append(new_node)

    def is_mapped(self, candidate_node):
        is_mapped = False
        for node in self.nodes:
            if node.x == candidate_node.x and node.y == candidate_node.y:
                is_mapped = True
                break
        return is_mapped


def enum(**enums):
    return type('Enum', (), enums)


if __name__ == "__main__":

    from mapper import Wad
    import sys

    wad = Wad("./Doom1.WAD")
    level_1 = wad.levels[0]

    lines = []

    Directions = enum(NORTH=0, WEST=1, EAST=2, SOUTH=3)

    for line in level_1.lines:
        lines.append(Line(level_1.vertices[line.a], level_1.vertices[line.b], line.is_one_sided))
        # print lines[-1]

    lines_x = []
    lines_y = []
    for line in lines:
        lines_x.extend([line.a.x, line.b.x])
        lines_y.extend([line.a.y, line.b.y])

    MAP_WIDTH = ((min(lines_x)), max(lines_x))
    MAP_HEIGHT = ((min(lines_y)), max(lines_y))

    helper = Helper()
    start_pos = [1056, 3616]
    vertex_length = 400
    player = Player(*start_pos)
    init_node = Node(player.x, player.y)

    sys.setrecursionlimit(15000)

    graph = Graph()
    graph.append_node(init_node)
    # print helper.map_out_graph(init_node, lines, vertex_length, graph, Directions.SOUTH)

    # line_1 = Line([0, 0], [5, 5], True)
    node_1 = Node(init_node.x, init_node.y + vertex_length)
    node_2 = Node(init_node.x, init_node.y + vertex_length)
    # node_3 = Node(5, 3)
    # node_4 = Node(6, 4)
    # node_5 = Node(5, 6)
    # node_6 = Node(7, 5)
    # node_7 = Node(5, 7)

    print Helper.is_node_reachable(Vertex(init_node, node_1), lines)

    print len(lines)
