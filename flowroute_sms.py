#################
from flask import Flask, request, jsonify
import smtplib
from configparser import ConfigParser

config = ConfigParser()
config.read('flowroute_sms.ini')

web_port = config['general']['web_port']
gmail_user = config['general']['gmail_user']
gmail_passwd = config['general']['gmail_passwd']
rcpt_to = config['general']['rcpt_to']

app = Flask(__name__)

@app.route('/incomingsms', methods=['POST'])
def incomingsms():
    from_num = request.json['from']
    to_num = request.json['to']
    body = request.json['body']
    try:
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(gmail_user,gmail_passwd)
        message = """From: <{}>
To: <{}>
Subject: Text From {}

Text Message: {}
""".format(gmail_user, rcpt_to, from_num, body)

        smtp.sendmail(
                gmail_user,
                rcpt_to,
                message)
        smtp.quit()
    except:
        print ("Something broke")
    return jsonify({'task': 'complete'}), 201
    

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int(web_port))
