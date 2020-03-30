# flowroute_sms.py

Python3 script that runs a small Flask app that takes in Flowroutes API Webhook for SMS through JSON, takes it apart, and sends an email out authenticated gmail account.

Download flowroute_sms.py and flowroute_sms.ini; modify flowroute_sms.ini for your environment.

You need flask: `pip3 install --user flask`

run script via
`nohup /usr/local/bin/python3 flowroute_sms.py &`

