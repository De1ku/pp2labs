import math


def task_1(deg: float | int) -> float:
    """Function to convert degree to radian""" 
    return (deg * math.pi) / 180

def task_2(h:int | float, b1: int | float, b2: int | float) -> int | float:
    """Function to calculate the area of a trapezoid"""
    return (b1 + b2) * h / 2

def task_3(n: int | float, s: int | float) -> int: #return without point
    """Function to calculate the area of regular polygon"""
    return int((n * s * s) / (4 * math.tan(math.pi / n)))

def task_4(base: int | float, height: int | float) -> float: # float cause in expected there is zero after the point (30.0)
    """Function to calculate the area of parallelogram"""
    return base * height


if __name__ == "__main__":
    print(f"{task_1(15):.6f}")
    print(task_2(5, 5, 6))
    print(task_3(4, 25))
    print(task_4(5, 6))