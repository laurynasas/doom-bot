import math
import time

RESTFUL_HOST = "localhost"
RESTFUL_PORT = 6666
from dumb_hunter import movePlayer, get_position, spin_amount, spinPlayer, get_doors
from graph import Line

if __name__ == "__main__":

    init_postion = get_position()
    print init_postion
    solution_coords = []
    input = open("solution_path.txt", 'r')
    with input:
        for line in input.readlines():
            solution_coords.append((float(line.split(" | ")[0]), float(line.split(" | ")[1])))
    solution_coords.reverse()
    # solution_coords = [(el[0], el[1]) for el in solution_coords]
    current_cord = solution_coords[0]
    radius = 5
    for index, next_coord in enumerate(solution_coords[1:]):
        print "I was here:", current_cord, " and will be going to: ", next_coord
        position = get_position()

        # if index == 4:
        # print "Have turned"
        spin_amount(position, next_coord)

        door_lines = []
        all_door_coord = get_doors()
        for door_info in all_door_coord:
            door_line = door_info["line"]
            for point in door_line:
                point_obj = door_line[point]
                line_points = []
                for coord in point_obj:
                    x = coord['x']
                    y = coord['y']
                    line_points.append(Line.Point(x, y))
            door_lines.append(Line(line_points[0], line_points[1], False))
        print door_lines



        time.sleep(2)

        while math.hypot(next_coord[0] - position[0], next_coord[1] - position[1]) > float(radius):
            movePlayer(2)
            print "Distance to point", math.hypot(next_coord[0] - position[0], next_coord[1] - position[1])
            time.sleep(1)
            position = get_position()
            print "my position:", position
        print "Got to a point"

        current_cord = next_coord


        # current_cord = next_coord
        # url = 'http://{}:{}/api/player/actions'.format(RESTFUL_HOST, RESTFUL_PORT)
        # payload = {"type": "forward", "amount": 100}
        # logging.warn('Calling {} with payload {}'.format(url, payload))
        # response = requests.post(url)
        # response.status_code
