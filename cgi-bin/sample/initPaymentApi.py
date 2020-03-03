#!/usr/bin/env python3

import os, sys, inspect
sys.path.append(os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../"))))

from orderInfo import *
from UnitPay import * 

unitPay = UnitPay( domain, secretKey )

try:
    response = unitPay.api('initPayment', {
        'account' : orderId,
        'desc' : orderDesc,
        'sum' : orderSum,
        'paymentType' : 'yandex',
        'currency' : orderCurrency,
        'projectId' : projectId,
    });
    if ('result' in response) and ('type' in response['result']):
        if (response['result']['type'] == 'redirect'):
            redirectUrl = response['result']['redirectUrl']
            paymentId = response['result']['paymentId']
            redirect(redirectUrl)
        elif (response['result']['type'] == 'invoice'):
            receiptUrl = response['result']['receiptUrl']
            paymentId = response['result']['paymentId']
            invoiceId = response['result']['invoiceId']
            redirect(receiptUrl)
    elif ('error' in response) and ('message' in response['error']):
        error = response['error']['message']
        print ('Content-Type: text/html; charset=UTF-8')
        print()
        print ('error: ' + error)

except Exception as e:
    s = str(e)
    print ('Content-Type: text/html; charset=UTF-8')
    print()
    print (s)

def redirect(redirectUrl):
    print ('Content-Type: text/html')
    print ('Location: ' + redirectUrl)
    print ('')# HTTP says you have to have a blank line between headers and content
    print ('<html>')
    print ('  <head>')
    print ('    <meta http-equiv="refresh" content="0;url=' + redirectUrl + '" />')
    print ('    <title>You are going to be redirected</title>')
    print ('  </head>' )
    print ('  <body>')
    print ('    Redirecting... <a href="' + redirectUrl + '">Click here if you are not redirected</a>')
    print ('  </body>')
    print ('</html>')
