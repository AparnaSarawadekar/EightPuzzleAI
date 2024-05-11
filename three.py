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
        if 0 <= new_row < 3:
            if 0 <= new_col < 3:
              new_state = []
              for row in node['state']:
                  new_state.append(list(row))
              new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
              new_state = tuple(map(tuple, new_state))
              new_nodes.append(make_node(new_state, node, node['cost'] + 1, node['depth'] + 1))
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
        if empty(nodes):
            return "failure", nodes_expanded, max_queue_size
        node = remove_front(nodes)
        nodes_expanded += 1
        if problem['goal_test'](node['state']):
            return node, nodes_expanded, max_queue_size
        new_nodes = expand(node)
        nodes = queueing_function(nodes, new_nodes, node['cost'])
        max_queue_size = max(max_queue_size, nodes.qsize())
    return "failure", nodes_expanded, max_queue_size

def ucs_queueing_function(queue, new_nodes, current_cost):
    for node in new_nodes:
        queue.put((current_cost + node['cost'], id(node), node))
    return queue

def a_star_misplaced_tile(queue, new_nodes, current_cost):
    goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    for node in new_nodes:
        h_cost = 0
        for i in range(3):
          for j in range(3):
              if node['state'][i][j] != goal_state[i][j]:
                if node['state'][i][j] != 0:
                  h_cost += 1
        total_cost = current_cost + node['cost'] + h_cost
        queue.put((total_cost, id(node), node))
    return queue

def a_star_manhattan_distance(queue, new_nodes, current_cost):
    goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                      4: (1, 0), 5: (1, 1), 6: (1, 2),
                      7: (2, 0), 8: (2, 1), 0: (2, 2)}
    for node in new_nodes:
        h_cost = 0
        for i in range(3):
            for j in range(3):
                tile = node['state'][i][j]
                if (tile != 0):
                    h_cost += abs(i - goal_positions[tile][0]) + abs(j - goal_positions[tile][1])
        total_cost = current_cost + node['cost'] + h_cost
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
    problem = {
        'initial_state': initial_state,
        'goal_test': lambda state: state == ((1, 2, 3), (4, 5, 6), (7, 8, 0)),
        'operators': []  # Not used as expand is hard-coded
    }

    queueing_function = {
        1: ucs_queueing_function,
        2: a_star_misplaced_tile,
        3: a_star_manhattan_distance
    }.get(choice)

    if not queueing_function:
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