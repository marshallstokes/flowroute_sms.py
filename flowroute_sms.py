#################
from flask import Flask, request, jsonify
import smtplib
from configparser import ConfigParser

config = ConfigParser()
config.read('flowroute_sms.ini')

web_port = config['general']['web_port']
smpt_user = config['general']['smtp_user']
smtp_passwd = config['general']['smtp_passwd']
rcpt_to = config['general']['rcpt_to']

app = Flask(__name__)

@app.route('/incomingsms', methods=['POST'])
def incomingsms():
    from_num = request.json['from']
    to_num = request.json['to']
    body = request.json['body']
    try:
        smtp = smtplib.SMTP_SSL(smtp_host, 465)
        smtp.login(smtp_user,smtp_passwd)
        message = """From: <{}>
To: <{}>
Subject: Text From {}

Text Message: {}
""".format(smtp_user, rcpt_to, from_num, body)

        smtp.sendmail(
                smtp_user,
                rcpt_to,
                message)
        smtp.quit()
    except:
        print ("Something broke")
    return jsonify({'task': 'complete'}), 201
    

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int(web_port))
