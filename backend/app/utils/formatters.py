from datetime import datetime, date

def format_date(given_date):
    try:
        return datetime.strptime(given_date, "%Y-%m-%d").date()
    except:
        raise ValueError("Invalid Date Format")
    
def format_time(given_time):
    try:
        return datetime.strptime(given_time, "%H:%M").time()
    except:
        raise ValueError("Invalid Time Format")