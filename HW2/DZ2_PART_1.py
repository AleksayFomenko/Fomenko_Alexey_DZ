from datetime import datetime as dt

def get_date(str):
    splited = str.split('-')
    if (len(splited) > 1):
        return splited[1].strip()
    return None

def parser(newspaper,formats):
    newspaper = get_date(newspaper)
    if not newspaper:
        return None
    for format in formats:
        try:
            date_datetime = dt.strptime(newspaper, format)
            return date_datetime
        except ValueError:
            continue
    return None

formats = [
'%A, %B %d, %Y',
'%A, %d.%m.%y',
'%A, %d %B %Y'
]
newspapers = [
    'The Moscow Times - Wednesday, October 2, 2002',
'The Guardian - Friday, 11.10.13',
'Daily News - Thursday, 18 August 1977'
]
for newspaper in newspapers:
    print(parser(newspaper,formats))
