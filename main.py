from flask import Flask, request, render_template
from flask_mail import Mail, Message
import configparser
   
app = Flask(__name__)
app.secret_key = 'yoursecretkey' # Change this to a more secure key
   
# Configuration of mail
config = configparser.ConfigParser()
config.read('config.ini')

app.config['MAIL_SERVER']=config['E-Mail']['MAIL_SERVER']
app.config['MAIL_PORT'] = int(config['E-Mail']['MAIL_PORT'])
app.config['MAIL_USERNAME'] = config['E-Mail']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config['E-Mail']['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config.getboolean('E-Mail', 'MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = config.getboolean('E-Mail', 'MAIL_USE_SSL')

# Instantiating the mail service only after the 'app.config' to avoid error   
mail = Mail(app)

   
@app.route("/", methods=['GET', 'POST'])
def home():
    # Try and except method
    # to avoid the app crashing if the message does not go through due to network or something
    try:
        # If it is a post request
        if request.method == 'POST':
            # Getting the html inputs and referencing them
            sender = request.form['sender'] # Address that will be used if sender address provided by user does not exist on the server
            recipient = request.form['recipient'] 
            message = request.form['message']
            subject = request.form['title']
            
            # Inputing the message in the correct order
            msg = Message(subject,sender=sender,recipients =[recipient] )
            msg.body = message
            mail.send(msg)
            return "message Sent"
        return render_template('mail.html')
    except Exception as e:
        return f'<p>{e} </p>'
    
   
if __name__ == '__main__':
    # For app to run and debug to True
   app.run(debug = True)