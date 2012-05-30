#!/usr/bin/python

import json
import requests
import re
from subprocess import Popen, PIPE

mac_format = re.compile('^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$')

def get_wifi_data():

	child = Popen(['/usr/bin/wpa_cli', 'scan_results'], stdout=PIPE);
	for l in child.stdout:
			data = l.decode('ascii').split('\t')
			mac = data[0]
			if not mac_format.match(mac):
				continue
			yield mac.replace(':','-')
	child.wait()


def craft_request():
	return json.dumps({'version': '1.1.0', 'host': 'gcl', 'wifi_towers': [ { "mac_address": mac, "age": 0 } for mac in get_wifi_data() ]})

if __name__ == '__main__':
	print(craft_request())
