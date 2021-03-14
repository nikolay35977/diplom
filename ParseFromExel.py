import xlrd

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
        workbook_dict[sheet.name] = {}
        columns = sheet.row_values(0)
        rows = []
        for row_index in range(1, sheet.nrows):
            row = sheet.row_values(row_index)
            rows.append(row)
        sheet_data = make_json_from_data(columns, rows)
        workbook_dict[sheet.name] = sheet_data
    return workbook_dict


def make_matrix_from_dict(dictionary, r):
    new_matrix = []
    q_array = []
    i = 0
    row = []
    for part in dictionary:
        for j in range(i, r):
            row.append(part[j])
        new_matrix.append(row)
        row = []
        q_array.append(part['q'])
        i += 1
    new_matrix.append(q_array)
    return new_matrix


def parse_matrix_from_xls(path, r):
    sample = xls_to_dict(path)
    distance_matrix = make_matrix_from_dict(sample['Лист1'], r)
    return distance_matrix


# ======asdasdsad=======
def print_matrix(matrix):
    max_len = max([len(str(e)) for r in matrix for e in r])
    for row in matrix:
        print(*list(map('{{:>{length}}}'.format(length=max_len).format, row)))


def make_points_dict(workbook_url, keyWord, r):
    book = xlrd.open_workbook(workbook_url)
    sheets = book.sheets()
    rows = {}
    adressRow = 0
    i = 0
    for row_index in range(1, sheets[0].nrows):
        row = sheets[0].row_values(row_index)
        if adressRow != 0 and row_index < adressRow + r + 1:
            rows[row[0]] = i
            i += 1
        if keyWord in row:
            adressRow = row_index
    return rows


def make_q_array(workbook_url, keyWord, connectionsMatrix, r):
    book = xlrd.open_workbook(workbook_url)
    sheets = book.sheets()
    rows = [0] * r
    adressRow = 0
    for row_index in range(1, sheets[0].nrows):
        row = sheets[0].row_values(row_index)
        if row[0] == 'Итого':
            adressRow = 0
        if adressRow != 0 and row[0] != '' and row[0] != 'К выполнению':
            rows[connectionsMatrix[row[9]]] = row[0]
        if keyWord in row:
            adressRow = row_index
    return rows

def fill_zeros_matrix(r):
    rows = []
    for i in range(r):
        row = []
        for j in range(r):
            if i == j:
                row.append(0)
            else:
                row.append(0)
        rows.append(row)
    return rows

def make_distance_matrix(workbook_url, keyWord, connectionsMatrix, r):
    book = xlrd.open_workbook(workbook_url)
    sheets = book.sheets()
    rows = fill_zeros_matrix(r)
    adressRow = 0
    for row_index in range(1, sheets[0].nrows):
        row = sheets[0].row_values(row_index)
        if adressRow != 0:
            if type(row[0]) == str or row[0] == 0.001:
                rows[connectionsMatrix[row[4]]][connectionsMatrix[row[13]]] = 0
            else:
                rows[connectionsMatrix[row[4]]][connectionsMatrix[row[13]]] = row[0]
        if keyWord in row:
            adressRow = row_index
    return rows



