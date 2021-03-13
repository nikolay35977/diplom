import xlrd
import numpy as np
import matplotlib.pyplot as plt
import math


def make_json_from_data(column_names, row_data):
    row_list = []
    for item in row_data:
        json_obj = {}
        for i in range(0, column_names.__len__()):
            json_obj[column_names[i]] = item[i]
        row_list.append(json_obj)
    return row_list


def xls_to_dict(workbook_url):
    workbook_dict = {}
    book = xlrd.open_workbook(workbook_url)
    sheets = book.sheets()
    for sheet in sheets:
        if sheet.name == 'PortHoles & Discrete Appurtenan':
            continue
        workbook_dict[sheet.name] = {}
        columns = sheet.row_values(0)
        rows = []
        for row_index in range(1, sheet.nrows):
            row = sheet.row_values(row_index)
            rows.append(row)
        sheet_data = make_json_from_data(columns, rows)
        workbook_dict[sheet.name] = sheet_data
    return workbook_dict


def make_array_from_dict(dictionary):
    new_array = []
    for part in dictionary:
        new_array.append([part['x'], part['y']])
    return new_array


def draw_result(points_array, store):
    M = np.array(points_array)

    rows, cols = M.T.shape

    for i, l in enumerate(range(0, cols)):
        xs = [store['x'], M[i, 0]]
        ys = [store['y'], M[i, 1]]
        plt.plot(xs, ys)

    plt.plot(store['x'], store['y'], 'ok')
    plt.axis('equal')
    plt.show()


def fill_payoff_matrix(points_array, r, store):
    d = []
    for i in range(0, r + 1):
        row = []
        if i == 0:
            x1 = store['x']
            y1 = store['y']
        else:
            x1 = points_array[i - 1][0]
            y1 = points_array[i - 1][1]
        for j in range(0, r + 1):
            if j > i:
                x2 = points_array[j - 1][0]
                y2 = points_array[j - 1][1]
                dist = math.hypot(x2 - x1, y2 - y1)
                row.append(round(dist, 2))
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


def print_matrix(matrix):
    max_len = max([len(str(e)) for r in matrix for e in r])
    for row in matrix:
        print(*list(map('{{:>{length}}}'.format(length=max_len).format, row)))


def make_array_q_from_dict(dictionary):
    new_array = []
    for el in dictionary:
        new_array.append(el['q'])
    return new_array


def get_route_q(route_array, q_array):
    check_q_route = 0
    for key in route_array:
        if key > 0:
            check_q_route += q_array[key - 1]
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
                            max_elem_j - 1] + get_route_q(route_array[find_i_in_matrix], q_array) < Q:
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
                        if (max_elem_j == first_point or max_elem_j == last_point) and q_array[max_elem_i - 1] + get_route_q(route_array[find_j_in_matrix], q_array) < Q:
                            boolean = False
                            max_elem_array.append(max_elem)
                            max_elem = 0
                        else:
                            if max_elem_j != first_point or max_elem_j != last_point:
                                boolean = True
                                max_elem_array.append(max_elem)
                                max_elem = 0
    return [max_elem_i, max_elem_j]


def count_route(route):
    count = 0
    for i in range(0, len(route)):
        for j in range(0, len(route[i])):
            count += 1
    return count



store = {'x': 10.0, 'y': 15.0}
r = 12
sample = xls_to_dict("Files/input.xls")
points_array = make_array_from_dict(sample['Лист1'])

draw_result(points_array, store)
payoff_matrix = fill_payoff_matrix(points_array, r, store)
print_matrix(payoff_matrix)
route_array = []
block_array = []
Q = 1500
q_array = make_array_q_from_dict(sample['Лист1'])
print(q_array)
q_route = 0

while count_route(route_array) < r:
    new_route = find_max_payoff(payoff_matrix, route_array, block_array, q_array, Q)
    new_route_array = []
    way_i = find_in_matrix(new_route[0], route_array)
    way_j = find_in_matrix(new_route[1], route_array)
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
print(route_array)
