from aima.search import UndirectedGraph, GraphProblem, astar_search
from graph import Node


class StateSpace(object):
    """ This is a datatype used to collect a number of important aspects of the environment
    It can be build online or be created offline using the Helper Agent

    You are welcome to modify or change it as you see fit

    """

    def __init__(self):
        """ Constructor for the local state-space representation derived from the Orcale"""
        self.state_locations = None
        self.state_actions = None
        self.start_id = None  # The id assigned to the start state
        self.goal_id = None  # The id assigned to the goal state
        self.start_loc = None  # The real word coordinates of the start state
        self.goal_loc = None  # The real word coordinates of the goal state
        self.reward_states_n = None
        self.reward_states = None
        self.reward_sendcommand = None
        self.reward_timeout = None
        self.timeout = None


class Agent:
    def __init__(self):
        self.state_space = StateSpace()

    def get_state_space(self, all_nodes, init_node, goal_node, vertex_length):
        state_space_locations = {}  # create a dict

        for node in all_nodes:
            state_id = node.__str__()
            state_space_locations[state_id] = (node.x, node.y)

            # -- Generate state / action list --#
        # First define the set of actions in the defined coordinate system
        actions = {"left": [-vertex_length, 0], "up": [0, vertex_length], "right": [vertex_length, 0]}
        state_space_actions = {}

        for state_id in state_space_locations:
            possible_states = {}
            for action in actions:
                delta = actions.get(action)
                state_loc = state_space_locations.get(state_id)
                state_loc_post_action = [state_loc[0] + delta[0], state_loc[1] + delta[1]]
                state_id_post_action = Node(str(state_loc_post_action[0]), str(state_loc_post_action[1])).__str__()
                if state_space_locations.get(state_id_post_action) != None:
                    possible_states[state_id_post_action] = 1
            state_space_actions[state_id] = possible_states

        # -- Save the info an instance of the StateSpace class --
        self.state_space.state_actions = state_space_actions
        self.state_space.state_locations = state_space_locations
        self.state_space.start_id = init_node.__str__()
        self.state_space.start_loc = state_space_locations[self.state_space.start_id]
        self.state_space.goal_id = goal_node.__str__()
        self.state_space.goal_loc = state_space_locations[self.state_space.goal_id]

    def find_solution_path(self):
        maze_map = UndirectedGraph(self.state_space.state_actions)
        maze_map_locations = self.state_space.state_locations
        start_location = maze_map_locations.keys()[maze_map_locations.values().index(self.state_space.start_loc)]
        goal_location = maze_map_locations.keys()[maze_map_locations.values().index(self.state_space.goal_loc)]

        maze_problem = GraphProblem(start_location, goal_location, maze_map)

        goal_node = astar_search(problem=maze_problem, h=None)

        solution_path = [goal_node]
        parent_node = goal_node.parent
        solution_path.append(parent_node)

        # Creates the list with actions to be taken
        while parent_node.state != start_location:
            parent_node = parent_node.parent
            solution_path.append(parent_node)

        return solution_path, start_location, goal_location, maze_map_locations


if __name__ == "__main__":
    agent = Agent()
    init = Node(1, 1)
    goal = Node(4, 7)
    # all_nodes = [init, Node(1, 2), Node(1, 3), Node(2, 1), Node(2, 2), Node(2, 3), Node(3, 3), Node(3, 4), Node(2, 4),
    #              Node(2, 5), Node(2, 6), Node(2, 7), Node(1, 7), Node(3, 7), Node(4, 7), Node(4, 6), Node(4, 5),
    #              Node(4, 4), goal]


    agent.get_state_space(all_nodes, init, goal, 1)
    (solution_path, start_location, goal_location, maze_map_locations) = agent.find_solution_path()
    print solution_path
