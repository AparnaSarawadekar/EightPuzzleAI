def ucs_8puzzle():
    from queue import PriorityQueue

    def find_zero(state):
        for i, row in enumerate(state):
            if 0 in row:
                return i, row.index(0)

    def move(state, direction):
        moves = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }
        zero_r, zero_c = find_zero(state)
        new_r, new_c = zero_r + moves[direction][0], zero_c + moves[direction][1]
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_state = [list(row) for row in state]
            new_state[zero_r][zero_c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[zero_r][zero_c]
            return tuple(map(tuple, new_state))
        return None

    def successors(state):
        succ_states = []
        for direction in ['up', 'down', 'left', 'right']:
            new_state = move(state, direction)
            if new_state:
                succ_states.append(new_state)
        return succ_states

    # Taking input from the user for the initial state
    initial = []
    print("Enter the initial state of the 8-puzzle:")
    for i in range(3):
        row = input(f"Enter row {i + 1}: ")
        initial.append(list(map(int, row.split())))

    goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    initial_state = tuple(map(tuple, initial))

    frontier = PriorityQueue()
    frontier.put((0, initial_state))
    came_from = {}
    cost_so_far = {}
    came_from[initial_state] = None
    cost_so_far[initial_state] = 0
    max_queue_size = 0
    nodes_expanded = 0
    visited = set()
    visited.add(initial_state)

    while not frontier.empty():
        _, current = frontier.get()

        if current == goal_state:
            break

        nodes_expanded += 1
        for next_state in successors(current):
            new_cost = cost_so_far[current] + 1
            if next_state not in visited or new_cost < cost_so_far.get(next_state, float('inf')):
                cost_so_far[next_state] = new_cost
                priority = new_cost
                frontier.put((priority, next_state))
                came_from[next_state] = current
                visited.add(next_state)
        max_queue_size = max(max_queue_size, frontier.qsize())

    # Output the results
    print("\nGoal State:")
    for row in goal_state:
        print(' '.join(map(str, row)))
    print(f"Solution depth is {cost_so_far[goal_state]}")
    print(f"Number of nodes expanded is {nodes_expanded}")
    print(f"Maximum queue size is {max_queue_size}")


ucs_8puzzle()
