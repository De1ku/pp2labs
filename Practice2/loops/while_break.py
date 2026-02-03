i = 1
while True: #break при достижении 5
    print(i)
    if i == 5:
        break
    i += 1

x = 11
while True: #поиск первого четного числа >10
    if x % 2 == 0:
        print(f"Found: {x}")
        break
    
    x += 1

total = 0
while True: #сумма вводимых чисел
    n = int(input("Number (0 to stop): "))
    if n == 0:
        break
    total += n
print("Total:", total)

password = "1234"
while True: #break если пароль верный
    attempt = input("Password: ")
    if attempt == password:
        print("Access granted")
        break
    print("Wrong password")

arr = [3, 8, 1, 9, 2]
target = 9
i = 0
while i < len(arr): #break при нахождении нужного элемента
    if arr[i] == target:
        print("Found at index", i)
        break
    i += 1
