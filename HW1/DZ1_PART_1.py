import json
visit_dict = {}
with open(file=r'HW1\purchase_log.txt', mode = 'r', newline='', encoding='UTF-8' ) as purchase_file: #Путь для Windows
    for list in purchase_file:
        cur = json.loads(list)
        visit_dict[cur['user_id']] = cur['category']
for key, value in visit_dict.items():
    print(f"{key} '{value}'")
