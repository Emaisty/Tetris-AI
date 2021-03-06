from copy import deepcopy

from figures import array_of_figures as pieces


def check_collision(field, piece, piece_pos):
    for i in range(4):
        for j in range(4):
            if piece[i][j]:
                if (i + piece_pos[0] >= len(field)) or (j + piece_pos[1] >= len(field[0])) or (i + piece_pos[0] < 0) or\
                        (j + piece_pos[1] < 0) or field[i + piece_pos[0]][j + piece_pos[1]]:
                    return True
    return False


def land(field, piece, pos_now):
    res = deepcopy(field)
    while not check_collision(res, piece, pos_now):
        pos_now[0] += 1
    if pos_now[0] == 0:
        return None
    pos_now[0] -= 1
    for i in range(4):
        for j in range(4):
            if i + pos_now[0] < len(field) and j + pos_now[1] < len(field[0]):
                res[i + pos_now[0]][j + pos_now[1]] += piece[i][j]
    return res


def all_landings(field, piece_index):
    """
    calculates all possible results
    :param field:
    :param piece_index:
    :return: [resulting field, rotation, x_position]
    """
    results = []
    for rotation in range(len(pieces[piece_index])):
        for x_pos in range(-3, 10):
            res = land(field, pieces[piece_index][rotation], [0, x_pos])
            if res is not None:
                results.append([res, rotation, x_pos])
    return results
