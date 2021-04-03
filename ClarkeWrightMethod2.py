import ParseFromExel
from numpy.linalg import inv

def print_matrix(matrix):
    max_len = max([len(str(e)) for r in matrix for e in r])
    for row in matrix:
        print(*list(map('{{:>{length}}}'.format(length=max_len).format, row)))


def fill_payoff_matrix(distance_matrix, r):
    d = []
    for i in range(0, r):
        row = []
        for j in range(0, r):
            if j > i:
                if distance_matrix[i][j] != float('inf'):
                    row.append(distance_matrix[i][j - i])
                else:
                    row.append(-1)
            elif j < i:
                if distance_matrix[i][j] != float('inf'):
                    Sij = d[0][i] + d[0][j] - d[j][i]
                    if Sij > 0:
                        row.append(round(Sij, 2))
                    else:
                        row.append(0)
                else:
                    row.append(-1)
            else:
                row.append(j)
        d.append(row)
    print_matrix(d)
    return d

def count_route(route):
    count = 0
    for i in range(0, len(route)):
        for j in range(0, len(route[i])):
            count += 1
    return count


def get_route_q(route_array, q_array):
    check_q_route = 0
    for key in route_array:
        if key > 0:
            check_q_route += q_array[key]
    return check_q_route


def find_in_matrix(item, matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if item == matrix[i][j]:
                return i
    i = -1
    return i

def find_in_matrix_max(r, payoff_matrix, max_elem_array, max_elem):
    max_elem_i = 1
    max_elem_j = 1
    for i in range(0, r):
        for j in range(0, i):
            if max_elem < payoff_matrix[i][j] and payoff_matrix[i][j] not in max_elem_array:
                max_elem = payoff_matrix[i][j]
                max_elem_i = i
                max_elem_j = j
    return max_elem, max_elem_i, max_elem_j


def find_max_payoff(payoff_matrix, route_array, block_array, q_array, Q):
    max_elem_i = 1
    max_elem_j = 1
    max_elem = -1
    boolean = True
    max_elem_array = []
    r = len(payoff_matrix)
    while boolean:
        boolean = False
        max_elem, max_elem_i, max_elem_j = find_in_matrix_max(r, payoff_matrix, max_elem_array, max_elem)
        if max_elem_i in block_array and max_elem_j in block_array:
            boolean = True
            max_elem_array.append(max_elem)
            max_elem = 0
        else:
            if len(route_array) > 0:
                find_i_in_matrix = find_in_matrix(max_elem_i, route_array)
                find_j_in_matrix = find_in_matrix(max_elem_j, route_array)
                print(find_i_in_matrix, find_j_in_matrix, max_elem_i, max_elem_j)
                if find_i_in_matrix != -1 and find_j_in_matrix != -1:
                    boolean = True
                    max_elem_array.append(max_elem)
                    max_elem = 0
                else:
                    if find_i_in_matrix == -1 and find_j_in_matrix == -1:
                        boolean = False
                        max_elem_array.append(max_elem)
                        max_elem = 0
                    elif find_i_in_matrix != -1:
                        first_point = route_array[find_i_in_matrix][0]
                        last_point = route_array[find_i_in_matrix][len(route_array[find_i_in_matrix]) - 1]
                        if (max_elem_i == first_point or max_elem_i == last_point) and q_array[
                            max_elem_j] + get_route_q(route_array[find_i_in_matrix], q_array) < Q:
                            boolean = False
                            max_elem_array.append(max_elem)
                            max_elem = 0
                        else:
                            if max_elem_i != first_point or max_elem_i != last_point:
                                boolean = True
                                max_elem_array.append(max_elem)
                                max_elem = 0
                    else:
                        first_point = route_array[find_j_in_matrix][0]
                        last_point = route_array[find_j_in_matrix][len(route_array[find_j_in_matrix]) - 1]
                        if (max_elem_j == first_point or max_elem_j == last_point) and q_array[
                            max_elem_i] + get_route_q(route_array[find_j_in_matrix], q_array) < Q:
                            boolean = False
                            max_elem_array.append(max_elem)
                            max_elem = 0
                        else:
                            if max_elem_j != first_point or max_elem_j != last_point:
                                boolean = True
                                max_elem_array.append(max_elem)
                                max_elem = 0
    return [max_elem_i, max_elem_j]


def check_route(route, all_route):
    new_route = []
    for i in range(0, len(route)):
        for j in range(0, len(route[i])):
            new_route.append(route[i][j])
    return list(set(all_route) - set(new_route))


def put_route(r):
    array = []
    c = 0
    for i in range(r):
        array.append(c)
        c += 1
    return array


def ClarkeWrightMethod(q_array, distance_matrix, r, Q):
    # print_matrix(distance_matrix)
    payoff_matrix_direct = fill_payoff_matrix(distance_matrix, r)
    route_array = []
    block_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    all_route = put_route(r)
    print_matrix(payoff_matrix_direct)
    while count_route(route_array) < r - 1:
        new_route = find_max_payoff(payoff_matrix_direct, route_array, block_array, q_array, Q)
        new_route_array = []
        way_i = find_in_matrix(new_route[0], route_array)
        way_j = find_in_matrix(new_route[1], route_array)
        print(check_route(route_array, all_route))
        print(route_array)
        if way_i != -1:
            if new_route[0] == route_array[way_i][0]:
                route_array[way_i].insert(0, new_route[1])
            else:
                route_array[way_i].append(new_route[1])
        elif way_j != -1:
            if new_route[1] == route_array[way_j][0]:
                route_array[way_j].insert(0, new_route[0])
            else:
                route_array[way_j].append(new_route[0])
        else:
            new_route_array.append(new_route[0])
            new_route_array.append(new_route[1])
        if len(new_route_array) != 0:
            route_array.append(new_route_array)

    return route_array


path = "Files/input3.xls"
r = 121
Q = 1.5
keyWord = 'Адрес'
qKeyWord = 'Документ задание.Вес брутто'
distanceKeyWord = 'Расстояние'
connectionsMatrix = ParseFromExel.make_points_dict(path, keyWord, r)
q_array = ParseFromExel.make_q_array(path, qKeyWord, connectionsMatrix, r)
distance_matrix = ParseFromExel.make_distance_matrix(path, distanceKeyWord, connectionsMatrix, r)
print_matrix(distance_matrix)
ClarkeWrightMethod(q_array, distance_matrix, r, Q)