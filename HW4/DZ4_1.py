import re
car_nambers = [ 'АБ22ВВ193',  
    'А222BС96',  
    'А123ВВ777', 
    'А222ZС96',
    'АБ22ВВ1',    
    'АБ22ВВ1934',
    'АБ22ВВ19',   
    'А022ВВ7799',     
    'АБ22ВВ193X', 
    'А227ВВ19А222BС96',  
]
letter_patern = r'[АВЕКМНОРСТХУABEKMHOPCTXY]'
full_patern = letter_patern + r'\d{3}' + letter_patern + r'{2}\d{2,3}$'
for full_namber in car_nambers:
    namb = re.fullmatch(full_patern, full_namber)
    if namb:
        print(f'Результат: Номер {namb.group()[0:6]} валиден. Регион {namb.group()[6:]}.') 
    else:
        print(f'Результат: Номер не валиден.')
