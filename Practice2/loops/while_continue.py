i = 1
while i <= 10: #print of нечетных 1-10
    if i % 2 == 0:
        i += 1
        continue
    print(i)
    i += 1


nums = [5, -2, 7, -1, 3]
i = 0
total = 0
while i < len(nums): #сумма без отрицательных эл-ов
    if nums[i] < 0:
        i += 1
        continue
    total += nums[i]
    i += 1
print(total)


s = "a b  c"
i = 0
result = ""
while i < len(s): # пропуск пробелов в строке
    if s[i] == " ":
        i += 1
        continue
    result += s[i]
    i += 1
print(result)


i = 1
while i <= 15: # скип чисел, кратных 3
    if i % 3 == 0:
        i += 1
        continue
    print(i)
    i += 1


while True: #читка ввода, игнор пустыпх строк
    line = input("Text (q to quit): ")
    if line == "q":
        break
    if line == "":
        continue
    print("Got:", line)
