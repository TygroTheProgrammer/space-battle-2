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
    game_map: list;
    game_units: dict;
    resources: list;

    def __init__(self):
        self.game_units = dict(); # set of unique unit ids
        self.game_map = list();
        self.directions = ['N', 'S', 'E', 'W']
        self.init = False;
        self.resources = dict();
        self.units = set();

    def analyze(self, json_data):
        # Probably not the best, way, but ehh
        if not self.init:
            if "game_info" in json_data:
                self.info = json_data['game_info'];
                self.init = True;
                self.game_map = [[None for i in range(2*self.info['map_height'])] for j in range(2*self.info['map_width'])]

        # Main logic loop
        units = json_data['unit_updates']; 
        self.update_units(units);
        # Tile update
        tiles = json_data['tile_updates'];
        self.update_map(tiles);

        # Logic
        self.do_work();
        
        rand_command = self.get_random_move(json_data);
        response = json.dumps(command, separators=(',',':')) + '\n'
        return response;

    def update_map(self, json_tile_data):
        for tile in json_tile_data:
            self.game_map[tile['x']][tile['y']] = tile;
            if 'resources' in tile and tile['resources']:
                self.add_resource(tile['resources']);

    def add_resource(self, resource):
        if not resource['id'] in self.resources:
            self.resources[resource['id']] = resource;
        print(json.dumps(resource, indent=4, sort_keys=True))

    def update_units(self, json_unit_data):
        for unit in json_unit_data:
            if not unit['id'] in self.game_units:
                unit['task'] = 'search';
            self.game_units[unit['id']] = unit;

    def get_random_move(self, json_data):
        unit_id = random.choice(tuple(self.game_units.keys()));
        direction = random.choice(self.directions)
        move = 'MOVE'
        command = {"commands": [{"command": move, "unit": unit_id, "dir": direction}]}
        return command;

if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090
    host = '0.0.0.0';
    # host = '127.0.0.1'

    server = ss.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()
