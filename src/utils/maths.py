"""
Basic Math utility functions are defines here
"""


class Math:
    @staticmethod
    def average(values: list) -> float:
        n = len(values)
        if n == 0:
            return 0
        result = Math.sum(values) / n
        return result

    @staticmethod
    def sum(values: list) -> float:
        result = 0
        for v in values:
            result += v
        return result

    @staticmethod
    def percentile(values: list, value: float) -> float:
        values.sort()
        count = 0
        n = len(values)
        for v in values:
            if v > value:
                break
            if v <= value:
                count += 1
        return (count / n) * 100
