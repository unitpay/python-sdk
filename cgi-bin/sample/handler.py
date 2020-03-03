#!/usr/bin/env python3

from orderInfo import *

import os, sys, inspect
sys.path.append(os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../"))))

from unitpay_lib import *
from UnitPay import * 

#print ('Content-Type: text/html')
print ('Content-Type: application/json')
print()

unitpay = UnitPay( domain, secretKey )
try:

    unitpay.checkHandlerRequest()

    qs = os.environ.get('QUERY_STRING', '')
    val = urllib.parse.parse_qs(qs)
    params = parseParams(val);
    method = val['method'][0]

    if (float(params['orderSum']) != float(orderSum) or
        params['orderCurrency'] != orderCurrency or
        params['account'] != orderId or
        params['projectId'].strip() != str(projectId)):
        raise Exception('Order validation Error')

    if (method == 'check'):
        print(unitpay.getSuccessHandlerResponse('Check Success. Ready to pay.'));
    elif (method == 'pay'): 
        print (unitpay.getSuccessHandlerResponse('Pay Success'));
    elif (method == 'error'):
        print (unitpay.getSuccessHandlerResponse('Error logged'));
    elif (method == 'refund'):
        print (unitpay.getSuccessHandlerResponse('Order canceled'));
except Exception as e:
    s = str(e)
    print (unitpay.getErrorHandlerResponse(s))
    
