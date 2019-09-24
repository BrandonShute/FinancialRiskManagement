from bisect import bisect_left


class LinearInterpolator(object):
    """ Linear interpolation. """

    def __init__(self, x_index, values):
        self.x_index = x_index
        self.values = values

    def __call__(self, x):
        # local lookups
        x_index, values = self.x_index, self.values

        i = bisect_left(x_index, x) - 1

        x1, x2 = x_index[i:i + 2]
        z1, z2 = values[i:i + 2]

        denominator = (x2 - x1)

        weight1 = (x2 - x) / denominator
        weight2 = (x - x1) / denominator

        return z1 * weight1 + z2 * weight2
