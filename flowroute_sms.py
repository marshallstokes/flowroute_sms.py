#################
from flask import Flask, request, jsonify, abort
import smtplib
import json
import datetime
from configparser import ConfigParser
from email.message import EmailMessage
from email.utils import parsedate_tz, mktime_tz, formatdate

config = ConfigParser()
config.read('flowroute_sms.ini')

web_port = config['general']['web_port']
smtp_host = config['general']['smtp_host']
smtp_user = config['general']['smtp_user']
smtp_passwd = config['general']['smtp_passwd']
from_email = config['general']['from_email']
rcpt_to = config['general']['rcpt_to']
allowed_ips = config.get('general', 'allowed_ips').split("\n")

app = Flask(__name__)

@app.route('/incomingsms', methods=['POST'])
def incomingsms():
	if request.remote_addr not in allowed_ips:
		print ("aborting request from " + request.remote_addr)
		abort(502)
		
	if not request.json or not 'data' in request.json:
		print ("json dumb validation failed. abort(404)")
		abort(400)
	
	req_data = request.get_json()
	sms = req_data['data']
	from_num = sms['attributes']['from']
	to_num = sms['attributes']['to']
	sms_body = sms['attributes']['body']
	print ('from ' + from_num)
	print ('to ' + to_num)
	
	msg = EmailMessage()
	msg['From'] = from_email
	msg['To'] = rcpt_to
	msg['Subject'] = 'SMS from ' + from_num
	msg['Date'] = datetime.datetime.now().strftime("%a, %d %b %Y %X %z")
	body = """\
New SMS message from {1}: {2}
""".format(rcpt_to, from_num, sms_body)
	msg.set_content(body)
	print ("Sending email:")
	print (msg.as_string())

	try:
		smtp = smtplib.SMTP_SSL(smtp_host, 465)
		smtp.login(smtp_user,smtp_passwd)
		smtp.send_message(msg)
		smtp.quit()
	except Exception as e:
		print ("failure: %s" % e)
	return jsonify({'task': 'complete'}), 201
	

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=int(web_port))
