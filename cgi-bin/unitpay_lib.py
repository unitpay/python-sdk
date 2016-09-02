import re

#parse "params" in request
def parseParams( s ):
	params = {}
	for v in s:
		if re.search('params', v):
			p = v[len('params['):-1]    
			params[p] = s[v][0]
	return params
#sorted by key
def ksort(d):
	return [[k,d[k]] for k in sorted(d.keys())]