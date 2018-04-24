import json

a = ['123',2,3,4,5,6,'撒打算']
list = [a[0],a[1],a[2],a[3],a[4]]
with open('text.csv','w',encoding='utf-8') as f:
    f.write(json.dumps(a))
print(list)