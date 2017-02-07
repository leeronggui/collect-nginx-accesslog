#!/usr/bin/env python
import sys
import re
import time 
import urllib
import urllib2
import json
import os

#statistical_res_dict = {
#	"mwallet_200": 1000,
#	"mwallet_302": 0,
#}

statistical_res_dict = {}

data_list = []

status_code_list = [
	200,
        302,
        400,
        404,
        499,
        500,
        502,
        403,
]

module_list = [
        "mwallet",
	"enterprise-web",
	"site",
	"mag",
	"mgs",
	"sitemember",
	"cashier",
	"fcw",
	"ucenter"
]

#init statistical_res_dict
for status_code in status_code_list:
    for module in module_list:
        statistical_res_dict_key = module + '_' + str(status_code)
        statistical_res_dict[statistical_res_dict_key] = 0 
statistical_res_dict["nginx_ignore"] = 0
statistical_res_dict["nginx_notmatch"] = 0
    
#print statistical_res_dict
pattern = re.compile(r'LVS:(.*) clientIP:(.*) cdnIP:(.*) \[(.*)\] Host:(.*) \"(.*)\" (.*) (.*) \"(.*)\" \"(.*)\" (.*) (.*)')

while True:
    #break
    line = sys.stdin.readline()
    if not line:break
    m = pattern.match(line)
    print len(m.groups())
    print m.group(0)
    #statistical_res_dict["nginx_notmatch"] = statistical_res_dict["nginx_notmatch"] + 1
    if len(m.groups()) != 12:
        print len(m.groups())
        statistical_res_dict["nginx_notmatch"] = statistical_res_dict["nginx_notmatch"] + 1
        continue
    #Get module name 
    request_list = m.group(6).split(' ')
    if len(request_list) != 3:
	statistical_res_dict["nginx_notmatch"] = statistical_res_dict["nginx_notmatch"] + 1
        continue
    path_list = request_list[1].split('/')
    module = path_list[1]

    #Get nginx request code
    status_code = m.group(7)

    #Get body bytes
    body_bytes = m.group(8)
    
    #Get request_time
    request_time = m.group(12)

#    print module, body_bytes, request_time
    #print module,status_code
    if module in module_list and int(status_code) in status_code_list:
        statistical_res_dict_key = module + '_' + str(status_code)
        statistical_res_dict[statistical_res_dict_key] = statistical_res_dict[statistical_res_dict_key] + 1
    else:
        statistical_res_dict["nginx_ignore"] = statistical_res_dict["nginx_ignore"] + 1

    
#print statistical_res_dict

def post_data_to_agent(endpoint, metric, value):
    ts = str(time.time()).split('.')[0]
    values_dict = {"metric": "None", "endpoint": "None", "timestamp": "None","step": 60,"value": 0,"counterType": "GAUGE","tags": "project=web,module=nginx"}
    values_dict['metric'] = metric
    values_dict['endpoint'] = endpoint
    values_dict['value'] = value
    values_dict['timestamp'] = int(ts)
    #url = 'http://127.0.0.1:1988/v1/push'
    #user_agent = 'application/x-www-form-urlencoded'
    #headers = {'User-Agent' : user_agent}  
    #data = urllib.urlencode(values_dict)
    return values_dict
    #data = json.dumps(values_dict)

    #output = os.popen('curl -X POST -d \"%s\"' % (values_dict))
    #print 22222222222222222
    #print("curl -X POST -d \"%s\" http://127.0.0.1:1988/v1/push" % (data))
    #output = os.popen("curl -X POST -d \"%s\" http://127.0.0.1:1988/v1/push" % (values_dict))
    #output = os.popen("curl -X POST -d \"[{\\\"metric\\\": \\\"%s\\\", \\\"endpoint\\\": \\\"test\\\", \\\"timestamp\\\": "%s",\\\"step\\\": 60,\\\"value\\\": %s,\\\"counterType\\\": \\\"GAUGE\\\",\\\"tags\\\": \\\"project=web,module=nginx\\\"}]\"  http://127.0.0.1:1988/v1/push" % (metric, ts, value))
    #print("curl -X POST -d \"[{\\\"metric\\\": \\\"aaa"\\\", \\\"endpoint\\\": \\\"test\\\", \\\"timestamp\\\": "aaa",\\\"step\\\": 60,\\\"value\\\": 222,\\\"counterType\\\": \\\"GAUGE\\\",\\\"tags\\\": \\\"project=web,module=nginx\\\"}]\" http://127.0.0.1:1988/v1/push")
    #print output.read()
    #req = urllib2.Request(url, data, headers)
    #print req
    #response = urllib2.urlopen(req) 
    #print 11111111111111111112
    #the_page = response.read()  
    #print ts
#   print type(values_dict)
    #print the_page
for key in statistical_res_dict.keys():
    value = statistical_res_dict[key]

    data = post_data_to_agent("nginx_online",key,value)
    data_list.append(data)

datas =  json.dumps(data_list).replace("\"","\\\"")

print("curl -s -X POST -d \"%s\" http://127.0.0.1:1988/v1/push" % (datas))
output = os.popen("curl -X POST -d \"%s\" http://127.0.0.1:1988/v1/push" % (datas))
print output.read()
