from time import perf_counter_ns


def perf_counter_ms() -> int:
    return perf_counter_ns() // 1000000
