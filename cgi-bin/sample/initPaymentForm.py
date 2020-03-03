#!/usr/bin/env python3

import os, sys, inspect
sys.path.append(os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../"))))

from orderInfo import *
from UnitPay import * 

unitpay = UnitPay( domain, secretKey )
redirectUrl = unitpay.form( publicId, orderSum, orderId, orderDesc, orderCurrency )

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