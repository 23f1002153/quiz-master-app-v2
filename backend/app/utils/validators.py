from datetime import datetime, date

def validate_email(email):
    if not email:
        return "Email is required"
    if "@" not in email or "." not in email:
        return "Invalid email"
    return None

def validate_phone(phone):
    if phone is None:
        return "Phone number is required"
    try:
        phone_str = str(int(phone)) # allow numeric strings also
    except (ValueError, TypeError):
        return "Phone number must be numeric"
    if len(phone_str) != 10:
        return "Phone number must contain exactly 10 digits"
    return None

def validate_gender(gender):
    valid_genders = {"male", "female", "other", "prefer not to say"}
    if not gender:
        return "Gender is required"
    if not isinstance(gender, str):
        return "Gender must be a string"
    if gender.strip().lower() not in valid_genders:
        return "Gender is not valid"
    return None

def validate_date(given_date, before_today = False, after_today = False):
    if not given_date:
        return "Date is required"
    try:
        given_date = datetime.strptime(given_date, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid Date Format. Use YYYY-MM-DD."
    today = date.today()
    if before_today:
        if given_date > today:
            return "Date cannot be in the future"
    if after_today:
        if given_date < today:
            return "Date cannot be in the past"
    return None

def validate_time(time_str):
    if not time_str:
        return "Time is required"
    try:
        # Accepts formats like "14:30", "23:59", etc.
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        return "Time must be in HH:MM (24-hour) format"
    return None

def validate_string(given_string, field, required = True):
    if not given_string:
        if required:
            return f"{field} is required"
        else:
            return None
    if not isinstance(given_string, str):
        return f"{field} must be a string"
    return None

def validate_int(given_int, field, required = True):
    if given_int is None:
        if required:
            return f"{field} is required"
        else:
            return None
    try:
        given_int = int(given_int)
        return None
    except:
        return f"{field} must be an integer"
    
def validate_bool(given_bool, field, required=True):
    if given_bool is None:
        if required:
            return None, f"{field} is required"
        else:
            return None, None

    if isinstance(given_bool, bool):
        return given_bool, None

    if isinstance(given_bool, str):
        if given_bool.lower() == "true":
            return True, None
        if given_bool.lower() == "false":
            return False, None
        return None, f"{field} is not a valid boolean"

    if isinstance(given_bool, int):
        if given_bool == 1:
            return True, None
        if given_bool == 0:
            return False, None
        return None, f"{field} is not a valid boolean"

    return None, f"{field} is not a valid boolean"
    

def validate_password(password):
    if not password or len(password) < 6:
        return "Password must be at least 6 characters"
    return None
