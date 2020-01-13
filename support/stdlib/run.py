from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_receive():

    # Display sent message
    number = request.form['From']
    msg = request.form["Body"]
    koala = {'msg':'','num':''}
    print("Message recieved from: " + number)
    print("Message: " + msg)
    return render_template("index.html",stuff=koala)

if __name__ == "__main__":
    app.run(debug=True)

    