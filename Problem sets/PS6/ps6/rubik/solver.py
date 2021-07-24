from Queue import Queue

import rubik


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == (7, 8, 6, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23):
        return None
    return bfs((start, None), end)


def bfs(state_with_moves, end):
    left_queue = Queue()
    left_queue.put(state_with_moves)
    left_visited = {}

    right_queue = Queue()
    right_queue.put((end, None))
    right_visited = {}

    while not left_queue.empty():
        left_current_state = left_queue.get()
        if left_current_state[0] in left_visited:
            left_queue.task_done()
        else:
            left_next_states = do_possible_moves(left_current_state)
            for state in left_next_states:
                left_queue.put(state)
            left_visited[left_current_state[0]] = left_current_state
            left_queue.task_done()

        right_current_state = right_queue.get()

        if right_current_state[0] in left_visited:
            return build_path(left_visited[right_current_state[0]], right_current_state, left_visited, right_visited)

        if right_current_state[0] in right_visited:
            right_queue.task_done()
        else:
            right_next_states = do_possible_moves(right_current_state)
            for state in right_next_states:
                right_queue.put(state)
            right_visited[right_current_state[0]] = right_current_state
            right_queue.task_done()
    return None


def do_possible_moves(state_with_moves):
    next_possible_states = []
    for move in rubik.quarter_twists:
        state = rubik.perm_apply(move, state_with_moves[0])
        next_possible_states.append((state, move))
    return next_possible_states


def build_path(left_current_state, right_current_state, left_visited, right_visited):
    return build_path_from_left(left_current_state, left_visited) + build_path_from_right(right_current_state,
                                                                                          right_visited)


def build_path_from_left(state_with_moves, visited):
    moves = []
    while state_with_moves[1] is not None:
        moves.append(state_with_moves[1])
        inverse_move = rubik.perm_inverse(state_with_moves[1])
        parent = rubik.perm_apply(inverse_move, state_with_moves[0])
        state_with_moves = (parent, visited[parent][1])
    moves.reverse()
    return moves


def build_path_from_right(state_with_moves, visited):
    moves = []
    while state_with_moves[1] is not None:
        inverse_move = rubik.perm_inverse(state_with_moves[1])
        moves.append(inverse_move)
        parent = rubik.perm_apply(inverse_move, state_with_moves[0])
        state_with_moves = (parent, visited[parent][1])
    return moves
