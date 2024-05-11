from queue import PriorityQueue

def make_node(state, parent=None, cost=0, depth=0):
    return {'state': state, 'parent': parent, 'cost': cost, 'depth': depth}

def make_queue(node):
    queue = PriorityQueue()
    queue.put((node['cost'], id(node), node))
    return queue

def remove_front(queue):
    return queue.get()[2]

def empty(queue):
    return queue.empty()

def expand(node):
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    blank_row, blank_col = find_blank_tile(node['state'])
    new_nodes = []
    for direction, (dr, dc) in directions.items():
        new_row, new_col = blank_row + dr, blank_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [list(row) for row in node['state']]
            new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
            new_state = tuple(map(tuple, new_state))
            new_cost = node['cost'] + 1  # Increment the cost for moving a tile
            new_nodes.append(make_node(new_state, node, new_cost, node['depth'] + 1))
    return new_nodes

def find_blank_tile(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def general_search(problem, queueing_function):
    nodes = make_queue(make_node(problem['initial_state']))
    max_queue_size = 1
    nodes_expanded = 0

    while not empty(nodes):
        node = remove_front(nodes)
        nodes_expanded += 1
        if problem['goal_test'](node['state']):
            return node, nodes_expanded, max_queue_size
        new_nodes = expand(node)
        nodes = queueing_function(nodes, new_nodes)
        max_queue_size = max(max_queue_size, nodes.qsize())
    return "failure", nodes_expanded, max_queue_size

def ucs_queueing_function(queue, new_nodes):
    for node in new_nodes:
        queue.put((node['cost'], id(node), node))  # Enqueue by total path cost only
    return queue

def heuristic_misplaced_tiles(state, goal_state):
    h_cost = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                h_cost += 1
    return h_cost

def heuristic_manhattan_distance(state, goal_positions):
    h_cost = 0
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                h_cost += abs(i - goal_positions[tile][0]) + abs(j - goal_positions[tile][1])
    return h_cost

def a_star_heuristic_function(queue, new_nodes, goal_state, heuristic_function):
    for node in new_nodes:
        h_cost = heuristic_function(node['state'], goal_state)
        total_cost = node['cost'] + h_cost  # g(n) + h(n)
        queue.put((total_cost, id(node), node))
    return queue

def get_user_input():
    initial_state = []
    print("Enter the initial state of the 8-puzzle (use 0 for the blank):")
    for i in range(3):
        row = input(f"Enter row {i + 1}: ")
        initial_state.append(tuple(map(int, row.split())))
    initial_state = tuple(initial_state)
    print("Choose the search method: 1 for UCS, 2 for A* Misplaced Tile, 3 for A* Manhattan Distance")
    choice = int(input("Your choice: "))
    return initial_state, choice

def main():
    initial_state, choice = get_user_input()
    goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    goal_positions = {n: (i // 3, i % 3) for i, n in enumerate(sum(goal_state, ()))}

    problem = {
        'initial_state': initial_state,
        'goal_test': lambda state: state == goal_state,
        'operators': []  # Not used as expand is hard-coded
    }

    if choice == 1:
        queueing_function = lambda nodes, new_nodes: ucs_queueing_function(nodes, new_nodes)
    elif choice == 2:
        queueing_function = lambda nodes, new_nodes: a_star_heuristic_function(nodes, new_nodes, goal_state, heuristic_misplaced_tiles)
    elif choice == 3:
        queueing_function = lambda nodes, new_nodes: a_star_heuristic_function(nodes, new_nodes, goal_state, heuristic_manhattan_distance)
    else:
        print("Invalid choice")
        return

    result, nodes_expanded, max_queue_size = general_search(problem, queueing_function)
    if result != "failure":
        print("\nSolution found:")
        print(f"Solution depth is {result['cost']}")
        print(f"Number of nodes expanded is {nodes_expanded}")
        print(f"Maximum queue size is {max_queue_size}")
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()
