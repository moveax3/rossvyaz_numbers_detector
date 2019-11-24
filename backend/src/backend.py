import re

from flask import (
    Flask,
    json,
)

from storage.numbers import Diaposon as PhoneNumbersDiaposon

app = Flask(__name__)


@app.route('/numberdetect/<number>')
def numberdetect(number=None):
    if re.match(r'^[7][0-9]{10}$', number):
        result = PhoneNumbersDiaposon.detect_number(int(number[1:]))
        try:
            resp_data = {'opsos': result[0], 'location': result[1]}
        except TypeError:
            resp_data = {'opsos': 'Not found', 'location': 'Not found'}
        response = app.response_class(
            response=json.dumps(resp_data, ensure_ascii=False, encoding='utf8'),
            mimetype='application/json',
            content_type='application/json; charset=utf-8',
            status=200,
        )
        response.headers['Content-Encoding'] = 'utf-8'
        return response
    else:
        response = app.response_class(
            response=json.dumps({'error_code': 'wrong format, use 7987654321'}),
            mimetype='application/json',
            status=422,
        )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
