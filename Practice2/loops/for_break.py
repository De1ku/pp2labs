for i in range(1, 10): #стоп на 5
    if i == 5:
        break
    print(i)



nums = [3, 4, -1, 10]
for x in nums: #поиск первого отр-го
    if x < 0:
        print("First negative:", x)
        break



text = "abcdef"
for ch in text: #поиск
    if ch == "d":
        print("Found d")
        break




found = False
for a in range(1, 5):
    for b in range(1, 5):
        if a * b == 6:
            print("Pair:", a, b)
            found = True
            break
    if found:
        break



target = 7
nums = [1, 3, 5]
for x in nums:
    if x == target:
        print("Found")
        break
else:
    print("Not found")