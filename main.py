import logging

import requests

RESTFUL_HOST = "localhost"
RESTFUL_PORT = 6666
from dumb_hunter import movePlayer, get_position


if __name__ == "__main__":

    init_postion = get_position()
    # url = 'http://{}:{}/api/player/actions'.format(RESTFUL_HOST, RESTFUL_PORT)
    # payload = {"type": "forward", "amount": 100}
    # logging.warn('Calling {} with payload {}'.format(url, payload))
    # response = requests.post(url)
    # response.status_code
    movePlayer(2)