from main import Cell
from main import checkValid

def manhetten(mat, src: Cell, dest: Cell):
    """
    :param mat: a matrix
    :param src: a cell
    :param dest: another cell
    :return: usually has to be an int;
        -1 indicates that there is an exception
        to calculate a manhetten distance
    """
    if not checkValid(src.x, src.y) or not checkValid(dest.x, dest.y):
        return -1
    return abs(src.x - dest.x) + abs(src.y - dest.y)


if __name__ == '__main__':
    mat = [[1, 0, 1, 1, 1],
           [1, 0, 1, 0, 1],
           [1, 1, 1, 0, 1],
           [0, 0, 0, 0, 1],
           [1, 1, 1, 0, 1]]

    source = Cell(0, 0)
    dest = Cell(1, 4)

    h = manhetten(mat, source, dest)
    print(h)