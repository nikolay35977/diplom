from ClarkeWrightMethod2 import ClarkeWrightMethod
from AntAlgorithm import AntAlgorithm
from AntAlgorithm2 import AntAlgorithm2
from test_helper import fill_matrix, check_length_track, refactor_clarke_wright

r = 13
path = "Files/input2.xls"
Q = 1500

distance_matrix = fill_matrix(path, r)
ClarkeWright = ClarkeWrightMethod(path, r, Q)
ClarkeWright = refactor_clarke_wright(ClarkeWright)
sAntAlgorithm = check_length_track(AntAlgorithm(path, r, Q), distance_matrix)
sAntAlgorithm2 = check_length_track(AntAlgorithm2(path, r, Q), distance_matrix)
for i in range(20000):
    x = check_length_track(AntAlgorithm2(path, r, Q), distance_matrix)
    y = check_length_track(AntAlgorithm(path, r, Q), distance_matrix)
    print(x, y)
    if sAntAlgorithm2 > x:
        sAntAlgorithm2 = x
    if sAntAlgorithm > y:
        sAntAlgorithm = y



print('AntAlgorithm: ', sAntAlgorithm)
print('ClarkeWright: ', check_length_track(ClarkeWright, distance_matrix))
print('AntAlgorithm2: ', sAntAlgorithm2)