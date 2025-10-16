from datetime import datetime as dt
from datetime import timedelta
def range(start_date,end_date):
    try:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        end_date = dt.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return []
    cur_date = start_date
    date_list = []
    while cur_date <= end_date:
        date_list.append(cur_date.strftime('%Y-%m-%d'))
        cur_date += timedelta(days=1)
    return date_list

print(range('2020-01-02','2020-01-07'))
    