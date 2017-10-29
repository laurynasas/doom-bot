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
        self.is_door = None

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
    def line_is_in_doors(line, door_lines, level_data):
        their_line_in_our = Line([level_data.vertices[line.a][0], level_data.vertices[line.a][1]],
                                 [level_data.vertices[line.b][0], level_data.vertices[line.b][1]], False)
        for our_line in door_lines:
            if their_line_in_our.a.x == our_line.a.x and their_line_in_our.a.y == our_line.a.y and their_line_in_our.b.x == our_line.b.x and their_line_in_our.b.y == our_line.b.y:
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

def get_distance_between_nodes(a,b):
    return math.hypot(a.x - b.x, a.y - b.y)

def enum(**enums):
    return type('Enum', (), enums)


if __name__ == "__main__":

    from mapper import Wad
    from seearch_the_graph import Agent
    from dumb_hunter import get_doors,movePlayerDir
    import math
    import time

    RESTFUL_HOST = "localhost"
    RESTFUL_PORT = 6666
    from dumb_hunter import movePlayer, get_position, spin_amount, get_doors

    wad = Wad("./Doom1.WAD")
    level_1 = wad.levels[0]
    dime = level_1.lower_left, level_1.upper_right

    lines = []

    Directions = enum(NORTH=0, WEST=1, EAST=2, SOUTH=3)
    import json

    door_lines = []
    all_door_coord = get_doors()
    for door_info in json.loads(all_door_coord):
        door_line = door_info["line"]
        line_points = []

        for point in door_line:
            point_obj = door_line[point]
            x = point_obj[u'x']
            y = point_obj[u'y']
            line_points.append([x, y])
        door_lines.append(Line(line_points[0], line_points[1], False))
    helper = Helper()

    goal_line = None

    print door_lines
    for line in level_1.lines:
        # if line.is_one_sided() or line.block_players_and_monsters:
        #     grey_black_line = Line(level_1.vertices[line.a], level_1.vertices[line.b], True)
        #     grey_black_line.is_door = False
        #     lines.append(grey_black_line)
        #
        if line.exit:
            goal_line = Line(level_1.vertices[line.a], level_1.vertices[line.b], True)
        if not line.block_players_and_monsters:
            boundary_line = Line(level_1.vertices[line.a], level_1.vertices[line.b], True)
            lines.append(boundary_line)
        if not line.block_monsters:
            boundary_line = Line(level_1.vertices[line.a], level_1.vertices[line.b], True)
            lines.append(boundary_line)

    lines_x = []
    lines_y = []
    for line in lines:
        lines_x.extend([line.a.x, line.b.x])
        lines_y.extend([line.a.y, line.b.y])

    start_pos = [1056, -3616]
    vertex_length = 70
    player = Player(*start_pos)
    init_node = Node(player.x, player.y)
    goal_node = Node(goal_line.a.x, goal_line.a.y)


    graph = Graph()
    graph.append_node(init_node)
    my_lines, all_nodes, all_vertices = helper.map_out_graph(init_node, lines, vertex_length, graph, Directions.SOUTH)
    agent = Agent()
    # all_nodes.append(goal_node)
    closest_node = all_nodes[0]
    min = get_distance_between_nodes(all_nodes[0], goal_node)

    # print '------------------------------------', min
    for node in all_nodes[1:]:
        if get_distance_between_nodes(node, goal_node) <= min:
            closest_node = node
            min = get_distance_between_nodes(node, goal_node)


    agent.get_state_space(all_nodes, all_nodes[0], closest_node, vertex_length,
                          lines)
    (solution_path, start_location, goal_location, maze_map_locations) = agent.find_solution_path()
    print solution_path

    solution_coords = [(int(el.state.split(" | ")[0]), int(el.state.split(" | ")[1])) for el in solution_path]

    solution_path = [Node(int(el.state.split(" | ")[0]), int(el.state.split(" | ")[1])) for el in solution_path]
    #
    write_to = open("solution_path.txt", 'w')

    with write_to:
        for node in solution_path:
            write_to.write(str(node) + "\n")

    level_1.save_svg(my_lines, my_path=solution_path, our_lines=lines)
    #
    #
    #

    init_postion = get_position()
    print init_postion
    # solution_coords = []
    # input = open("solution_path.txt", 'r')
    # with input:
    #     for line in input.readlines():
    #         solution_coords.append((float(line.split(" | ")[0]), float(line.split(" | ")[1])))









    #
    solution_coords.reverse()
    # solution_coords = [(el[0], el[1]) for el in solution_coords]
    current_cord = solution_coords[0]
    radius = 20
    for index, next_coord in enumerate(solution_coords[1:]):
        print "I was here:", current_cord, " and will be going to: ", next_coord
        position = get_position()

        # if index == 4:
        # print "Have turned"
        spin_amount(position, next_coord)

        # all_door_coord = get_doors()
        # for door_info in all_door_coord:
        #     door_line = door_info["line"]
        #     for point in door_line:
        #         point_obj = door_line[point]
        #         line_points = []
        #         for coord in point_obj:
        #             x = coord['x']
        #             y = coord['y']
        #             line_points.append(Line.Point(x, y))
        #     door_lines.append(Line(line_points[0], line_points[1], False))
        # print door_lines

        # time.sleep(2)
        previous_position = position
        counter = 0
        while math.hypot(next_coord[0] - position[0], next_coord[1] - position[1]) > float(radius):
            movePlayer(2)
            time.sleep(0.3)
            print "Distance to point", math.hypot(next_coord[0] - position[0], next_coord[1] - position[1])
            # time.sleep(1)
            position = get_position()
            print "my position:", position

            if abs(math.sqrt( (previous_position[0] - position[0])**2 + (previous_position[1] - position[1])**2)) <1 :
                counter +=1
                if counter >3:
                    movePlayerDir(10,"strafe-right")
                    counter = 0
            previous_position = position
        print "Got to a point"

        current_cord = next_coord











        # current_cord = next_coord
        # url = 'http://{}:{}/api/player/actions'.format(RESTFUL_HOST, RESTFUL_PORT)
        # payload = {"type": "forward", "amount": 100}
        # logging.warn('Calling {} with payload {}'.format(url, payload))
        # response = requests.post(url)
        # response.status_code
