import re
car_id_1 = 'А222BС96'
car_id_2 = 'АБ22ВВ193'

matches = re.findall(r'[A-ZА-Я]+','AАGTЯTЕЕТ')
print(matches)