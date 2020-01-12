from twilio.rest import Client

def sms_send(destNumber, srcNumber, sendMessage):

    # Your Account SID from twilio.com/console
    account_sid = "ACe1eeeac413575b6fe92dc1668bcb90b0"
    # Your Auth Token from twilio.com/console
    auth_token  = "78b81a19d6573a909e2cc4f59772eb7d"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=destNumber, 
        from_=srcNumber,
        body=sendMessage)

    # print(message.sid)
if __name__ == "__main__":
    myMessage = "Testing the twilio message"
    graham_phone = "+17785583011"
    twilio_phone = "+12563636371"
    sms_send(graham_phone, twilio_phone, myMessage)
