from player import Player
from world import World
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# traversal_path = ['n', 'n']

# map_file = "maps/test_cross.txt"
# traversal_path = ['n', 'n', 's', 's', 's', 's', 'n', 'n', 'e', 'e', 'w', 'w', 'w', 'w']

# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = []


def build_traversal_path(user: Player):
    # Dictionary of room_id, and exits for that room
    visited = {user.current_room.id: user.current_room.get_exits()}

    # Dictionary of reverse directions
    reverse_direction = {'s': 'n', 'n': 's', 'w': 'e', 'e': 'w'}

    # Temporary holder for building our traversal_path
    travel_path = []

    path_back_to_room_with_unvisited_directions = []

    # While all rooms have not been visited yet
    while len(visited) < len(room_graph) - 1:

        # If the current room_id hasn't been visited
        if user.current_room.id not in visited:

            # Add it to visited with it's available exits
            visited[user.current_room.id] = user.current_room.get_exits()

            # Remove the previous room from visited so we "mark our spot"
            visited[user.current_room.id].remove(path_back_to_room_with_unvisited_directions[-1])

        # While the current room has less than 1 exit available
        while len(visited[user.current_room.id]) < 1:
            # Go backwards, adding to our travel path and updating out user object
            previous_direction = path_back_to_room_with_unvisited_directions.pop()
            travel_path.append(previous_direction)
            user.travel(previous_direction)

        # Get the next move from exits in our visited dictionary
        next_move = visited[user.current_room.id].pop(0)

        # Add next move to travel_path and the path back to room with unvisited directions
        travel_path.append(next_move)
        path_back_to_room_with_unvisited_directions.append(reverse_direction[next_move])

        # Update user object
        user.travel(next_move)

    # Celebrate ;-P
    return travel_path


traversal_path = build_traversal_path(player)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
