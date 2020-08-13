from find_landings import all_landings
import numpy as np
from direct_keys import *
from copy import deepcopy

FIELD_SIZE = [20, 10]


def clear_line(field):
    """
    counts and clears full lines
    :param field:
    :return: field
    """
    full_cnt = 0
    i = 0
    while i < len(field):
        if all(field[i]) == 1:
            full_cnt += 1
            del field[i]
            field.insert(0, [0]*FIELD_SIZE[1])
        else:
            i += 1
    return field, full_cnt


def find_roofs(field):
    """
    finds blank squares under landed pieces
    :param field:
    :return:
    """
    tops = [100]*10
    blank_cnt = 0
    for i in range(len(field)):
        for j in range(FIELD_SIZE[1]):
            if field[i][j] and tops[j] == 100:
                tops[j] = i
            elif not field[i][j] and tops[j] != 100:
                blank_cnt += 1
    return blank_cnt, 17 - min(tops)


def almost_full_line(field):
    score = 0
    for i in range(len(field)):
        if sum(field[i]) == 9:
            score += 1
        if sum(field[i]) == 8:
            score += 0.5
    return score


def get_score(field):
    """
    tells how good a position is
    :param field:
    :return:
    """
    field = field.tolist()
    score = 100

    clear = clear_line(field)
    field = clear[0]
    score += (3 * clear[1]) ** 2

    roofs = find_roofs(field)
    score -= roofs[0] * 5
    score -= round(roofs[1] ** 1.3, 2)
    score += almost_full_line(field)
    return score


def choose_action(field, piece_idx):
    """
    finds the best action to take
    :param field:
    :param piece_idx:
    :return: [rotation, x_pos], max_score
    """
    results = all_landings(field[4:], piece_idx)
    for i in range(len(results)):
        results[i].append(get_score(deepcopy(results[i][0])))
    results.sort(key=lambda x: x[3], reverse=True)
    return results[0][1], results[0][2], results[0][3]


def place_piece(rotation, x_pos):
    for i in range(rotation):
        click_key(rotate_k)
    move = x_pos - 3  # 3 is the starting position
    for i in range(abs(move)):
        if move > 0:
            click_key(mv_right)
        else:
            click_key(mv_left)
    click_key(place_k)
