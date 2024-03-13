import re
from rest_framework.validators import ValidationError
import requests
import threading

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
    

class SmsThread(threading.Thread):
    def __init__(self, sms):
        self.sms = sms
        super(SmsThread, self).__init__()

    def run(self):
        send_message(self.sms)

def send_message(message_txt):
    url = "https://api.telegram.org/bot7012407877:AAG3NjzfoLM5jcsMP3yVI-mnDpn0DNz6uNA/sendMessage"
    params = {'chat_id': '856028802', 'text': message_txt}
    response = requests.post(url, data=params)
    return response.json()

def send_sms(sms_text):
    sms_thread = SmsThread(sms_text)
    sms_thread.start()
    sms_thread.join()