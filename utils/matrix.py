# It's like implementing numpy!

from collections.abc import Callable, Sequence
from fractions import Fraction


class Array2D():
    def __init__(self, data: Sequence[Sequence[Fraction | int]]):
        assert (len(data) > 0)
        assert (len(data[0]) > 0)
        self.m = len(data)
        self.n = len(data[0])
        self.arr: list[list[Fraction]] = []
        for row in data:
            assert len(row) == self.n
            self.arr.append([Fraction(n) for n in row])

    @classmethod
    def zeros(cls, m: int, n: int) -> Array2D:
        return cls([[0 for _ in range(n)] for _ in range(m)])

    def shape(self) -> tuple[int, int]:
        return (self.m, self.n)

    def copy(self) -> Array2D:
        return Array2D(self.arr)

    def pretty(self) -> str:
        return f"ARRAY\n[{'\n'.join(
            ['\t'.join([str(el) for el in row]) for row in self.arr]
        )}]"

    # ELEMENTARY ROW OPERATIONS
    def swap(self, row1: int, row2: int) -> Array2D:
        r = Array2D(self.arr)
        r.swap_inplace(row1, row2)
        return r

    def swap_inplace(self, row1: int, row2: int) -> None:
        data = self.arr[row1]
        self.arr[row1] = self.arr[row2]
        self.arr[row2] = data

    def apply_to_row(self, row: int, func: Callable[[Fraction], Fraction]) -> Array2D:
        r = Array2D(self.arr)
        r.apply_to_row_inplace(row, func)
        return r

    def apply_to_row_inplace(self, row: int, func: Callable[[Fraction], Fraction]) -> None:
        for i in range(len(self.arr[row])):
            self.arr[row][i] = func(self.arr[row][i])

    def subtract_row(self, row: int, source: int) -> Array2D:
        r = Array2D(self.arr)
        r.subtract_row_inplace(row, source)
        return r

    def subtract_row_inplace(self, row: int, source: int) -> None:
        start_idx = -1
        for i in range(len(self.arr[source])):
            if self.arr[source][i] != 0:
                start_idx = i
                break
        assert start_idx >= 0
        scalar = self.arr[row][start_idx] / self.arr[source][start_idx]
        for i in range(len(self.arr[row])):
            self.arr[row][i] -= scalar * self.arr[source][i]

    def is_rref(self) -> bool:
        cur_pivot_col = -1
        for irow, row in enumerate(self.arr):
            zeros = True
            for icol, val in enumerate(row):
                if val != 0:
                    if val != 1 or icol <= cur_pivot_col:
                        return False
                    cur_pivot_col = icol
                    for i in range(len(self.arr)):
                        if i != irow and self.arr[i][icol] != 0:
                            return False
                    zeros = False
                    break
            if zeros:
                cur_pivot_col = len(self.arr[0])
        return True

    def fixed_vars(self) -> list[int]:
        assert self.is_rref()
        r = []
        for row in self.arr:
            for icol, val in enumerate(row):
                if val != 0:
                    r.append(icol)
                    break
        return r

    def free_vars(self) -> list[int]:
        fixed = self.fixed_vars()
        return [i for i in range(len(self.arr[0]) - 1) if i not in fixed]


# Using Gauss-Jordan elimination


def rref(a: Array2D):
    a = a.copy()
    cur_row = 0
    cur_col = 0
    while cur_row < len(a.arr):
        if cur_col == len(a.arr[0]) - 1:
            break

        # find a row starting with 0 and move it to the top
        for i in range(cur_row, len(a.arr)):
            if a.arr[i][cur_col] != 0:
                a.swap_inplace(cur_row, i)
                break
        if a.arr[cur_row][cur_col] == 0:
            cur_col += 1
            continue

        # normalize current row
        normalizing_quotient = 1 / a.arr[cur_row][cur_col]
        a.apply_to_row_inplace(cur_row, lambda x: x * normalizing_quotient)

        # subtract from future rows
        for i in range(cur_row + 1, len(a.arr)):
            a.subtract_row_inplace(i, cur_row)
        cur_row += 1
        cur_col += 1

    # backprop
    cur_row = len(a.arr) - 1
    while all(a.arr[cur_row][i] == 0 for i in range(len(a.arr[cur_row]))):
        cur_row -= 1
    for backrow in range(cur_row, 0, -1):
        for i in range(backrow):
            a.subtract_row_inplace(i, backrow)

    assert a.is_rref()
    return a


def test():
    # Example from Wikipedia
    arr = Array2D([[1, 3, 1, 9], [1, 1, -1, 1], [3, 11, 5, 35]])
    print(arr.pretty())
    res = rref(arr)
    print(res.pretty())
    assert res.arr == [[1, 0, -2, -3], [0, 1, 1, 4], [0, 0, 0, 0]]
    arr2 = Array2D([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
    print(arr2.pretty())
    res2 = rref(arr2)
    print(res2.pretty())
    assert res2.arr == [[1, 0, 0, 2], [0, 1, 0, 3], [0, 0, 1, -1]]
    arr3 = Array2D([[1, 0, 0, 2], [0, 1, 0, 3], [0, 0, 1, -1]])
    print(arr3.pretty())
    res3 = rref(arr3)
    print(res3.pretty())
    assert res3.arr == [[1, 0, 0, 2], [0, 1, 0, 3], [0, 0, 1, -1]]
    arr4 = Array2D([[1, 0, 1, 0, 2], [0, 1, 5, 0,  3], [0, 0, 0, 1, -1]])
    print(arr4.pretty())
    res4 = rref(arr4)
    print(res4.pretty())
    assert res4.arr == arr4.arr


if __name__ == '__main__':
    test()
