import json
import csv
visit_dict = {}
with open(file=r'HW1\purchase_log.txt', mode = 'r', newline='', encoding='UTF-8' ) as purchase_file: #Путь для Windows
    for list in purchase_file:
        cur = json.loads(list)
        visit_dict[cur['user_id']] = cur['category']

with open(file=r'HW1\funnel.csv', mode = 'w',newline='', encoding='utf-8') as funnel: #Путь для Windows
    funnel_ = csv.writer(funnel)
    with open(file=r'HW1\visit_log.csv', mode = 'r', encoding='utf-8') as visitlog: #Путь для Windows
        visit_log = csv.reader(visitlog)
        for list in visit_log:
            if len(list)>1:
                id = list[0]
                source = list[1]
            else:
                continue
            if id in visit_dict:
                funnel_.writerow([id,source,visit_dict[id]])
