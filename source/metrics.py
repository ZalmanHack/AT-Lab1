import statistics
from math import sqrt


class STD:
    @staticmethod
    def get(actual: list, targets: list):
        assert len(actual) == len(targets)
        x = [1 if targets[index] in items else 0 for index, items in enumerate(actual)]
        x_mean = statistics.mean(x)
        return sqrt(sum([pow(item - x_mean, 2) for item in x]) / (len(x) - 1))


class MSE:
    @staticmethod
    def get(actual: list, targets: list):
        assert len(actual) == len(targets)
        x = [1 if targets[index] in items else 0 for index, items in enumerate(actual)]
        sum_error = 0.0
        for i in range(len(x)):
            sum_error += (1 - x[i] ** 2)
        mean_error = sum_error / float(len(x))
        return mean_error
