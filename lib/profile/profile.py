from collections import defaultdict

from .profile_entry import ProfileEntry


class Profile(defaultdict):
    # TODO docstrings
    def __init__(self, enabled = True):
        super().__init__(ProfileEntry)
        self.enabled = enabled

    def __getitem__(self, key):
        if self.enabled:
            return super().__getitem__(key)
        return self

    def __add__(self, value):
        return self

    def __sub__(self, value):
        return self

    def __mul__(self, value):
        return self

    def __div__(self, value):
        return self

    def __truediv__(self, value):
        return self

    def __mod__(self, value):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def print_stats(self):
        for key, entry in self.items():
            print(f"{key}: {entry}")

    @property
    def total_value(self):
        return 0

    @total_value.setter
    def total_value(self, value):
        pass

    @property
    def n_runs(self):
        return 0

    @n_runs.setter
    def n_runs(self, value):
        pass

    @property
    def cumulative(self):
        return 0

    @cumulative.setter
    def cumulative(self, value):
        pass

    @property
    def formatting(self):
        return 0

    @formatting.setter
    def formatting(self, value):
        pass
