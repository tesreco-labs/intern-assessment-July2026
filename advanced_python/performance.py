import functools
import time

from .logging_config import get_logger


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        execution_time = time.perf_counter() - start_time
        get_logger().info(
            "Function=%s ExecutionTime=%.6fs Result=%s",
            func.__name__,
            execution_time,
            result,
        )
        return result

    return wrapper


@log_execution
def calculate_performance_score(attendance_score, task_score, mentor_score):
    score = (attendance_score * 0.30) + (task_score * 0.50) + (mentor_score * 0.20)
    return round(score, 2)
