import re

from flask import Flask, request

from storage.numbers import Diaposons as PhoneNumbersDiaposons

app = Flask(__name__)


@app.route('/numberdetect/<number>')
def numberdetect(number=None):
    if re.match(r'^[7][0-9]{10}$', number):
        result = PhoneNumbersDiaposons.detect_number(int(number[1:]))
        return 200, result
    else:
        return 422
