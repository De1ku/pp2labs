# 1 inherit 2 classes
class Fly:
    def move(self):
        return "fly"

class Swim:
    def move(self):
        return "swim"

class Duck(Fly, Swim):
    pass

d = Duck()
print(d.move())  # from Fly, because Fly is first


# 2) MRO: method resolution order
print(Duck.mro())


# 3) "Mixins"
class CanLog:
    def log(self, msg):
        return f"[LOG] {msg}"

class CanSerialize:
    def to_dict(self):
        return self.__dict__

class User(CanLog, CanSerialize):
    def __init__(self, name):
        self.name = name

u = User("Ali")
print(u.log("created"), u.to_dict())


# 4) "Diamond inheritance" and cooperative super()
class A:
    def f(self):
        return "A"

class B(A):
    def f(self):
        return super().f() + "->B"

class C(A):
    def f(self):
        return super().f() + "->C"

class D(B, C):
    def f(self):
        return super().f() + "->D"

print(D().f())
print(D.mro())


# 5
class Left:
    def hello(self):
        return "left"

class Right:
    def hello(self):
        return "right"

class Both(Left, Right):
    pass

print(Both().hello())  # left
