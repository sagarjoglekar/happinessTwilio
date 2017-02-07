# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioRestClient
import ParseTwilioConfig
import time
import os

from flask import Flask, request, redirect
import twilio.twiml



class MessageBuilder:
    _from = "+17079883108"
    _to = "+17072196111"
    Body = "Welcome to Dubai, This is a cost free Message.."

    def __init__(self , t=None , f=None):
        if t != None:
            self._to = t
        if f != None:
            self._from = f

    def buildTransitMessage(self):
        str1 = "You have landed on Terminal 1, your connecting fligt is on terminal 2 and it will take you 15 minutes to reach there"
        str2 = "Further information about the gates would be delivered cost free when you reach there"
        return str1 + str2

    def buildWelcomeMessage(self):
        str1 = "Currently the approximate immigration time is 35 minutes "
        str2 = "Information about baggage would be delivered once you reach immigration"
        return str1 + str2

    def buildBaggageMessage(self):
        str1 = "Your bags are on Carousal 5"
        str2 = "The turn around time is nominal and you should get your bags in approximately 10 minutes"
        return str1 + str2

    def buildFarewell(self):
        str1 = "I hope your transit/experience with DXB was pleasent. We look forward to serve you again. Enjoy DubHI!!"
        return str1

    def to(self):
        return self._to

    def src(self):
        return self._from


def wait():
    os.system('read -s -n 1 -p "Press any key to continue..."')


RAN_ONCE = False
config = ParseTwilioConfig.Parser("sagar.config")
config.parseConfig()

def runOnce():
    if not RAN_ONCE:
        account_sid = config.getAccountSid()
        auth_token  = config.getAuthToken()
        client = TwilioRestClient(account_sid, auth_token)


        Mbuilder = MessageBuilder()
        m1 = client.messages.create(to=Mbuilder.to(), from_=Mbuilder.src(),body=Mbuilder.Body)
        print "Sent Body"
        time.sleep(30)

        m2 = client.messages.create(to=Mbuilder.to(), from_=Mbuilder.src(),body=Mbuilder.buildWelcomeMessage())
        print "Sent Welcome message"
        time.sleep(30)

        m3 = client.messages.create( to = Mbuilder.to() , from_ = Mbuilder.src(), body = Mbuilder.buildBaggageMessage())
        print " Sent baggage message"
        time.sleep(30)

        m4 = client.messages.create( to = Mbuilder.to() , from_ = Mbuilder.src() , body = Mbuilder.buildFarewell() );
        print "Sent farewell"

        RAN_ONCE = True


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)



if __name__ == "__main__":

    runOnce()

    app.run(debug=True)



