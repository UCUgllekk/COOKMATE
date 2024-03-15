emp = {}
emp['meal1'] = {'Ingredients': 1,
                'Instructions': 1}

st = [{'hello': {'hi': 1,
            'goodby': 1}}]
for i in st:
    for i,j in i.items():
        print(i,j['hi'])
# new_lst = list(st[0])
# print(new_lst['hi'])