names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

print("Using enumerate():")
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")

print("\nUsing zip():")
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

value1 = "123"
value2 = 45.67
value3 = [1, 2, 3]

print("\nType checking:")
print(f"value1 is str: {isinstance(value1, str)}")
print(f"value2 is float: {isinstance(value2, float)}")
print(f"value3 is list: {isinstance(value3, list)}")

number_from_string = int(value1)
int_from_float = int(value2)
string_from_number = str(number_from_string)

print("\nType conversions:")
print(f'int("{value1}") = {number_from_string}')
print(f"int({value2}) = {int_from_float}")
print(f"str({number_from_string}) = '{string_from_number}'")