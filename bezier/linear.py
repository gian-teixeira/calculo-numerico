import numpy as np

def solve_superior_triangle(aug_matrix):
    matrix = aug_matrix.copy()
    for i in range(matrix.shape[0]-1,-1,-1):
        matrix[i] /= matrix[i,i]
        for j in range(i+1,matrix.shape[0]):
            if matrix[i,j] == 0: continue
            matrix[i] -= matrix[i,j]*matrix[j]
    return matrix[:,matrix.shape[1]-1]
# ===== #

def solve_by_gauss(matrix, use_pivot = False):
    matrix = matrix.copy()
    N,M = matrix.shape
    for i in range(0,N):
        if use_pivot:
            max_index = np.argmax(np.abs(matrix)[i:,i]) + i
            matrix[[i,max_index]] = matrix[[max_index,i]]
        for k in range(i+1,N):
            factor = matrix[k][i]/matrix[i][i]
            matrix[k] = matrix[k] - matrix[i]*factor
    arg_zero_rows = np.sum(~matrix[:,:M-1].any(1))
    ans_zero_rows = np.sum(~matrix[:,M-1:].any(1))
    if arg_zero_rows != ans_zero_rows: return None #Not solvable
    if N-arg_zero_rows < M-1: return None #Infinity
    return solve_superior_triangle(matrix[:M-arg_zero_rows])
# ===== #