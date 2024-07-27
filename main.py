# Inspired by LeetCode Problem 202. Happy Number
# Zach Stumpf 2024

import matplotlib.pyplot as plt
import numpy as np

import time
from typing import Callable, Tuple, Iterable
import statistics

class SumDigitsSquared:
    """
    A class to calculate the sum of the squares of the digits of an integer.

    Ex: 25 -> 2**2 + 5**5 = 4 + 25 = 29

    This class provides two methods, `MathMethod` and `StrMethod`, to perform the
    calculation using different approaches.
    """
    maxConstraint = True

    @staticmethod
    def validate_n(n: int) -> None:
        """
        Raises ValueError if n is not within constraints as defined by LeetCode.
        Bypass this check by setting SumDigitsSquared.maxConstraint to False.
        """
        MIN = 1
        MAX = 2**31 - 1
        if not (MIN <= n <= MAX):
            raise ValueError(
                f"n = {n} violates constraint: {MIN} <= n <= {MAX}")

    @classmethod
    def MathMethod(cls, n: int) -> int:
        """
        Uses mod (%) to get the last digit, then floor division by 10 to remove
        that last digit, repeats until done squaring and adding the digits.

        """
        if cls.maxConstraint: cls.validate_n(n)

        result = 0
        while n > 0:
            last = n % 10
            result += last**2
            n = n // 10
        return result

    @classmethod
    def StrMethod(cls, n: int) -> int:
        """
        Converts n to a string, converts each character to an int,
        squares the ints and sums them.

        """
        if cls.maxConstraint: cls.validate_n(n)

        return sum([int(i) ** 2 for i in str(n)])


def time_it(func: Callable) -> float:
    """
    Returns execution time of a function in nanoseconds (ns).

    """
    start = time.perf_counter_ns()
    func()
    end = time.perf_counter_ns() - start
    return end

def compute_avg_times(nValues: Iterable[int]) -> Tuple[float, float]:
    """
    Runs MathMethod and StrMethod, returning a tuple of the average times:
    (average MathMethod, average StrMethod)

    To find the average of each method, the method is ran and timed for each
    value in nValues, and the average of the times is taken.

    Ex: To do 100 trials of n = 25, pass nValues = [25] * 100.

    """
    # yMath means y-values (dependent variables) for the Math method
    # lambda used because time_it requires a function as parameter
    yMath = [time_it(lambda: SumDigitsSquared.MathMethod(x)) for x in nValues]
    yStr = [time_it(lambda: SumDigitsSquared.StrMethod(x)) for x in nValues]

    avgMath = statistics.mean(yMath)
    avgStr = statistics.mean(yStr)

    return (avgMath, avgStr)


if __name__ == "__main__":
    # -----------------------------------------------------------------------------
    # Generate values of n to test.
    # Specifically, we want to observe how the methods behave when n gets
    # drastically larger. To get an average of multiple trials for a specific number
    # near n, we use n and the next 10,000 values, which adds more variation
    # than just doing multiple trials of the same value of n.
    categories = ('1',
                  '100K',
                  '1M',
                  '10M',
                  '100M',
                  '1B')

    ITERATIONS = 10_000
    print(f"For each value of n, values n through n + {ITERATIONS} will be tested.\n")

    # Store numbers in variables to prevent repeating each number twice when
    # creating numpy arrays. n prefix means number.
    n1 = 1
    n100K = 100_000
    n1M = 1_000_000
    n10M = 10_000_000
    n100M = 100_000_000
    n1B = 1_000_000_000

    # Create numpy arrays for each category. x prefix means x-values (independent
    # variables).
    x1 = np.arange(n1, n1 + ITERATIONS + 1)
    x100K = np.arange(n100K, n100K + ITERATIONS + 1)
    x1M = np.arange(n1M, n1M + ITERATIONS + 1)
    x10M = np.arange(n10M, n10M + ITERATIONS + 1)
    x100M = np.arange(n100M, n100M + ITERATIONS + 1)
    x1B = np.arange(n1B, n1B + ITERATIONS + 1)
    # -----------------------------------------------------------------------------


    # -----------------------------------------------------------------------------
    # Run the experiment.
    avgTimesMath = []
    avgTimesStr = []

    print('Results\n' + '-'*70)
    for nValues in (x1, x100K, x1M, x10M, x100M, x1B):
        # Run the tests
        avgTimeMath, avgTimeStr = compute_avg_times(nValues)
        print(f"n = {nValues[0]:<15} Math: {avgTimeMath:<8,.0f} ns      String: {avgTimeStr:<8,.0f} ns")
        
        # Collect data
        avgTimesMath.append(avgTimeMath)
        avgTimesStr.append(avgTimeStr)
    # -----------------------------------------------------------------------------


    # -----------------------------------------------------------------------------
    # Generate the graph.
    x_pos = np.arange(len(categories))


    # Increase image quality of plots
    # After 150 DPI, python3 has trouble displaying plot in window
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300 # industry standard for printing


    plt.figure(figsize=(8, 6))

    plt.bar(x_pos - 0.2, avgTimesMath, width=0.4,
            color='tab:blue', align='center', label='Math Method')
    plt.bar(x_pos + 0.2, avgTimesStr, width=0.4, color='tab:orange',
            align='center', label='String Method')

    plt.xticks(x_pos, categories)
    plt.xlabel('Value of n')
    plt.ylabel('Average Execution Time (ns) for n Through n + 10K')
    plt.title('Average Execution Time for SumDigitsSquared Methods')
    plt.legend()

    plt.savefig("SumDigitsSquaredGraph.png")
    plt.show()
    # -----------------------------------------------------------------------------
