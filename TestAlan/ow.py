def strip_ow(x):
    return x.strip('\n')

with open ('ow.txt', 'r') as file:
    list_1 = list(map(strip_ow, file.readlines()))
    print (list_1)
