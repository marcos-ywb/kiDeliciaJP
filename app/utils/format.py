import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatCurrency(value):
    return locale.currency(value, grouping=True, symbol='R$ ')

def formatDate(date):
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    elif not isinstance(date, (datetime,)):
        raise TypeError("Input deve ser uma string ou objeto datetime")
    
    return date.strftime('%d/%m/%Y - %H:%M')
