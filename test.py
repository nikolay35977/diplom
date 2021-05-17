from ClarkeWrightMethod2 import ClarkeWrightMethod
import AntAlgorithm
import AntAlgorithm2
import ParseFromExel
from test_helper import fill_matrix, check_length_track, refactor_clarke_wright

path = "Files/input3.xls"
r = 121
Q = 1.5
keyWord = 'Адрес'
qKeyWord = 'Документ задание.Вес брутто'
distanceKeyWord = 'Расстояние'
connectionsMatrix = ParseFromExel.make_points_dict(path, keyWord, r)
q_array = ParseFromExel.make_q_array(path, qKeyWord, connectionsMatrix, r)
distance_matrix = ParseFromExel.make_distance_matrix(path, distanceKeyWord, connectionsMatrix, r)

y_t = AntAlgorithm.AntAlgorithm(q_array, distance_matrix, r, Q)
y = check_length_track(y_t, distance_matrix)
print(y, y_t)
x_t = AntAlgorithm2.AntAlgorithm2(q_array, distance_matrix, r, Q)
x = check_length_track(x_t, distance_matrix)
print(x, x_t)
z_t = refactor_clarke_wright(ClarkeWrightMethod(q_array, distance_matrix, r, Q))
z = check_length_track(z_t, distance_matrix)
print(z, z_t)

for i in range(1):
    AntAlgorithm2_T = AntAlgorithm2.AntAlgorithm2(q_array, distance_matrix, r, Q)
    AntAlgorithm2_C = check_length_track(AntAlgorithm2_T, distance_matrix)
    AntAlgorithm_T = AntAlgorithm.AntAlgorithm(q_array, distance_matrix, r, Q)
    AntAlgorithm_C = check_length_track(AntAlgorithm_T, distance_matrix)
    if x > AntAlgorithm2_C:
        x = AntAlgorithm2_C
        x_t = AntAlgorithm2_T
        print('AntAlgorithm2: length: ', x, ' cars count: ', len(x_t), ' traks: ', x_t)
    if y > AntAlgorithm_C:
        y = AntAlgorithm_C
        y_t = AntAlgorithm_T
        print('AntAlgorithm: length: ', y, ' cars count: ', len(y_t), ' traks: ', y_t)

print('---------------------------------------------------------------------------------------')
print('AntAlgorithm: length: ', y, ' cars count: ', len(y_t), ' traks: ', y_t)
print('ClarkeWright: length: ', z, ' cars count: ', len(z_t), ' traks: ', z_t)
print('AntAlgorithm2: length: ', x, ' cars count: ', len(x_t), ' traks: ', x_t)
