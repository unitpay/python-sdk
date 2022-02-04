#!/usr/bin/env python3

import urllib.parse
import hashlib
import os
from urllib.request import urlopen
import json
import re
import copy
from unitpay_lib import *

class UnitPay:
	secretKey = ''
	supportedUnitpayMethods = ['initPayment', 'getPayment']
	requiredUnitpayMethodsParams = {'initPayment' : ['desc', 'account', 'sum'],'getPayment' : ['paymentId']}
	supportedPartnerMethods = ['check', 'pay', 'error'];
	supportedUnitpayIp = [
        '31.186.100.49',
        '52.29.152.23',
        '52.19.56.234',
        '127.0.0.1' # for debug
    ];
	def __init__(self, domain, secretKey):
	    self.formUrl = 'https://' + domain + '/pay/'
	    self.apiUrl = 'https://' + domain + '/api'
		self.secretKey = secretKey
	def form( self, publicKey, summ, account, desc, currency='RUB', locale='ru'):
		params = {
			'account' : account,
			'currency' : currency,
			'desc' : desc,
			'sum' : summ
		}
		params['signature'] = self.getSignature(params)
		params['locale'] = locale
		
		return self.formUrl + publicKey + '?' + urllib.parse.urlencode(params)
		
	def getSignature( self, params, method = None ):
		paramss = copy.copy(params)
		if 'signature' in paramss:
			del paramss['signature']
		if 'sign' in paramss:
			del paramss['sign']	
		paramss = ksort(paramss)
		paramss.append([0,self.secretKey])
		if method:
			paramss.insert(0,['method',method])

		#list of dict to str
		res_p = []
		for p in paramss:
			res_p.append(str(p[1]))
		strr = '{up}'.join(res_p)
		strr = strr.encode('utf-8')
		h = hashlib.sha256(strr).hexdigest()
		return h
	def checkHandlerRequest(self):
		ip = os.environ.get('REMOTE_ADDR', '')
		qs = os.environ.get('QUERY_STRING', '')
		val = urllib.parse.parse_qs(qs)
		params = parseParams(val);
		method = val['method'][0]
		if not 'method' in val:
			raise Exception('Method is null')
		if not params:
			raise Exception('Params is null')
		if not method in self.supportedPartnerMethods:
			raise Exception('Method is not supported')
		signature = self.getSignature(params, method);
		if not 'signature' in params:
			raise Exception('signature params is null')
		if params['signature'] != signature:
			raise Exception('Wrong signature')
		if not ip in self.supportedUnitpayIp:
			raise Exception ('IP address error')
		return True
	def getErrorHandlerResponse(self, message):
		return json.dumps({'error': {'message': message}})
	def getSuccessHandlerResponse(self, message):
		return json.dumps({'result': {'message': message}})
	def api(self, method, params = {}):
		if (not(method in self.supportedUnitpayMethods)):
			raise Exception('Method is not supported')
		for rParam in self.requiredUnitpayMethodsParams[method]:
			if (not rParam in params):
				raise Exception('Param ' + rParam + ' is null')
		params['secretKey'] = self.secretKey
		requestUrl = self.apiUrl + '?method=' + method + '&' + self.insertUrlEncode('params', params)
		response = urlopen(requestUrl)
		data = response.read().decode('utf-8')
		jsons = json.loads(data)
		return jsons
	def insertUrlEncode(self, inserted, params):
		result = ''
		first = True
		for p in params:
			if first:
				first = False
			else:
				result += '&'
			result += inserted + '[' + p + ']=' + str(params[p])
		return result
