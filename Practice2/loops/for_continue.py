for i in range(1, 11): #принт четных
    if i % 2 != 0:
        continue
    print(i)



lines = ["hi", "", "ok", ""]
for line in lines: #пропуск пустых
    if line == "":
        continue
    print(line)



words = ["cat", "python", "hi", "code"]
for w in words: #пропуск короче 4
    if len(w) < 4:
        continue
    print(w)



nums = [5, -2, 7, -1, 3]
total = 0
for x in nums: #сумма положительных
    if x < 0:
        continue
    total += x
print(total)



nums = [10, 0, 5]
for x in nums: #пропуск нуля
    if x == 0:
        continue
    print(100 / x)
