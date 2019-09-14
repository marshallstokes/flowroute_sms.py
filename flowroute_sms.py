#################
from flask import Flask, request, jsonify
import smtplib

gmail_user = 'user@gmail.com'
gmail_passwd = 'PASSWORD'

rcpt_to = 'XXXXXXX@vtext.com'

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
    return jsonify({'task': 'task'}), 201


app.run(host="0.0.0.0",port=int("8080"))