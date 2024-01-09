#!/usr/bin/env python
# -*- coding: utf-8 -*-
# script for cronjob to autoupdate letsencrypt certificate
# author: Paul
import os
import subprocess
import requests
import json
from datetime import datetime

if __name__ == '__main__':
    date_file = '/home/pi/config/date.sh'
    days_left = None
    home_assistant_ip='192.168.1.69'
    home_assistant_port='8123'
    home_assistant_token='your_token_here'
    print('Starting lets enrypt update on {0}'.format(datetime.now()))
    if os.path.isfile(date_file):
        p = subprocess.Popen([date_file], stdout=subprocess.PIPE)
        output, _ = p.communicate()
        days_left = int(output[:-1].decode())
    if days_left and days_left < 25:
        print('getting state of port 80 forwarding to raspi')
        url = "http://{0}:{1}/api/states/switch.fritz_box_7490_port_forward_http_server".format(home_assistant_ip, home_assistant_port)
        headers = {
                "Authorization": "Bearer {0}".format(home_assistant_token),
                "content-type": "application/json",
                }
        response = requests.request("GET", url, headers=headers)
        jdata = json.loads(response.text)
        if jdata['state'] == 'off':
            print('turning port forwarding on')
            url = "http://{0}:{1}/api/services/switch/turn_on".format(home_assistant_ip, home_assistant_port)
            mydata = '{"entity_id":"switch.fritz_box_7490_port_forward_http_server"}'
            response = requests.request("POST", url, headers=headers, data=mydata)
            print(response.text)
            jdata = json.loads(response.text)

            cmd = 'sudo certbot renew'
            os.system(cmd)
            print('updated cert with certbot')

            cmd = 'sudo /etc/init.d/nginx reload'
            os.system(cmd)
            print('reloaded nginx instance')

            cmd = 'sudo /etc/init.d/nginx restart'
            os.system(cmd)
            print('restarted nginx instance')

            print('turning port forwarding off')
            url = "http://192.168.1.69:8123/api/services/switch/turn_off"
            mydata = '{"entity_id":"switch.fritz_box_7490_port_forward_http_server"}'
            response = requests.request("POST", url, headers=headers, data=mydata)
            print(response.text)
            jdata = json.loads(response.text)
            #for i in jdata:
            #    print(i, jdata[i])
        print('finished updating cert')
    else:
        print('{0} days left before update of letsencrypt cert required.'.format(days_left))
