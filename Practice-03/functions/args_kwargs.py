# 1
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3))
print(sum_all(10, 20, 30, 40))


# 2
def greet_many(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet_many("Hello", "Ali", "Dana", "Timur")


# 3
def show_profile(**kwargs):
    for k, v in kwargs.items():
        print(f"{k} = {v}")

show_profile(name="Aruzhan", age=19, city="Almaty")


# 4
def logger(level, *messages, **meta):
    print("LEVEL:", level)
    print("MESSAGES:", list(messages))
    print("META:", meta)

logger("INFO", "start", "connected", user="neo", retries=3)


# 5
def area_rect(w, h):
    return w * h

dims = [3, 7]
print(area_rect(*dims))

params = {"w": 5, "h": 9}
print(area_rect(**params))
