from queue import PriorityQueue

def make_node(state, parent=None, cost=0, depth=0):
    """Create a new node."""
    return {'state': state, 'parent': parent, 'cost': cost, 'depth': depth}

def make_queue(node):
    """Initialize the priority queue with the first node."""
    queue = PriorityQueue()
    queue.put((node['cost'], id(node), node))
    return queue

def remove_front(queue):
    """Remove and return the front node from the queue."""
    return queue.get()[2]

def empty(queue):
    """Check if the queue is empty."""
    return queue.empty()

def expand(node, size):
    """Generate new nodes from the current node by moving the blank tile."""
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    blank_row, blank_col = find_blank_tile(node['state'], size)
    new_nodes = []
    for direction, (dr, dc) in directions.items():
        new_row, new_col = blank_row + dr, blank_col + dc
        if 0 <= new_row < size and 0 <= new_col < size:
            new_state = [list(row) for row in node['state']]
            new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
            new_state = tuple(map(tuple, new_state))
            new_cost = node['cost'] + 1
            new_nodes.append(make_node(new_state, node, new_cost, node['depth'] + 1))
    return new_nodes

def find_blank_tile(state, size):
    """Find the position of the blank (0) tile."""
    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                return i, j

def heuristic_misplaced_tiles(state, goal_state, size):
    """Calculate the number of misplaced tiles for a variable-sized puzzle."""
    h_cost = 0
    for i in range(size):
        for j in range(size):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                h_cost += 1
    return h_cost

def heuristic_manhattan_distance(state, goal_positions, size):
    """Calculate Manhattan distance heuristic for variable-sized puzzles."""
    h_cost = 0
    for i in range(size):
        for j in range(size):
            tile = state[i][j]
            if tile != 0:
                h_cost += abs(i - goal_positions[tile][0]) + abs(j - goal_positions[tile][1])
    return h_cost

def general_search(problem, queueing_function, size):
    """General search template."""
    nodes = make_queue(make_node(problem['initial_state']))
    max_queue_size = 1
    nodes_expanded = 0

    while not empty(nodes):
        node = remove_front(nodes)
        nodes_expanded += 1
        if problem['goal_test'](node['state']):
            return node, nodes_expanded, max_queue_size
        new_nodes = expand(node, size)
        nodes = queueing_function(nodes, new_nodes)
        max_queue_size = max(max_queue_size, nodes.qsize())
    return "failure", nodes_expanded, max_queue_size

def ucs_queueing_function(queue, new_nodes):
    """Queueing function for UCS."""
    for node in new_nodes:
        queue.put((node['cost'], id(node), node))
    return queue

def a_star_heuristic_function(queue, new_nodes, heuristic_function):
    """Queueing function for A* using a generic heuristic function."""
    for node in new_nodes:
        h_cost = heuristic_function(node['state'])
        total_cost = node['cost'] + h_cost
        queue.put((total_cost, id(node), node))
    return queue

def get_user_input():
    """Get the initial state, size, and search method choice from the user."""
    size = int(input("Enter the size of the puzzle (3 for 3x3, 4 for 4x4, 5 for 5x5): "))
    initial_state = []
    print("Enter the initial state of the puzzle (use 0 for the blank):")
    for i in range(size):
        row = input(f"Enter row {i + 1}: ")
        initial_state.append(tuple(map(int, row.split())))
    initial_state = tuple(initial_state)
    print("Choose the search method: 1 for UCS, 2 for A* Misplaced Tile, 3 for A* Manhattan Distance")
    choice = int(input("Your choice: "))
    return initial_state, choice, size


def main():
    initial_state, choice, size = get_user_input()
    goal_state = [list(range(1 + i * size, 1 + i * size + size)) for i in range(size)]
    goal_state[-1][-1] = 0
    goal_state = tuple(tuple(row) for row in goal_state)

    goal_positions = {n: (i, j) for i, row in enumerate(goal_state) for j, n in enumerate(row)}

    problem = {
        'initial_state': initial_state,
        'goal_test': lambda state: state == goal_state,
        'operators': []
    }

    if choice == 1:
        queueing_function = lambda nodes, new_nodes: ucs_queueing_function(nodes, new_nodes)
    elif choice == 2:
        queueing_function = lambda nodes, new_nodes: a_star_heuristic_function(nodes, new_nodes,
                                                                               lambda state: heuristic_misplaced_tiles(
                                                                                   state, goal_state, size))
    elif choice == 3:
        queueing_function = lambda nodes, new_nodes: a_star_heuristic_function(nodes, new_nodes,
                                                                               lambda
                                                                                   state: heuristic_manhattan_distance(
                                                                                   state, goal_positions, size))
    else:
        print("Invalid choice")
        return

    result, nodes_expanded, max_queue_size = general_search(problem, queueing_function, size)
    if result != "failure":
        print("\nSolution found:")
        print(f"Solution depth is {result['cost']}")
        print(f"Number of nodes expanded is {nodes_expanded}")
        print(f"Maximum queue size is {max_queue_size}")
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()
