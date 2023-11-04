#!/usr/bin/python

import sys
import json
import random

if (sys.version_info > (3, 0)):
    print("Python 3.X detected")
    import socketserver as ss
else:
    print("Python 2.X detected")
    import SocketServer as ss


class NetworkHandler(ss.StreamRequestHandler):
    def handle(self):
        game = Game()

        while True:
            data = self.rfile.readline().decode() # reads until '\n' encountered
            json_data = json.loads(str(data))
            # uncomment the following line to see pretty-printed data
            # print(json.dumps(json_data, indent=4, sort_keys=True))
            response = game.analyze(json_data)
            if response:
                response = response.encode();
                self.wfile.write(response)


class Game:
    # Notes for vars (for me)
    init: bool;
    info: dict;
    units: dict;

    def __init__(self):
        self.units = set() # set of unique unit ids
        self.directions = ['N', 'S', 'E', 'W']
        self.init = False;

    def analyze(self, json_data):
        # Probably not the best, way, but ehh
        if not self.init:
            if "game_info" in json_data:
                Game.info = json_data['game_info'];
                Game.init = True;
                print(json.dumps(Game.info, indent=4, sort_keys=True))
        else:
            # Main logic loop
            units = json_data['unit_updates']; 
            tiles = json_data['tile_updates'];
            # TODO do stuff with data
            pass;




    def update_map(self, json_data):
        for tile in json_data['tile_updates']:
            self.tile_map[tile['x']][tile['y']] = tile;

    def get_random_move(self, json_data):
        units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        self.units |= units # add any additional ids we encounter
        unit = random.choice(tuple(self.units))
        direction = random.choice(self.directions)
        move = 'MOVE'
        command = {"commands": [{"command": move, "unit": unit, "dir": direction}]}
        response = json.dumps(command, separators=(',',':')) + '\n'
        return response

if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090
    host = '0.0.0.0';
    # host = '127.0.0.1'

    server = ss.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()
