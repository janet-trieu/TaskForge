from flask import Flask
from flask_mail import Mail, Message
from flask import Flask, request

from src.proj_master import *

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'compgpt3900@gmail.com'
app.config['MAIL_PASSWORD'] = "gqjtjsnnaxwqeeeg"

sending_email = "compgpt3900@gmail.com"

mail = Mail(app)

@app.route('/invite/to/project', methods=['POST'])
def invite_to_project_flask():
    inputs = request.get_json()
    proj_inv = invite_to_project(inputs['pid'], inputs['sender_uid'], inputs['receiver_uid'])

    receipient_email = proj_inv[0]
    msg_title = proj_inv[1]
    msg_body = proj_inv[2]

    msg = Message(msg_title, sender = sending_email, recipients = [receipient_email])
    msg.body = msg_body
    mail.send(msg)