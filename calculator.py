#!/usr/bin/python
'''
Dave Fugelso, Python Certification Course February 14, 2015.

Implement a simple calculator based on IRI path values using WSGI.

'''

import datetime
import re


default = "No Value Set"

#HTML for root/instruction page.
body = """<html>
<head>
<title>Session 6 Homework - a web browser calculator</title>
</head>
<body>

You may add, multiply, subtract and divide. <br>
<br>
The syntax for an operation is &ltoperator&gt/&gtoperand 1&gt/&ltoperand 2&gt. Valid operands include: 'add', 'plus', 'subtraction', 'sub', 'multiplication', 'times', 'mult', 'division', and 'div'<br>
<br>


</body>
</html>"""

#String to hold the result
result_format = """<html>
<head>
<title>Session 6 Homework - Resultes Page</title>
</head>
<body>

<strong>Your results: {} {} {} = {} </strong><br>
<br>
<a href="http://localhost:8080/">Go Back</a><br>
<br>


</body>
</html>"""


add = ['add', 'plus']
sub = ['subtraction', 'sub']
mul = ['multiplication', 'times', 'mult']
div = ['division', 'div']
operations = add + sub + mul + div

def get_operands (operands):
    '''
    Get operands for the operation, Raise a value error if any issues.
    '''
    if len(operands) != 3:
        raise ValueError
    
    op1 = int(operands[1])
    op2 = int(operands[2])

    return op1, op2
    
def operate (operator, op1, op2):
    '''
    Perform the arithmetic operation.
    '''
    if operator in add:
        return op1 + op2, '+'
    elif operator in sub:
        return op1 - op2, '-'
    elif operator in mul:
        return op1 * op2, '*'
    elif operator in div:
        if op2 == 0:
            raise ValueError
        return op1/op2, '/'
    else:
        print operator, op1, op2
        raise ValueError
        
def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    operands = path.split('/')

    status = '200 OK'
    
    try:
        if path == '' or len(operands)==0:
            # Root page. Display instructions.
            response_body = body
        elif operands[0] in operations:
            try:
                op1, op2 = get_operands (operands)
                val, symbol = operate(operands[0], op1, op2)
                response_body = result_format.format (op1, symbol, op2, val)         
            except ValueError:
                status = '400 Bad Request'
                response_body = 'Bad Request'
        else:
            status = '404 Not Found'
            response_body = 'Page not found'   
    except:
        #Yes, catching any and all exceptions here.
        status = '500 Internal Server Error'
        response_body = 'Something went terribly wrong.'
        
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]   
    start_response(status, response_headers)

    return [response_body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()