import ParseFromExel

def check_length_track(tracks, distance_matrix):
    old_k = -1
    length_track = 0
    for row in tracks:
        for k in row:
            if old_k != k:
                length_track += distance_matrix[old_k][k]
            old_k = k
    return length_track

def refactor_clarke_wright(tracks):
    new_track = []
    for row in tracks:
        new_row = [0]
        for k in row:
            new_row.append(k)
        new_row.append(0)
        new_track.append(new_row)
    return new_track

def fill_matrix(path, r):
    d = []
    distance_matrix = ParseFromExel.parse_matrix_from_xls(path, r)
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