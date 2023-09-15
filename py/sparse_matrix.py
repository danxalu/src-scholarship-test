from typing import List

import numpy as np


class Element:
    def __init__(self, index, value):
        self.index = index
        self.value = value


class SparseMatrix:
    def __init__(self, *, file=None, dense: np.array = None):
        self.data_: List[List[Element]] = []

        if file is not None:
            assert dense is None
            with open(file, 'r') as f:
                n = int(f.readline())
                for _ in range(n):
                    self.data_.append([])
                    line = f.readline().split()
                    for j in range(1, len(line), 2):
                        self.data_[-1].append(Element(index=int(line[j]),
                                                      value=float(line[j+1])))

        if dense is not None:
            assert file is None
            n = len(dense)
            for i in range(n):
                self.data_.append([])
                for j in range(n):
                    if dense[i, j] != 0:
                        self.data_[i].append(Element(j, dense[i, j]))

    def print(self):
        n = len(self.data_)
        print(f'{len(self.data_)} rows')
        for i in range(n):
            element_index = 0
            for j in range(n):
                if element_index < len(self.data_[i]):
                    if self.data_[i][element_index].index == j:
                        print(f'{self.data_[i][element_index].value:.2f} ', end='')
                    else:
                        print(f'{0:.2f} ', end='')
                else:
                    print(f'{0:.2f} ', end='')
            print()

    def to_dense(self):
        n = len(self.data_)
        A = np.zeros((n, n), dtype=float)
        for i in range(n):
            for element in self.data_[i]:
                A[i, element.index] = element.value
        print(self);
        print(A);
        return A

    def __matmul__(self, other):
        # vvvvv your code here vvvvv
        result = SparseMatrix(dense=self.to_dense() @ other.to_dense())
        # ^^^^^ your code here ^^^^^

        return result

    def __pow__(self, power, modulo=None):
        dense = self.to_dense();

        # vvvvv your code here vvvvv
        ##result = SparseMatrix(dense=np.linalg.matrix_power(self.to_dense(), power)
        dense_self = dense
        dense_other = np.array(dense)
        if (dense.shape[1] != dense.shape[0]):
            print("Check rows and cols!")
            return None
        lenA = dense.shape[0]

        dense_other = dense_other.transpose()

        result = np.eye(lenA)

        for apos in range(lenA):
            r = dense_self[apos][0]
            for bpos in range(lenA):
                c = dense_other[bpos][0]
                tempa = apos
                tempb = bpos
                sum_ = 0
                while (tempa < lenA and dense_self[tempa][0] == r and tempb < lenA and dense_other[tempb][0] == c):

                    if (dense_self[tempa][1] < dense_other[tempb][1]):
                        tempa += 1
                    elif (dense_self[tempa][1] > dense_other[tempb][1]):
                        tempb += 1
                    else:
                        sum_ += dense_self[tempa][2] * dense_other[tempb][2]
                        tempa += 1
                        tempb += 1

                if (sum_ != 0):
                    print("sum", sum_)
                    r = int(r)
                    c = int(c)
                    result[r][c] = sum_
                while (bpos < lenA and dense_other[bpos][0] == c):
                    bpos += 1

            while (apos < lenA and dense_self[apos][0] == r):
                apos += 1
        # ^^^^^ your code here ^^^^^

        ##result np.array
        f = open("matr", "w")
        f.write(lenA)
        f.write("\n")
        for i, j in result:
            f.write("i, j")
            f.write("\n")
        f.close()

        return result ##выводит np.array
