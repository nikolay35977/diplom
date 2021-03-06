import ParseFromExel
import random
import time


def print_matrix(matrix):
    max_len = max([len(str(e)) for r in matrix for e in r])
    for row in matrix:
        print(*list(map('{{:>{length}}}'.format(length=max_len).format, row)))


def fill_tau_matrix(r):
    tau = []
    for i in range(r):
        row = []
        for j in range(0, r):
            row.append(1)
        tau.append(row)
    return tau


def fill_matrix(distance_matrix, r):
    d = []
    for i in range(0, r):
        row = []
        for j in range(0, r):
            if j > i:
                row.append(distance_matrix[i][j - i])
            elif j < i:
                row.append(distance_matrix[j][i - j])
            else:
                row.append(0)
        d.append(row)
    return d


def sum_variants(i, alpha, betta, distance_matrix, tau, r, tracks):
    S = 0
    for k in range(r):
        if k not in tracks and distance_matrix[i][k] != 0:
            nij = 1 / distance_matrix[i][k]
            Xij = pow(nij, betta) * pow(tau[i][k], alpha)
            S += Xij
    return S


def find_random_in_array(array, x):
    for i in range(len(array)):
        if array[i] > x:
            return i
    return len(array) - 1


def loop_for_track(alpha, betta, distance_matrix, tau, block_track, q_array, r, Q, timeout):
    q_track = 0
    hasSpace = True
    i = 0
    track = [0]
    while hasSpace:
        S = 0
        dict = {}
        variants = sum_variants(i, alpha, betta, distance_matrix, tau, r, block_track)
        count_p = 0
        P = []
        for j in range(r):
            if j not in block_track and distance_matrix[i][j] != 0 and q_track + q_array[j] < Q:
                nij = 1 / distance_matrix[i][j]
                if variants != 0:
                    x = (pow(nij, betta) * pow(tau[i][j], alpha)) / variants
                    S += x
                    if x != 0:
                        dict[count_p] = j
                        P.append(S)
                        count_p += 1
        if len(P) == 0:
            hasSpace = False
        else:
            interval = find_random_in_array(P, random.random())
            value = dict[interval]
            q_track += q_array[value]
            track.append(value)
            block_track.append(value)
            i = dict[interval]
        if time.time() > timeout:
            break

    track.append(0)
    return track, block_track


def check_on_tracks(tracks, i, j):
    old_k = -1
    for row in tracks:
        for k in row:
            if old_k != k:
                if (old_k == i and k == j) or (old_k == j and k == i):
                    return True
            old_k = k


def update_tau(tau, tracks, r, Q_ant, p, distance_matrix):
    for i in range(r):
        for j in range(r):
            if i != j:
                if distance_matrix[i][j] == 0:
                    del_tau = 1
                else:
                    del_tau = Q_ant / distance_matrix[i][j]
                if check_on_tracks(tracks, i, j):
                    tau[i][j] = tau[i][j] + del_tau
                else:
                    tau[i][j] = (1 - p) * tau[i][j] - del_tau
    return tau


def AntAlgorithm(q_array, distance_matrix, r, Q):
    tracks = []
    tau = fill_tau_matrix(r)
    alpha = 1
    betta = 1
    block_track = [0]
    p = 0.01
    Q_ant = 0.01

    timeout = time.time() + 10
    while len(block_track) < r and not (time.time() > timeout):
        track = loop_for_track(alpha, betta, distance_matrix, tau, block_track, q_array, r, Q, timeout)
        tracks.append(track[0])

    for i in range(2000):
        if time.time() < timeout:
            tau = update_tau(tau, tracks, r, Q_ant, p, distance_matrix)
        block_track = [0]
        tracks = []
        print(i)
        timeout = time.time() + 10
        while len(block_track) < r and not (time.time() > timeout):
            track = loop_for_track(alpha, betta, distance_matrix, tau, block_track, q_array, r, Q, timeout)
            tracks.append(track[0])
    return tracks
