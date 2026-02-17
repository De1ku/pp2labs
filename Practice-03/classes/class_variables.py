# 1 static var for all objects
class Car:
    wheels = 4

a = Car()
b = Car()
print(a.wheels, b.wheels, Car.wheels)


# 2 modifying static class variable
Car.wheels = 6
print(a.wheels, b.wheels)


# 3 modifying attribute for exact exemplar
a.wheels = 3
print(a.wheels, b.wheels, Car.wheels)  # a has it's own


# 4 counter of all created objects in static var
class User:
    count = 0

    def __init__(self, name):
        self.name = name
        User.count += 1

u1 = User("Ali")
u2 = User("Dana")
u3 = User("Tim")
print(User.count)


# 5
class Bag:
    items = []

    def add(self, item):
        self.items.append(item)

b1 = Bag()
b2 = Bag()
b1.add("apple")
print(b2.items)  # surprise is also seeing "apple" (list is shared between all exemplars)
