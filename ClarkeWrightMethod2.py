import ParseFromExel


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
                row.append(distance_matrix[i][j-i])
            elif j < i:
                Sij = d[0][i] + d[0][j] - d[j][i]
                if Sij > 0:
                    row.append(round(Sij, 2))
                else:
                    row.append(0)
            else:
                row.append(j)
        d.append(row)
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

def find_max_payoff(payoff_matrix, route_array, block_array, q_array, Q):
    max_elem = 0
    max_elem_i = 1
    max_elem_j = 1
    boolean = True
    max_elem_array = []
    r = len(payoff_matrix)
    while boolean:
        boolean = False
        for i in range(1, r):
            for j in range(1, i):
                if max_elem < payoff_matrix[i][j] and payoff_matrix[i][j] not in max_elem_array:
                    max_elem = payoff_matrix[i][j]
                    max_elem_i = i
                    max_elem_j = j
        if max_elem_i in block_array and max_elem_j in block_array:
            boolean = True
            max_elem_array.append(max_elem)
            max_elem = 0
        else:
            if len(route_array) > 0:
                find_i_in_matrix = find_in_matrix(max_elem_i, route_array)
                find_j_in_matrix = find_in_matrix(max_elem_j, route_array)
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
                        if (max_elem_j == first_point or max_elem_j == last_point) and q_array[max_elem_i] + get_route_q(route_array[find_j_in_matrix], q_array) < Q:
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
        c+=1
    return array

def ClarkeWrightMethod(q_array, distance_matrix, r, Q):
    payoff_matrix = fill_payoff_matrix(distance_matrix, r)
    route_array = []
    block_array = []
    all_route = put_route(r)
    while count_route(route_array) < r - 1:
        new_route = find_max_payoff(payoff_matrix, route_array, block_array, q_array, Q)
        new_route_array = []
        way_i = find_in_matrix(new_route[0], route_array)
        way_j = find_in_matrix(new_route[1], route_array)
        print(check_route(route_array, all_route))
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