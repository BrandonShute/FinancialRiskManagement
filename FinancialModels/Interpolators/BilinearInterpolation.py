from bisect import bisect_left


class BilinearInterpolation(object):
    """ Bilinear interpolation. """

    def __init__(self, x_index, y_index, values):
        self.x_index = x_index
        self.y_index = y_index
        self.values = values

    def __call__(self, x, y):
        # local lookups
        x_index, y_index, values = self.x_index, self.y_index, self.values

        i = bisect_left(x_index, x) - 1
        j = bisect_left(y_index, y) - 1

        x1, x2 = x_index[i:i + 2]
        y1, y2 = y_index[j:j + 2]
        z11, z12 = values[j][i:i + 2]
        z21, z22 = values[j + 1][i:i + 2]

        return (z11 * (x2 - x) * (y2 - y) + z21 * (x - x1) * (y2 - y) + z12 * (
                x2 - x) * (y - y1) + z22 * (x - x1) * (y - y1)) / (
                       (x2 - x1) * (y2 - y1))
