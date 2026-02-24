def task_1(n: int):
    for i in range(1, n+1):
        yield i**2

def evens(n: int):
    for i in range(n+1):
        if i%2 == 0:
            yield i
        else:
            pass

def task_2(n: int):
    a = ",".join(str(i) for i in evens(n))
    print(a)

def divisible_3_4(n: int):
    for i in range(n+1):
        if i%3 == 0 and i%4 == 0:
            yield i

def squares(a: int, b: int):
    for i in range(a, b+1):
        yield i**2

def nums(n: int):
    for i in range(n, 0-1, -1):
        yield i


if __name__ == "__main__":
    a = squares(1, 8)
    for i in a:
        print(i)
