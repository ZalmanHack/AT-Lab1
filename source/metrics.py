import statistics
from math import sqrt


class Metrics:
    @staticmethod
    def __transform(actual: list, targets: list) -> list:
        assert len(actual) == len(targets)
        return [1 if targets[index] in items else 0
                for index, items in enumerate(actual)]

    @staticmethod
    def __transform_with_pos(actual: list, targets: list) -> list:
        assert len(actual) == len(targets)
        return [(len(items) - items.index(targets[index])) / len(items) if targets[index] in items else 0
                for index, items in enumerate(actual)]

    @staticmethod
    def get_std(actual: list, targets: list) -> float:
        x = Metrics.__transform(actual, targets)
        x_mean = statistics.mean(x)
        return sqrt(sum([pow(item - x_mean, 2) for item in x]) / (len(x) - 1))

    @staticmethod
    def get_mse(actual: list, targets: list) -> float:
        x = Metrics.__transform(actual, targets)
        sum_error = 0.0
        for i in range(len(x)):
            sum_error += (1 - x[i] ** 2)
        mean_error = sum_error / float(len(x))
        return mean_error

    @staticmethod
    def get_std_pos(actual: list, targets: list) -> float:
        x = Metrics.__transform_with_pos(actual, targets)
        x_mean = statistics.mean(x)
        return sqrt(sum([pow(item - x_mean, 2) for item in x]) / (len(x) - 1))

    @staticmethod
    def get_mse_pos(actual: list, targets: list) -> float:
        x = Metrics.__transform_with_pos(actual, targets)
        sum_error = 0.0
        for i in range(len(x)):
            sum_error += (1 - x[i] ** 2)
        mean_error = sum_error / float(len(x))
        return mean_error
