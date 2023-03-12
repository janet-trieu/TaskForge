'''
Temporary file to store the functionality to send emails to a user
'''
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'compgpt3900@gmail.com'
app.config['MAIL_PASSWORD'] = "gqjtjsnnaxwqeeeg"

mail = Mail(app)
@app.route("/")
def index():

    sending_email = "compgpt3900@gmail.com"

    recipient = "dabin.haam@gmail.com"

    msg = Message("Testing",
        sender=sending_email,
        recipients=[recipient])
    msg.body = "Testing"

    mail.send(msg)
    return "Sent"

if __name__ == "__main__":
    app.run(debug=True) # Do not edit this port