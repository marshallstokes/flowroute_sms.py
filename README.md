# flowroute_sms.py

Python3 script that runs a small Flask app that takes in Flowroutes API Webhook for SMS through JSON, takes it apart, and sends an email out authenticated gmail account.

Just download  flowroute_sms.py and flowroute_sms.ini; modify flowroute_sms.ini with your values:\
[general]\
web_port = 8080\
gmail_user = username@gmail.com\
gmail_passwd = gmailpassword\
rcpt_to = 4055551212@vtext.com\

and run script via
nohup /usr/local/bin/python3 flowroute_sms.py &
