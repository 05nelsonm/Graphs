import random
import time
import sys
sys.path.append('../graph')
from util import Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            # print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        # Write a for loop that calls create user the right amount of times
        for i in range(num_users):
            self.add_user(f"User {i + 1}")

        # Create friendships
        # To create N random friendships, you could create a list with all
        #  possible friendship combinations, shuffle the list, then grab the
        #  first N elements from the list.
        possible_friendships = []
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        # Create N friendships where N = avg_friendships * num_users // 2
        # avg_friendships = total_friendships / num_users
        # total_friendships = avg_friendships * num_users
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def populate_graph_linear(self, num_users, avg_friendships):
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        # Write a for loop that calls create user the right amount of times
        for i in range(num_users):
            self.add_user(f"User {i+1}")

        target_friendships = num_users * avg_friendships
        total_friendships = 0
        collisions = 0
        while total_friendships < target_friendships:
            # Pick a random user
            user_id = random.randint(1, num_users)
            # Pick another random user
            friend_id = random.randint(1, num_users)
            # Try to create the friendship
            if self.add_friendship(user_id, friend_id):
                # If it works, increment a counter
                total_friendships += 2
            else:
                # If not, try again
                collisions += 1
        print(f"NUM COLLISIONS: {collisions}")

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME

        # QUEUE
        # Create a queue
        q = Queue()
        # Enqueue A PATH TO the starting vertex
        q.enqueue([user_id])
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            path = q.dequeue()
            # GRAB THE LAST ID FROM THE END OF THE PATH
            last_id = path[-1]
            # Check if it's been visited
            # If it hasn't been visited...
            if last_id not in visited:
                # Mark it as visited
                visited[last_id] = path
                # Enqueue all it's neighbors to back of the queue
                for friend_id in self.friendships[last_id]:
                    # MAKE A COPY OF THE PATH
                    copy = path.copy()
                    # ADD NEIGHBOR TO BACK OF PATH
                    copy.append(friend_id)
                    # ENQUEUE THE COPY
                    q.enqueue(copy)
        return visited


# 1. To create 100 users with an average of 10 friends each, how many
#    times would you need to call `add_friendship()`? Why?
#
#        A: 100 * 10 // 2 = 500

# 2. If you create 1000 users with an average of 5 random friends
#    each, what percentage of other users will be in a particular
#    user's extended social network?
#
#        A:     Running a test of:
#               sg = SocialGraph()
#               sg.populate_graph(1000, 5)
#               connections = sg.get_all_social_paths(1)
#               print(len(connections) / 1000)
#
#               Answer = 0.99
#
#    What is the average degree of separation between a user and
#    those in his/her extended network?
#
#        A:     Running a test of:
#               sg = SocialGraph()
#               sg.populate_graph(1000, 5)
#               connections = sg.get_all_social_paths(1)
#               print(len(connections) / 1000)
#               total = 0
#               for path in connections.values():
#                   total += len(path)
#               print(f"Avg degrees of separation = {total / len(connections) - 1}")
#
#               Answer = ~4.5

# 3. You might have found the results from question #2 above to be
#    surprising. Would you expect results like this in real life?
#
#        A: No.
#
#    If not, what are some ways you could improve your friendship
#    distribution model for more realistic results?
#
#        A: Use a Voronoi algorithm that accounts for clustering.

# 4. If you followed the hints for part 1, your `populate_graph()` will
#    run in O(n^2) time. Refactor your code to run in O(n) time. Are
#    there any tradeoffs that come with this implementation?
#
#        A: After a certain density, Linear Populate takes much longer
#           to populate because of collisions.


if __name__ == '__main__':
    # sg = SocialGraph()
    # sg.populate_graph(10, 2)
    # print(sg.friendships)
    # connections = sg.get_all_social_paths(1)
    # print(connections)

    num_users = 2000
    avg_friendships = 400
    sg = SocialGraph()
    start_time = time.time()
    sg.populate_graph(num_users, avg_friendships)
    end_time = time.time()
    print("\n\n-----")
    print(f"Quadratic populate: {end_time - start_time} seconds")
    print("-----\n\n")

    sg = SocialGraph()
    start_time = time.time()
    sg.populate_graph_linear(num_users, avg_friendships)
    end_time = time.time()
    print(f"Linear populate: {end_time - start_time} seconds")
