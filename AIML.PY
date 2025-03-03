import heapq
import time

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g  # Cost to reach this node
        self.h = h  # Heuristic cost
        self.f = g + h  # Total estimated cost
    
    def __lt__(self, other):
        return self.f < other.f  # Priority queue comparison

# Possible moves
MOVES = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

# Goal State
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def find_position(state, value):
    for i, row in enumerate(state):
        if value in row:
            return i, row.index(value)

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = find_position(GOAL_STATE, state[i][j])
                distance += abs(x - i) + abs(y - j)
    return distance

def misplaced_tiles(state):
    count = sum(1 for i in range(3) for j in range(3) if state[i][j] and state[i][j] != GOAL_STATE[i][j])
    return count

def get_neighbors(node, heuristic):
    neighbors = []
    x, y = find_position(node.state, 0)
    
    for move, (dx, dy) in MOVES.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in node.state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            h = heuristic(new_state)
            neighbors.append(PuzzleNode(new_state, node, move, node.g + 1, h))
    
    return neighbors

def reconstruct_path(node):
    path = []
    while node.parent:
        path.append(node.move)
        node = node.parent
    return path[::-1]

def a_star_search(initial_state, heuristic):
    start_time = time.time()
    start_node = PuzzleNode(initial_state, None, None, 0, heuristic(initial_state))
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        if current_node.state == GOAL_STATE:
            end_time = time.time()
            return reconstruct_path(current_node), current_node.g, (end_time - start_time)
        
        closed_set.add(tuple(map(tuple, current_node.state)))
        
        for neighbor in get_neighbors(current_node, heuristic):
            if tuple(map(tuple, neighbor.state)) not in closed_set:
                heapq.heappush(open_list, neighbor)
    
    return None, None, None  # No solution found

# Example usage
initial_state = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]

# Solve using Manhattan Distance
path, moves, time_taken = a_star_search(initial_state, manhattan_distance)
print("Solution using Manhattan Distance:")
print("Path:", path)
print("Total Moves:", moves)
print("Time Taken:", round(time_taken, 4), "seconds")

# Solve using Misplaced Tiles
path, moves, time_taken = a_star_search(initial_state, misplaced_tiles)
print("\nSolution using Misplaced Tiles:")
print("Path:", path)
print("Total Moves:", moves)
print("Time Taken:", round(time_taken, 4), "seconds")