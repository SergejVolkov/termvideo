from time import perf_counter_ns

from .format import Format


class ProfileEntry:
    _units = list(zip(
        map(int, [1, 1e3, 1e6, 1e9, 1e9 * 60, 1e9 * 3600]),
        ["ns", "μs", "ms", "s", "m", "h"]
    ))

    def __init__(self, total_value = 0, n_runs = 0,
                 cumulative = False,
                 formatting = (Format.TIME, "%.1f")):
        self.total_value = total_value
        self.n_runs = n_runs
        self.cumulative = cumulative
        self.formatting = formatting

    def __add__(self, value):
        return ProfileEntry(self.total_value + value,
                            self.n_runs + 1,
                            self.cumulative,
                            self.formatting)

    def __sub__(self, value):
        return ProfileEntry(self.total_value - value,
                            self.n_runs + 1,
                            self.cumulative,
                            self.formatting)

    def __mul__(self, value):
        return ProfileEntry(self.total_value * value,
                            self.n_runs + 1,
                            self.cumulative,
                            self.formatting)

    def __div__(self, value):
        return ProfileEntry(self.total_value // value,
                            self.n_runs + 1,
                            self.cumulative,
                            self.formatting)

    def __truediv__(self, value):
        return ProfileEntry(self.total_value / value,
                            self.n_runs + 1,
                            self.cumulative,
                            self.formatting)

    def __mod__(self, value):
        return ProfileEntry(self.total_value % value,
                            self.n_runs + 1,
                            self.cumulative)

    def __enter__(self):
        self.start_time = perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.total_value += perf_counter_ns() - self.start_time
        self.n_runs += 1
        return False

    def __str__(self):
        return self.format

    @property
    def value(self):
        if self.cumulative or self.n_runs == 0:
            return self.total_value
        return self.total_value / self.n_runs

    @property
    def format(self):
        if self.formatting[0] == Format.NUMBER:
            return self.formatting[1] % self.value
        elif self.formatting[0] == Format.PERCENT:
            return f"{self.formatting[1]} %%" % (self.value * 100)
        elif self.formatting[0] == Format.TIME:
            for bound, unit in reversed(self._units):
                if self.value >= bound:
                    return f"{self.formatting[1]} {unit}" % (self.value / bound)
            return "0"
        raise ValueError(f"format {self.formatting[0]} not understood")
