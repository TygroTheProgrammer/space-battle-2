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
    def __init__(self):
        self.game_units = dict(); # set of unique unit ids
        self.game_map = list();
        self.directions = ['N', 'S', 'E', 'W']
        self.init = False;
        self.resources = dict();
        self.units = set();
        self.units_path = dict();

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
        self.assign_work();
        
        commands = [];
        for unit_id in self.game_units:
            direction = random.choice(self.directions)
            command = "MOVE";

            # If path, follow path
            if unit_id in self.units_path:
                # TODO override direction to follow path
                # if at end of path, mine instead
                # if nothing to mine, set path back to base
                # if at base, remove path

            commands.append({"command": move, "unit": unit_id, "dir": direction}]);

        response = json.dumps(commands, separators=(',',':')) + '\n'
        return response;

    def assign_work(self):
        # Nasty indentation here
        for resource in self.resources:
            # Check if each resource is open
            if resource['prio'] == 'open':
                # Find worker
                for unit_id in self.game_units:
                    if not unit_id in self.units_path:
                        # TODO assign path to worker
                        resource['prio'] == 'closed';
                        break;

    def update_map(self, json_tile_data):
        for tile in json_tile_data:
            self.game_map[tile['x']][tile['y']] = tile;
            if 'resources' in tile and tile['resources']:
                self.add_resource(tile['resources']);

    def add_resource(self, resource):
        if not resource['id'] in self.resources:
            self.resources[resource['id']] = resource;
            self.resources[resource['id']]['prio'] = 'open'; 
            print(json.dumps(resource, indent=4, sort_keys=True))

    def update_units(self, json_unit_data):
        for unit in json_unit_data:
            if not unit['id'] in self.game_units;
                self.units_path[unit['id'] = None;
            self.game_units[unit['id']] = unit;

    def get_random_move(self, json_data):
        unit_id = random.choice(tuple(self.game_units.keys()));
        direction = random.choice(self.directions)
        move = 'MOVE'
        command = {"commands": [{"command": move, "unit": unit_id, "dir": direction}]}
        return command;

<<<<<<< Updated upstream
=======
    def move_to(self, json_data, u, to_x, to_y):
        grid = Grid(self.game_map); #TODO Assign numeric values to obstacles
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never);
        
        start = grid.node(u['x'], u['y']);
        end = grid.node(to_x, to_y);

        path, _ = finder.find_path(start, end, grid);
        
        # Translate path into commands
        commands = []
        for i in range(1, len(path)):
            dx = path[i][0] - path[i-1][0]
            dy = path[i][1] - path[i-1][1]
            if dx > 0:
                commands.append("E")
            elif dx < 0:
                commands.append("W")
            elif dy > 0:
                commands.append("S")
            elif dy < 0:
                commands.append("N")
    

        return commands

        
        
        







>>>>>>> Stashed changes
if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090
    host = '0.0.0.0';
    # host = '127.0.0.1'

    server = ss.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()
