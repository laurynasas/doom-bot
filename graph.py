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
            if Helper.do_intersect((vertex.start_node.x, vertex.start_node.y), (vertex.end_node.x, vertex.end_node.y),
                                   (line.a.x, line.a.y), (line.b.x, line.b.y)):
                vertex.end_node.reachable = False
                return False
        vertex.end_node.reachable = True
        return True

    @staticmethod
    def map_out_graph(node, lines, vertex_length, graph, came_from, counter=0, my_lines=[], all_nodes=[], all_vertices =[]):
        all_nodes.append(node)
        candidate_to_the_north = Node(node.x, node.y + vertex_length)
        candidate_to_the_west = Node(node.x - vertex_length, node.y)
        candidate_to_the_east = Node(node.x + vertex_length, node.y)
        candidate_to_the_south = Node(node.x, node.y - vertex_length)
        counter += 1
        # if counter > 15:
        #     print "will return"
        #     return my_lines

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_north), lines) and came_from is not Directions.NORTH:
            all_vertices.append(Vertex(node, candidate_to_the_north))
            if not graph.is_mapped(candidate_to_the_north):
                my_lines.append([[node.x, node.y], [candidate_to_the_north.x, candidate_to_the_north.y]])
                graph.append_node(candidate_to_the_north)
                print "Appended upwards " + candidate_to_the_north.__str__()

                Helper.map_out_graph(candidate_to_the_north, lines, vertex_length, graph, Directions.SOUTH, counter,
                                     my_lines=my_lines, all_nodes=all_nodes)
            else:
                print "Node already mapped " + candidate_to_the_north.__str__()

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_west), lines) and came_from is not Directions.WEST:
            all_vertices.append(Vertex(node, candidate_to_the_west))
            if not graph.is_mapped(candidate_to_the_west):
                my_lines.append([[node.x, node.y], [candidate_to_the_west.x, candidate_to_the_west.y]])
                graph.append_node(candidate_to_the_west)
                print "Appended to the left " + candidate_to_the_west.__str__()
                Helper.map_out_graph(candidate_to_the_west, lines, vertex_length, graph, Directions.EAST,
                                     all_nodes=all_nodes)
            else:
                print "Node already mapped " + candidate_to_the_west.__str__()

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_east), lines) and came_from is not Directions.EAST:
            all_vertices.append(Vertex(node, candidate_to_the_east))
            if not graph.is_mapped(candidate_to_the_east):
                my_lines.append([[node.x, node.y], [candidate_to_the_east.x, candidate_to_the_east.y]])

                graph.append_node(candidate_to_the_east)
                print "Appended to the right " + candidate_to_the_east.__str__()
                Helper.map_out_graph(candidate_to_the_east, lines, vertex_length, graph, Directions.WEST,
                                     all_nodes=all_nodes)
            else:
                print "Node already mapped " + candidate_to_the_east.__str__()

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_south), lines) and came_from is not Directions.SOUTH:
            all_vertices.append(Vertex(node, candidate_to_the_south))

            if not graph.is_mapped(candidate_to_the_south):
                my_lines.append([[node.x, node.y], [candidate_to_the_south.x, candidate_to_the_south.y]])
                graph.append_node(candidate_to_the_south)
                print "Appended downwards " + candidate_to_the_south.__str__()
                Helper.map_out_graph(candidate_to_the_south, lines, vertex_length, graph, Directions.NORTH,
                                     all_nodes=all_nodes)
            else:
                print "Node already mapped " + candidate_to_the_south.__str__()

        return my_lines, all_nodes, all_vertices

    @classmethod
    def ccw(cls, A, B, C):
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    # Return true if line segments AB and CD intersect
    @classmethod
    def intersect(cls, A, B, C, D):
        return cls.ccw(A, C, D) != cls.ccw(B, C, D) and cls.ccw(A, B, C) != cls.ccw(A, B, D)

    @classmethod
    def on_segment(cls, p, q, r):
        onSegment = False
        if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
            onSegment = True
        return onSegment

    @classmethod
    def orientation(cls, p, q, r):
        orientation = -1
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            orientation = 0  # co-linear
        if val > 0:
            orientation = 1  # clockwise
        if val < 0:
            orientation = 2  # counter clockwise
        return orientation

    @classmethod
    def do_intersect(cls, p1, q1, p2, q2):
        do_intersect = False

        o1 = Helper.orientation(p1, q1, p2)
        o2 = Helper.orientation(p1, q1, q2)
        o3 = Helper.orientation(p2, q2, p1)
        o4 = Helper.orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            do_intersect = True  # general case

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
    from seearch_the_graph import Agent

    wad = Wad("./Doom1.WAD")
    level_1 = wad.levels[0]
    dime = level_1.lower_left, level_1.upper_right

    lines = []

    Directions = enum(NORTH=0, WEST=1, EAST=2, SOUTH=3)

    for line in level_1.lines:
        if line.is_one_sided():
            lines.append(Line(level_1.vertices[line.a], level_1.vertices[line.b], True))

            # print lines[-1]

    lines_x = []
    lines_y = []
    for line in lines:
        lines_x.extend([line.a.x, line.b.x])
        lines_y.extend([line.a.y, line.b.y])

    MAP_WIDTH = ((min(lines_x)), max(lines_x))
    MAP_HEIGHT = ((min(lines_y)), max(lines_y))
    # print MAP_HEIGHT, MAP_WIDTH
    helper = Helper()
    start_pos = [1056, -3516]
    vertex_length = 70
    player = Player(*start_pos)
    init_node = Node(player.x, player.y)

    graph = Graph()
    graph.append_node(init_node)
    my_lines, all_nodes, all_vertices = helper.map_out_graph(init_node, lines, vertex_length, graph, Directions.SOUTH)
    print all_nodes
    agent = Agent()
    # init = Node(1, 1)
    # goal = Node(4, 7)
    # # all_nodes = [init, Node(1, 2), Node(1, 3), Node(2, 1), Node(2, 2), Node(2, 3), Node(3, 3), Node(3, 4), Node(2, 4),
    # #              Node(2, 5), Node(2, 6), Node(2, 7), Node(1, 7), Node(3, 7), Node(4, 7), Node(4, 6), Node(4, 5),
    # #              Node(4, 4), goal]
    #
    #
    agent.get_state_space(all_nodes, all_nodes[0], all_nodes[(len(all_nodes)/2)+250], vertex_length)
    (solution_path, start_location, goal_location, maze_map_locations) = agent.find_solution_path()
    print solution_path

    solution_path = [Node(int(el.state.split(" | ")[0]), int(el.state.split(" | ")[1])) for el in solution_path]
    level_1.save_svg(my_lines, my_path=solution_path)
    # line_1 = Line([0, 0], [5, 5], True)
    node_1 = Node(init_node.x, init_node.y + vertex_length)
    node_2 = Node(init_node.x, init_node.y + vertex_length)
    # node_3 = Node(5, 3)
    # node_4 = Node(6, 4)
    # node_5 = Node(5, 6)
    # node_6 = Node(7, 5)
    # node_7 = Node(5, 7)

    # print Helper.is_node_reachable(Vertex(init_node, node_1), lines)

    # print len(lines)
