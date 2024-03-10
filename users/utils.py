import re
from rest_framework.validators import ValidationError

email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
phone_number_regex = r'^\+998\d{9}$'

def check_email_or_phone_number(user_input):
    if re.match(email_regex, user_input) is not None:
        return 'Email Address'
    elif re.match(phone_number_regex, user_input) is not None:
        return 'Phone Number'
    else:
        data = {'status': False, 'message': 'Please enter your email address or phone number or incorrectly data!'}
        raise ValidationError(data)