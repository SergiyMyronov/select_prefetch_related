import functools
import time

from django.db import connection, reset_queries


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")  # noqa
        print(f"Number of Queries : {end_queries - start_queries}")  # noqa
        print(f"Finished in : {(end - start):.2f}s")  # noqa
        return result

    return inner_func
