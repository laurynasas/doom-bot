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
    def does_vertex_exist(all_vertices, start_coord, end_coord):
        for vertex in all_vertices:
            vector_1 = [abs(start_coord[0] - end_coord[0]), abs(start_coord[1] - end_coord[1])]
            vector_2 = [abs(vertex.start_node.x - vertex.end_node.x), abs(vertex.start_node.y - vertex.end_node.y)]
            if (vector_1[0] - vector_2[0] == 0) and (vector_1[1] - vector_2[1] == 0):
                print "exists"
                return True
        return False

    @staticmethod
    def map_out_graph(node, lines, vertex_length, graph, came_from, my_lines=[], all_nodes=[],
                      all_vertices=[]):
        all_nodes.append(node)
        candidate_to_the_north = Node(node.x, node.y + vertex_length)
        candidate_to_the_west = Node(node.x - vertex_length, node.y)
        candidate_to_the_east = Node(node.x + vertex_length, node.y)
        candidate_to_the_south = Node(node.x, node.y - vertex_length)

        if Helper.is_node_reachable(Vertex(node, candidate_to_the_north), lines) and came_from is not Directions.NORTH:
            all_vertices.append(Vertex(node, candidate_to_the_north))
            if not graph.is_mapped(candidate_to_the_north):
                my_lines.append([[node.x, node.y], [candidate_to_the_north.x, candidate_to_the_north.y]])
                graph.append_node(candidate_to_the_north)
                print "Appended upwards " + candidate_to_the_north.__str__()

                Helper.map_out_graph(candidate_to_the_north, lines, vertex_length, graph, Directions.SOUTH,
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

    lines_x = []
    lines_y = []
    for line in lines:
        lines_x.extend([line.a.x, line.b.x])
        lines_y.extend([line.a.y, line.b.y])

    helper = Helper()
    start_pos = [1056, -3616]
    vertex_length = 70
    player = Player(*start_pos)
    init_node = Node(player.x, player.y)

    graph = Graph()
    graph.append_node(init_node)
    my_lines, all_nodes, all_vertices = helper.map_out_graph(init_node, lines, vertex_length, graph, Directions.SOUTH)
    agent = Agent()
    agent.get_state_space(all_nodes, all_nodes[0], all_nodes[(len(all_nodes) / 2) + 250], vertex_length,
                          lines)
    (solution_path, start_location, goal_location, maze_map_locations) = agent.find_solution_path()
    print solution_path

    solution_path = [Node(int(el.state.split(" | ")[0]), int(el.state.split(" | ")[1])) for el in solution_path]

    write_to = open("solution_path.txt", 'w')

    with write_to:
        for node in solution_path:
            write_to.write(str(node) + "\n")

    level_1.save_svg(my_lines, my_path=solution_path)
