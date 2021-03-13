#from ParseFromExel import parse_matrix_from_xls
import ParseFromExel
import random
from ClarkeWrightMethod2 import ClarkeWrightMethod


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


def loop_for_track(alpha, betta, distance_matrix, tau, block_track, q_array, r, Q):
    q_track = 0
    InBase = False
    i = 0
    track = [0]
    while not InBase:
        S = 0
        dict = {}
        variants = sum_variants(i, alpha, betta, distance_matrix, tau, r, block_track)
        count_p = 0
        P = []
        for j in range(r):
            if j not in block_track and distance_matrix[i][j] != 0 and q_track + q_array[j] < Q:
                nij = 1 / distance_matrix[i][j]
                x = (pow(nij, betta) * pow(tau[i][j], alpha)) / variants
                S += x
                if x != 0:
                    dict[count_p] = j
                    P.append(S)
                    count_p += 1
        if len(P) == 0:
            InBase = True
            track.append(0)
        else:
            interval = find_random_in_array(P, random.random())
            value = dict[interval]
            q_track += q_array[value]
            track.append(value)
            if value == 0:
                InBase = True
            block_track.append(value)
            i = dict[interval]

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


def AntAlgorithm2(path, r, Q):
    distance_matrix = ParseFromExel.parse_matrix_from_xls(path, r)
    q_array = distance_matrix.pop()
    tau = fill_tau_matrix(r)
    distance_matrix = fill_matrix(distance_matrix, r)
    alpha = 1
    betta = 1
    block_track = []
    p = 0.01
    Q_ant = 0.01
    tracks = ClarkeWrightMethod(path, r, Q)
    tau = update_tau(tau, tracks, r, 0.1, p, distance_matrix)
    tracks = []

    while len(block_track) < r - 1:
        track = loop_for_track(alpha, betta, distance_matrix, tau, block_track, q_array, r, Q)
        tracks.append(track[0])
    tracks = []
    for i in range(10000):
        tau = update_tau(tau, tracks, r, Q_ant, p, distance_matrix)
        block_track = []
        tracks = []
        while len(block_track) < r - 1:
            track = loop_for_track(alpha, betta, distance_matrix, tau, block_track, q_array, r, Q)
            tracks.append(track[0])
    return tracks


def AntAlgorithm212(q_array, distance_matrix, r, Q):
    tau = fill_tau_matrix(r)
    alpha = 1
    betta = 1
    block_track = []
    p = 0.01
    Q_ant = 0.01
    tracks = []

    while len(block_track) < r - 1:
        track = loop_for_track(alpha, betta, distance_matrix, tau, block_track, q_array, r, Q)
        tracks.append(track[0])
    tracks = []
    for i in range(10000):
        tau = update_tau(tau, tracks, r, Q_ant, p, distance_matrix)
        block_track = []
        tracks = []
        while len(block_track) < r - 1:
            track = loop_for_track(alpha, betta, distance_matrix, tau, block_track, q_array, r, Q)
            tracks.append(track[0])
    return tracks


pathPoints = "Files/input3.xls"
r = 121
Q = 1.5
keyWord = 'Адрес'
qKeyWord = 'Документ задание.Вес брутто'
distanceKeyWord = 'Расстояние'
connectionsMatrix = ParseFromExel.make_points_dict(pathPoints, keyWord, r)
q_array = ParseFromExel.make_q_array(pathPoints, qKeyWord, connectionsMatrix, r)
distance_matrix = ParseFromExel.make_distance_matrix(pathPoints, distanceKeyWord, connectionsMatrix, r)
print(AntAlgorithm212(q_array, distance_matrix, r, Q))