from datetime import datetime

def my_decorator(func):
    """Decorator to print the function name, execution time, and result."""

    def wrapper(*args, **kwargs):
        """Runs the function and displays its execution details."""

        print("Function name is: ",func.__name__)
        t1 = datetime.now()
        res = func(*args, **kwargs)
        t2 = datetime.now()
        print("Execution time is: ",t2-t1)
        print("Result is: ",res)
        
        return res
    return wrapper

@my_decorator
def intern_performance_calculator(project, attendance):
    """Calculates an intern's performance score based on project and attendance."""
    return (project*0.5) + (attendance*0.5)

intern_performance_calculator(9, 7)