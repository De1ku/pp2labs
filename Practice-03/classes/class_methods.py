# 1 @classmethod alternative constructor (using cls, not self)
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_birth_year(cls, name, birth_year, current_year):
        return cls(name, current_year - birth_year)

p = Person.from_birth_year("Ali", 2008, 2026)
print(p.name, p.age)


# 2 @classmethod to modify data in class
class App:
    version = "1.0"

    @classmethod
    def set_version(cls, v):
        cls.version = v

App.set_version("1.1")
print(App.version)


# 3 @staticmethod
class MathTools:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

print(MathTools.is_even(10))


# 4 staticmethod
class Validator:
    @staticmethod
    def is_valid_name(name):
        return isinstance(name, str) and len(name.strip()) >= 2

print(Validator.is_valid_name("A"))
print(Validator.is_valid_name("Ali"))


# 5 instance method vs classmethod
class Team:
    team_name = "Unknown"

    def __init__(self, member):
        self.member = member

    @classmethod
    def rename(cls, new_name):
        cls.team_name = new_name

t = Team("Dana")
Team.rename("Wolves")
print(t.member, t.team_name, Team.team_name)
