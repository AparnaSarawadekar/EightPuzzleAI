from queue import PriorityQueue

def make_node(state, parent=None, cost=0, depth=0):
    return {'state': state, 'parent': parent, 'cost': cost, 'depth': depth}

def make_queue(node):
    queue = PriorityQueue()
    queue.put((node['cost'], id(node), node))  # Initialize with first node
    return queue

def remove_front(queue):
    return queue.get()[2]

def empty(queue):
    return queue.empty()

def find_blank_tile(state, size):
    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                return i, j

def expand(node, size):
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

def heuristic_misplaced_tiles(state, goal_state, size):
    return sum(1 for i in range(size) for j in range(size) if state[i][j] != 0 and state[i][j] != goal_state[i][j])

def heuristic_manhattan_distance(state, goal_positions, size):
    return sum(abs(i - goal_positions[state[i][j]][0]) + abs(j - goal_positions[state[i][j]][1])
               for i in range(size) for j in range(size) if state[i][j] != 0)

def general_search(problem, queueing_function, size):
    nodes = make_queue(make_node(problem['initial_state']))
    max_queue_size = 1
    nodes_expanded = 0

    while not empty(nodes):
        node = remove_front(nodes)
        if problem['goal_test'](node['state']):
            return node, nodes_expanded, max_queue_size
        new_nodes = expand(node, size)
        nodes, max_queue_size = queueing_function(nodes, new_nodes, max_queue_size)
        nodes_expanded += 1
    return "failure", nodes_expanded, max_queue_size

def ucs_queueing_function(queue, new_nodes, max_queue_size):
    for node in new_nodes:
        queue.put((node['cost'], id(node), node))
    return queue, max(max_queue_size, queue.qsize())

def a_star_heuristic_function(queue, new_nodes, heuristic_function, max_queue_size):
    for node in new_nodes:
        h_cost = heuristic_function(node['state'])
        total_cost = node['cost'] + h_cost
        queue.put((total_cost, id(node), node))
    return queue, max(max_queue_size, queue.qsize())

def get_user_input():
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
    goal_positions = {n: divmod(idx, size) for idx, n in enumerate(sum(goal_state, ()))}

    problem = {
        'initial_state': initial_state,
        'goal_test': lambda state: state == goal_state,
        'operators': []  # Not used as expand is hardcoded
    }

    if choice == 1:
        queueing_function = lambda nodes, new_nodes, max_q: ucs_queueing_function(nodes, new_nodes, max_q)
    elif choice == 2:
        queueing_function = lambda nodes, new_nodes, max_q: a_star_heuristic_function(nodes, new_nodes,
            lambda state: heuristic_misplaced_tiles(state, goal_state, size), max_q)
    elif choice == 3:
        queueing_function = lambda nodes, new_nodes, max_q: a_star_heuristic_function(nodes, new_nodes,
            lambda state: heuristic_manhattan_distance(state, goal_positions, size), max_q)
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
