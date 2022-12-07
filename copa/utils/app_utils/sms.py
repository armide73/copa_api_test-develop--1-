"""SMS Module"""
import requests


def send_sms(receiver, message, sender):
    """Send SMS to a single recipient"""
    data = {
        'recipients': receiver,
        'message': message,
        'sender': sender[:10]
    }
    response = requests.post(
        'https://www.intouchsms.co.rw/api/sendsms/.json',
        data,
        auth=('frank.muhiza', 'frank.muhiza'))
    return response
