import logging

import requests

RESTFUL_HOST = "localhost"
RESTFUL_PORT = 6666

if __name__ == "__main__":
    url = 'http://{}:{}/api/player'.format(RESTFUL_HOST, RESTFUL_PORT)
    payload = {}
    logging.warn('Calling {} with payload {}'.format(url, payload))
    response = requests.get(url)
    response.status_code

